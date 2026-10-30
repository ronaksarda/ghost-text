"""python -m model.train — LoRA fine-tune of the judge on Tinker (train split only), checkpoint chosen on val.

Writes model/checkpoint.txt (the tinker:// sampler path) and model/train_log.json (loss, val scores, tokens, cost).
The test split is never touched here.
"""
import json
import time
from pathlib import Path

import tinker
from tinker import types

import envfile
from eval.run import LABELS, load, metrics
from judge.prompt import parse, render, target

BASE = "Qwen/Qwen3-8B"
RANK, LR, EPOCHS, BATCH = 32, 2e-4, 3, 16
PRICE = {"train": 0.44, "prefill": 0.195, "sample": 0.60}  # $ per 1M tokens, Tinker pricing page, Oct 30 2026
HERE = Path(__file__).parent


def datum(tok, row: dict) -> tuple[types.Datum, int, int]:
    prompt = tok.encode(render(row["text"], row["technique"], row["context"]), add_special_tokens=False)
    answer = tok.encode(target(row["label"]), add_special_tokens=False)
    full = prompt + answer
    return types.Datum(
        model_input=types.ModelInput.from_ints(tokens=full[:-1]),
        loss_fn_inputs={"weights": [0.0] * (len(prompt) - 1) + [1.0] * len(answer), "target_tokens": full[1:]},
    ), len(full), len(answer)


def sample_labels(sampler, tok, rows: list[dict]) -> tuple[list[str], int, int]:
    params = types.SamplingParams(max_tokens=12, temperature=0.0, stop=["<|im_end|>"])
    prompts = [tok.encode(render(r["text"], r["technique"], r["context"]), add_special_tokens=False) for r in rows]
    futures = [sampler.sample(prompt=types.ModelInput.from_ints(tokens=p), num_samples=1, sampling_params=params)
               for p in prompts]  # all in flight at once
    outs = [tok.decode(f.result().sequences[0].tokens) for f in futures]
    return [parse(o)[0] for o in outs], sum(map(len, prompts)), sum(len(tok.encode(o)) for o in outs)


def main() -> None:
    envfile.load()
    train, val = load("train"), load("val")
    service = tinker.ServiceClient()
    trainer = service.create_lora_training_client(base_model=BASE, rank=RANK)
    tok = trainer.get_tokenizer()
    data = [datum(tok, r) for r in train]
    log = {"base_model": BASE, "rank": RANK, "lr": LR, "batch": BATCH, "epochs": [], "tokens": {"train": 0, "prefill": 0, "sample": 0}}
    best = None
    for epoch in range(1, EPOCHS + 1):
        order = sorted(range(len(data)), key=lambda i: hash((epoch, i)) % 10_007)  # fixed shuffle per epoch
        losses = []
        for s in range(0, len(order), BATCH):
            batch = [data[i] for i in order[s:s + BATCH]]
            fb = trainer.forward_backward([d for d, _, _ in batch], "cross_entropy")
            opt = trainer.optim_step(types.AdamParams(learning_rate=LR))
            out = fb.result()
            opt.result()
            log["tokens"]["train"] += sum(n for _, n, _ in batch)
            losses.append(out.metrics.get("loss:sum", 0.0) / sum(a for _, _, a in batch))  # mean loss per answer token
        path = trainer.save_weights_for_sampler(name=f"epoch{epoch}").result().path
        preds, pre, smp = sample_labels(service.create_sampling_client(model_path=path), tok, val)
        log["tokens"]["prefill"] += pre
        log["tokens"]["sample"] += smp
        m = metrics(val, preds, 0.0)
        macro = sum(m["per_class"][c]["f1"] for c in LABELS) / len(LABELS)
        log["epochs"].append({"epoch": epoch, "path": path, "mean_loss": sum(losses) / len(losses),
                              "val_macro_f1": macro, "val_injection_f1": m["per_class"]["injection"]["f1"],
                              "val_real_site_fp_rate": m["real_site_fp_rate"]})
        print(json.dumps(log["epochs"][-1]))
        if best is None or macro > best[0]:
            best = (macro, path)
    log["chosen"] = best[1]
    log["cost_usd"] = round(sum(log["tokens"][k] * PRICE[k] for k in PRICE) / 1e6, 4)
    log["finished"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (HERE / "checkpoint.txt").write_text(best[1] + "\n")
    (HERE / "train_log.json").write_text(json.dumps(log, indent=2))
    print(f"chosen {best[1]} (val macro F1 {best[0]:.3f}), about ${log['cost_usd']}")


if __name__ == "__main__":
    main()

# Hacktoberfest 2026 Week 4 ("Ghost in the Machine"): research notes

Research date: 2026-10-28. All submission counts are a snapshot taken on that date from the public DEV API and will grow until the deadline.

## Summary

- **You cannot win two prize categories in Week 4.** The contest rules say you may submit one entry, and *"each participant may win no more than one (1) prize in the Contest."* One entry can still be *considered* for the overall prize and for every partner category it meaningfully uses. That raises your odds of winning something, but it caps you at one prize. ([contest rules](https://dev.to/page/hacktoberfest-week4-2026-10-26-contest-rules), [challenge FAQ](https://dev.to/challenges/hacktoberfest-week4-2026-10-26))
- **Deadline: October 31, 2026 at 11:59 PM PDT, which is November 1, 06:59 UTC.** Week 4 is the last of five rounds, so there is no later Hacktoberfest round where you could win a second prize. ([contest rules](https://dev.to/page/hacktoberfest-week4-2026-10-26-contest-rules), [Hacktoberfest knowledge doc schedule](https://devrelay.com/knowledge/hacktoberfest))
- **The write-up matters most.** The criteria are Writing Quality (weighted most heavily), Relevance to the Prompt and Theme, Creativity, Technical Execution, and Use of Partner Technology (prize categories only). The FAQ says *"A great project with a thin write-up won't win."* ([challenge page](https://dev.to/challenges/hacktoberfest-week4-2026-10-26))
- **The field is crowded.** About 355 confirmed Week 4 entries were up within two days. Haunted terminals, digital ofrendas, dead-code or git "séances", and ghost-story generators dominate. 82 entries claim Best Use of Gemma, while most partner categories have only 1 to 3 claimants. ([#hf26challenge feed](https://dev.to/api/articles/latest?tag=hf26challenge))
- **Past winners share a recognizable pattern.** They typically have a specific person or problem in the title, a number in the headline, a measured evaluation with failures shown, a "first user" or reaction section, and multiple partner technologies doing real work. The median length is about 2,300 words. Reactions are low (median 5), so the judges, not popularity, decide. ([Weekend winners](https://dev.to/devteam/congrats-to-the-hacktoberfest-weekend-challenge-build-for-a-friend-winners-pgc), [Week 1 winners](https://dev.to/devteam/congrats-to-the-hacktoberfest-open-source-ai-challenge-touch-grass-winners-152c), [Week 2 winners](https://dev.to/devteam/congrats-to-the-hacktoberfest-open-source-ai-challenge-week-2-side-hustle-winners-2i33))

## Challenge rules & tracks

**Prompt.** This prompt is the same for all five Hacktoberfest challenges: *"Build something with open-source AI at its core."* This can mean an open-weight model, an open-source agent harness or framework, local inference, or a mix. *"the open pieces should be what makes your project work."* Your post must explain *"why open innovation matters for what you built."* ([challenge page](https://dev.to/challenges/hacktoberfest-week4-2026-10-26))

**Theme, "Ghost in the Machine".** *"Build something spooky, or something that honors the past in the spirit of Día de los Muertos, with open-weight models or open-source AI."* The page says the theme is *"intentionally broad"*. Its example ideas are a haunted terminal, a virtual ofrenda builder, an offline séance chatbot for a dead programming language, a local oral-history tool, a ghost story built from smart-home sensor logs, and reviving an abandoned open-source tool or a forgotten corner of internet history. ([challenge page](https://dev.to/challenges/hacktoberfest-week4-2026-10-26), [launch post](https://dev.to/devteam/join-the-hacktoberfest-open-source-ai-challenge-ghost-in-the-machine-2850-in-prizes-across-21-3cho))

**Prizes ($2,850 across 21 winners).** ([contest rules](https://dev.to/page/hacktoberfest-week4-2026-10-26-contest-rules))
- Overall winner (1): $250 USD, a DEV++ membership, and an exclusive badge.
- Featured categories (6), each $200 and a badge: Render, TabPFN, Tinker, Arduino, DigitalOcean, Gemma.
- Partner categories (14), each $100 and a badge: Auth0 for AI Agents, Backboard, Browserbase, ElevenLabs, Entire, GitHub Copilot, Mastra, MongoDB Atlas, Sentry Agent Tracing, SerpApi, Temporal, Tiger Data, Ultramarine (Paper Instruments), and a .tech domain.
- Every valid entry gets a completion badge.

**How many entries and wins:**
- Rules: *"You may submit one (1) Entry during the Entry Period. In the event that a participant submits more than one Entry, only the first Entry submitted will be considered for judging."* ([contest rules](https://dev.to/page/hacktoberfest-week4-2026-10-26-contest-rules))
- Rules: *"An Entry may be submitted to every prize category whose technology it meaningfully uses, but each participant may win no more than one (1) prize in the Contest."* ([contest rules](https://dev.to/page/hacktoberfest-week4-2026-10-26-contest-rules))
- FAQ, "Can one submission win more than once?": *"No."* It continues: *"you can win once per challenge, and we'll aim to celebrate as many different builders as possible across the month."* ([challenge page](https://dev.to/challenges/hacktoberfest-week4-2026-10-26), [HF26 hub](https://dev.to/challenges/hf26))
- Evidence that the rule is enforced: the Weekend overall winner used ElevenLabs, Render, and Sentry ([post](https://dev.to/adk_bbx/phone-calls-are-the-boss-fight-of-living-in-japan-1h6h)) and won only the overall prize. The Week 2 eBay-recall post used SerpApi, Temporal, and Backboard ([post](https://dev.to/dronzer2code/we-searched-ebay-for-237-recalled-products-only-45-of-12562-listings-named-the-model-2efi)) and won only SerpApi ([Week 2 winners](https://dev.to/devteam/congrats-to-the-hacktoberfest-open-source-ai-challenge-week-2-side-hustle-winners-2i33)).
- Across weeks, the same person can win again. For example, anishisbusy won Tiger Data in Week 1 and Backboard in Week 2, and antoniahp won Sentry in Week 1 and .tech in Week 2 ([Week 1 winners](https://dev.to/devteam/congrats-to-the-hacktoberfest-open-source-ai-challenge-touch-grass-winners-152c), [Week 2 winners](https://dev.to/devteam/congrats-to-the-hacktoberfest-open-source-ai-challenge-week-2-side-hustle-winners-2i33)). Week 4 is the final round.

**Required elements.** Missing any of these risks the entry being treated as incomplete. ([contest rules](https://dev.to/page/hacktoberfest-week4-2026-10-26-contest-rules))
1. A published DEV post that uses the submission template and the challenge tag.
2. A new project, created during the Entry Period, built with open-weight models or open-source AI, that responds to the theme.
3. A demo in the post, such as a deployed link or a video walkthrough.
4. A link to the code repository.
5. An explanation of which open-source AI was used, how the project is built around it, and why open innovation matters.
6. If you enter partner categories, a list of them in the post, plus *"a meaningful use of the corresponding partner technology."*

**Submission template.** The front matter is `tags: devchallenge, hf26challenge`. The first line is *"This is a submission for the Hacktoberfest Open-Source AI Challenge Week 4: Ghost in the Machine"*, linked to the challenge page. The sections are: What I Built; Demo; Code; How I Built It; Why Does Open Innovation Matter?; My Agent Session (optional, *"judges love it"*); The Spirit of It (optional: *"this is where you can make your post stand out... Show us the moment it landed"*); Prize Categories; and a note to credit teammates' DEV usernames. Source: the prefill link on the [challenge page](https://dev.to/challenges/hacktoberfest-week4-2026-10-26) and the [launch post](https://dev.to/devteam/join-the-hacktoberfest-open-source-ai-challenge-ghost-in-the-machine-2850-in-prizes-across-21-3cho). DEV allows four tags at most, so two slots are left free ([DEV guidelines knowledge doc](https://devrelay.com/knowledge/dev-guidelines)).

**Other rules:** ([challenge page](https://dev.to/challenges/hacktoberfest-week4-2026-10-26))
- **No old projects.** *"all submissions and their respective repositories must be started and completed within the challenge window. Commits made after the submission deadline must be noted in the project's readme."* Pull requests to existing projects do not count.
- **Teams.** Up to four people, with one post per team. List teammates' DEV handles, and the team splits any prize itself.
- **Prior work.** Building on open source is encouraged, but changes must be significant, and any *"non-generic, non-trivial usage of prior work"* must be credited. Plagiarism makes an entry ineligible.
- **Language.** Only English entries are eligible for prizes.
- **Eligibility.** You must be 18 or older. The excluded countries are listed in the [General Official Rules](https://dev.to/page/official-hackathon-rules), summarized in the [DEV Challenges knowledge doc](https://devrelay.com/knowledge/dev-challenges). The sponsor is Major League Hacking PBC ([contest rules](https://dev.to/page/hacktoberfest-week4-2026-10-26-contest-rules)).

**AI use and disclosure:**
- Challenge FAQ: *"Use of AI is allowed as long as all other rules are followed."* ([challenge page](https://dev.to/challenges/hacktoberfest-week4-2026-10-26))
- DEV's AI guidelines ask authors to disclose AI assistance, either with #ABotWroteThis or anywhere in the post, to check facts, and to be able to stand by the content. The API's `ai_disclosure_level` must be `some_ai` or `fully_autonomous` for AI-assisted posts, never `no_ai`. ([DEV AI guidelines](https://dev.to/guidelines-for-ai-assisted-articles-on-dev), [dev.to/llms.txt](https://dev.to/llms.txt), summarized in the [DEV guidelines knowledge doc](https://devrelay.com/knowledge/dev-guidelines))
- Embedding an agent session is optional but encouraged: *"it helps the judges understand your process."* ([challenge page](https://dev.to/challenges/hacktoberfest-week4-2026-10-26)) The Sanity Challenge page warned that uploaded sessions are unlisted by default and should be checked for keys before they are made public ([DEV Challenges knowledge doc](https://devrelay.com/knowledge/dev-challenges)).

## Judging criteria

The exact wording comes from the [launch post](https://dev.to/devteam/join-the-hacktoberfest-open-source-ai-challenge-ghost-in-the-machine-2850-in-prizes-across-21-3cho):

- **Writing Quality (weighted most heavily):** *"Is the post clear and engaging? Does it explain what you built, who it's for, and why open innovation matters?"*
- **Relevance to the Prompt and Theme:** *"Is open-source AI or open-weight models at the core of the project? Does it capture the spirit of the theme in a thoughtful way?"*
- **Creativity:** *"Is it an original idea, or a fresh take on a familiar problem?"*
- **Technical Execution:** *"Does it work, and is it well built?"*
- **Use of Partner Technology (optional):** *"does the project use that technology in a meaningful way?"*

The contest rules say the partner criterion applies to *"prize category winners only"* ([contest rules](https://dev.to/page/hacktoberfest-week4-2026-10-26-contest-rules)). The FAQ adds: *"This is DEV, so your write-up matters most. A great project with a thin write-up won't win."* ([challenge page](https://dev.to/challenges/hacktoberfest-week4-2026-10-26))

**Ties.** *"the judges will select the entry that received the highest number of positive reactions"* ([contest rules](https://dev.to/page/hacktoberfest-week4-2026-10-26-contest-rules)).

**Judges.** The judges are not named. The rules say only *"a panel as selected by Sponsor."* This is **unverified**: no judge names appear on the challenge page, rules page, or launch post.

**Weights.** No numeric weights are published beyond Writing Quality being *"weighted most heavily."*

## Deadlines

| Event | When | Source |
| --- | --- | --- |
| Entry period opens | Oct 26, 2026, 9:00 AM PDT | [contest rules](https://dev.to/page/hacktoberfest-week4-2026-10-26-contest-rules) |
| **Submissions due** | **Oct 31, 2026, 11:59 PM PDT (Nov 1, 06:59 UTC)** | [contest rules](https://dev.to/page/hacktoberfest-week4-2026-10-26-contest-rules), [launch post](https://dev.to/devteam/join-the-hacktoberfest-open-source-ai-challenge-ghost-in-the-machine-2850-in-prizes-across-21-3cho) |
| Winners announced | "Week of November 2", in a DEV post | [challenge page](https://dev.to/challenges/hacktoberfest-week4-2026-10-26) |
| Prize contact | Within 10 business days of the announcement; tax and affidavit forms due within 7 business days | [challenge page](https://dev.to/challenges/hacktoberfest-week4-2026-10-26) |

The sponsor's server clock is the official clock ([DEV Challenges knowledge doc](https://devrelay.com/knowledge/dev-challenges)). Past announcement posts went up 4 to 5 days after each close: Weekend on Oct 9, Week 1 on Oct 16, Week 2 on Oct 23 ([devteam posts](https://dev.to/api/articles?username=devteam&per_page=40)). As of Oct 28, the Week 3 winners post was not yet published.

## Sponsor requirements

These are the exact requirements per category, from the [challenge page](https://dev.to/challenges/hacktoberfest-week4-2026-10-26). Every category also needs *"a meaningful use"* and must be listed in the Prize Categories section ([contest rules](https://dev.to/page/hacktoberfest-week4-2026-10-26-contest-rules)).

**Featured categories ($200):**

| Category | Requirement (abridged from the page) | Week 4 entries claiming it* |
| --- | --- | --- |
| Render | Use Render as the AI runtime, to host an agent front end, or to run Hermes or OpenClaw | 18 |
| TabPFN | Use Prior Labs' tabular model to forecast, predict, classify, or spot anomalies from data such as a CSV. TabPFN-3.5 is recommended (open-weight, free under a non-commercial license signed at platform.priorlabs.ai). Prior Labs *"favors projects that use TabPFN inside a wider prediction agent"* | 5 |
| Tinker | Fine-tune a model for a specific task with Thinking Machines' Tinker, and *"show a clear improvement in performance, latency, or cost over a baseline"* | 1 |
| Arduino | Build with an Arduino UNO Q: run a model on the board, build a physical agent, or optimize with Qualcomm AI Hub | 1 |
| DigitalOcean | Host the app or agent, run an open-weight model on a GPU Droplet, or use the Gradient AI Platform | 3 |
| Gemma | Use Gemma: run it locally, fine-tune it, or serve it | 82 |

**Partner categories ($100):**

| Category | Requirement | Claims* |
| --- | --- | --- |
| Auth0 for AI Agents | Sign-in for an agent, Token Vault tool calls, human approval of risky actions, or fine-grained authorization for RAG | 1 |
| Backboard | R-CLI, compare open-weight models through one API key, or memory/RAG for an open-source project's assistant | 4 |
| ElevenLabs | Give an agent a voice, transcribe audio for a local model, or narrate the demo | 7 |
| Browserbase | Drive a live site with the Stagehand SDK, gather context for an open model, or make a repeatable workflow | 1 |
| Entire | Share the agent sessions behind the project, or search past agent work to explain code | 6 |
| GitHub Copilot | Copilot coding agent, CLI, or app; GitHub Actions; or Copilot PR review | 9 |
| Mastra | Orchestrate an agent over open models, add memory and tools, or triage GitHub issues | 3 |
| MongoDB Atlas | Data layer, Vector Search, or agent long-term memory | 3 |
| Ultramarine | Use Paper Instruments' model on real work via the OpenAI or Anthropic SDKs, and *"say what your run actually cost"* ($5 credit) | 1 |
| Sentry Agent Tracing | Show the agent's setup, performance (latency, tokens, cost), findings, and debugging, with *"traces or screenshots"* | 6 |
| SerpApi | Live web search for an agent, RAG grounded in fresh results, or news tracking | 0 to 1 |
| .tech domain | Put the project live on a .tech domain claimed through Hacktoberfest and link it (free first year, $29.99 a year after) | 3 |
| Temporal | Wrap the agent in a Temporal workflow so it survives failures and retries | 3 |
| Tiger Data | pgvector embeddings, hybrid search, or Tiger MCP | 2 |

\*The claim counts come from my keyword scan of the "Prize Categories" section in 355 Week 4 posts fetched on Oct 28 through the [DEV API](https://dev.to/api/articles/latest?tag=hf26challenge). They are approximate: keyword matching misses some entries and over-matches others, about 37 posts could not be fetched, and 200 of the 355 posts listed no categories.

**Credits.** Tinker, Render, and Backboard credits, a free .tech domain, and $5 of Ultramarine credit are available at hacktoberfest.com/my/promos ([challenge page](https://dev.to/challenges/hacktoberfest-week4-2026-10-26)). I did not verify the amounts or availability: the page requires a login, and the DevRelay MLH tools were not authenticated in this session.

## Past winners analysis

**Earlier rounds** ([HF26 hub](https://dev.to/challenges/hf26)):

| Round | Theme | Window |
| --- | --- | --- |
| Weekend | Build for a Friend | Oct 2 to 5 |
| Week 1 | Touch Grass | Oct 5 to 11 |
| Week 2 | Side Hustle | Oct 12 to 18 |
| Week 3 | Slow and Steady | Oct 19 to 25 (winners not yet announced on Oct 28) |

**Winner announcement posts:**
- [Weekend: Build for a Friend winners](https://dev.to/devteam/congrats-to-the-hacktoberfest-weekend-challenge-build-for-a-friend-winners-pgc). The post says it was *"our most participated-in challenge to date, nearly tripling our previous record."*
- [Week 1: Touch Grass winners](https://dev.to/devteam/congrats-to-the-hacktoberfest-open-source-ai-challenge-touch-grass-winners-152c). Turnout was *"record-breaking"* again. Judges praised builders who *"took your projects outside and told us how it went."*
- [Week 2: Side Hustle winners](https://dev.to/devteam/congrats-to-the-hacktoberfest-open-source-ai-challenge-week-2-side-hustle-winners-2i33). Judges liked *"small, specific, useful tools"* and builders who put the project *"in front of a real first user."* They noted that open models made the business work through low cost, privacy, or *"tuning for a niche that general-purpose APIs miss."*

The Hacktoberfest winner posts do not include per-winner judge commentary. They only embed the winners. The judges' reasoning below therefore comes from their intro paragraphs and from two similar 2026 DEV announcements that do comment on each winner.

**Selected winners:**

| Winner | Idea | What stands out (from the post itself) | Structure |
| --- | --- | --- | --- |
| [Phone calls are the boss fight of living in Japan](https://dev.to/adk_bbx/phone-calls-are-the-boss-fight-of-living-in-japan-1h6h) (Weekend overall) | Voice agent that makes Japanese phone calls for a friend | A specific person and pain point; a "What my friend said" section; a "Bugs I hit" section; ElevenLabs, Render, and Sentry all doing real work | About 2,900 words, video, GitHub link, tags devchallenge/weekendchallenge/hf26challenge/ai |
| [Job hunting became my side hustle... Deis](https://dev.to/muhammadmurtuzahussain/job-hunting-became-my-side-hustle-so-i-built-deis-gemma-4-tinder-for-jobs-swipe-right-gemma-3jcm) (Week 2 overall) | Swipe-to-apply job tool with Gemma 4 tailoring CVs | Sections titled "Gemma judges, code guarantees", "The bug I shipped and fixed", "My First User", and an agent session | About 3,600 words, video, agent session |
| [I Distilled a 397B Model Into a 4B One for $1.60...](https://dev.to/soumyadeepdey/i-distilled-a-397b-model-into-a-4b-one-for-160-it-now-catches-28-of-33-park-alerts-that-should-bic) (Week 1 Tinker) | Distilled model that flags park alerts | Cost and accuracy numbers in the headline (the before/after result Tinker asks for), plus "Results" and "What went wrong" sections | About 4,800 words, 26 reactions, GitHub link, agent session |
| [I stopped asking AI to count. Now it catches 95.6%...](https://dev.to/heet_ranpura/i-stopped-asking-ai-to-count-now-it-catches-956-of-the-mistakes-in-crochet-patterns-on-a-laptop-1el0) (Week 2 Tinker) | Crochet-pattern checker | *"The one rule: the model never counts"* (deterministic code does the counting); "Where it still fails (measured, not hidden)" | About 3,800 words, video, GitHub link |
| [We Searched eBay for 237 Recalled Products...](https://dev.to/dronzer2code/we-searched-ebay-for-237-recalled-products-only-45-of-12562-listings-named-the-model-2efi) (Week 2 SerpApi) | Recall-listing finder | A data-journalism headline; "Scoring it without fooling ourselves"; three partner technologies | About 4,700 words, GitHub link, agent session |
| [LLMs Have No Nose, So We Built One](https://dev.to/k66inthesky/llms-have-no-nose-so-we-built-one-an-ai-nose-on-the-arduino-uno-q-3fhl) (Week 2 Arduino) | Gas sensor plus model on the UNO Q | A physical project with a vivid hook | About 2,200 words, cover image, GitHub link |
| [Kharcha: a 4B model that reads Indian bank SMS...](https://dev.to/coffeeandcommits/kharcha-a-4b-model-that-reads-indian-bank-sms-so-the-money-stays-on-your-laptop-2n8j) (Weekend Backboard) | Local finance parser | The privacy reason for open models is the headline | About 1,800 words, video, 39 reactions |

**Aggregate across 51 Hacktoberfest winners (Weekend, Week 1, Week 2).** The Week 1 overall winner returned a 404 from the API and is excluded. Data was fetched from the [DEV API](https://dev.to/api/articles) for each post linked in the three winner announcements.
- **Length:** median about 2,280 words (range 1,060 to 4,980).
- **Reactions:** median 5, and several winners had 0 or 1. Popularity is not what wins.
- **Assets:** 42 of 51 link to GitHub, 28 embed a video or GIF, 30 have a cover image, and 17 embed or link an agent session.
- **Titles:** 34 use a "Name: what it does" colon pattern, 30 are first person (I, my, we), and 18 contain a number.
- **Sections beyond the template:** 23 have a section on what went wrong, bugs, or limits; 17 have a first-user or reaction section; 14 have a results or eval section.

**Similar 2026 DEV announcements with per-winner judge comments:**
- [Sanity Challenge winners](https://dev.to/devteam/congrats-to-the-sanity-challenge-winners-1140) (Oct 22). Clockwrit won for an eval scoring *"30/30, against 22/30 for the same model with no tools and 16/30 for keyword search."* Clearance Desk followed the rule *"the model finds and explains while deterministic code judges."* A groundwater agent had an offline mode, and its builder found inconsistencies in source papers and contacted the authors. Judges also praised posts that *"published the rounds they lost"* and *"wrote down every wrong turn."*
- [Weekend Challenge: Generosity Edition winners](https://dev.to/devteam/congrats-to-the-dev-weekend-challenge-generosity-edition-winners-2mmg) (Oct 1). Keepalive analysed 579,178 nonprofits' tax returns and *"reframed our idea of charity."* For ElevenLabs, judges said *"The voice is not a feature bolted on the side, it is the entire product."* For Snowflake, it *"does real work here rather than sitting underneath as storage."*

## Current submissions & saturation map

**Source and method.** Entries were collected from [https://dev.to/api/articles/latest?tag=hf26challenge](https://dev.to/api/articles/latest?tag=hf26challenge) for posts published after Oct 26 16:00 UTC: 429 posts. I fetched 392 bodies, and 355 contain the Week 4 template line or a Week 4 reference.

**Numbers:**
- Median length is 746 words, and 187 entries are under 800 words.
- 44 left the template placeholder comments in.
- 62 embed an agent session, 47 include a video link, and 252 link GitHub.
- Models mentioned: Ollama 200, Gemma 142, Whisper 72, Qwen 70, Llama about 63, closed APIs (OpenAI or Gemini API) about 47.

**Sample of current entries.** Reactions and comments as of Oct 28.

| Title | Idea | React/Com |
| --- | --- | --- |
| [EchoVault — Preserving Living Memories with Air-Gapped... AI](https://dev.to/arnab825/echovault-preserving-living-memories-with-air-gapped-grounded-open-source-ai-4gfe) | Offline family-memory archive | 7/0 |
| [The Rootkit Exorcist](https://dev.to/data_secchronicles/the-rootkit-exorcist-summoning-local-ai-to-investigate-suspicious-scripts-an1) | Local LLM triages suspicious scripts | 7/0 |
| [What Happens When You Put an AI in a Ghost Story?](https://dev.to/scs0209/what-happens-when-you-put-an-ai-in-a-ghost-story-32h2) | Gemma plays four haunted objects, with code checking each reply (author is a past winner) | 6/0 |
| [RepoGhost](https://dev.to/egbutaify2ui/repoghost-bringing-quiet-open-source-projects-back-to-life-with-gemma-4-3oii) | Revives quiet GitHub repos | 6/0 |
| [PHANTOM - The Ghost in Your Codebase](https://dev.to/dr5t/phantom-the-ghost-in-your-codebase-d2k) | Haunted code analysis | 6/0 |
| [My AI was in the cloud. I brought it home.](https://dev.to/thomasbnt/my-ai-was-in-the-cloud-i-brought-it-home-4hp4) | Moving a cloud assistant to local inference | 5/0 |
| [GhostShell: A Haunted AI Terminal](https://dev.to/dipanshu_vishwakarma/ghostshell-a-haunted-ai-terminal-for-hacktoberfest-2026-33hg) | Haunted terminal (one of many) | 5/0 |
| [I wrote a program that only runs after I die](https://dev.to/anishisbusy/i-wrote-a-program-that-only-runs-after-i-die-53ne) | Dead-man's-switch agent using Auth0 CIBA human approval (author is a two-time past winner) | 5/0 |
| [study Boss Battle](https://dev.to/mkuchchal/tudy-boss-battle-i-turned-my-forgotten-notes-into-a-monster-fight-lmm) | Forgotten notes become a monster fight | 5/0 |
| [Whisper invented a cooking ad over six seconds of silence...](https://dev.to/memeshe/whisper-invented-a-cooking-ad-over-six-seconds-of-silence-so-i-built-a-memorial-book-that-refuses-b56) | Vietnamese memorial book that guards against transcription hallucination | 2/0 |
| [Last Witness: an AI detective for a dead 1999 website](https://dev.to/p0rt/last-witness-an-ai-detective-for-a-dead-1999-website-graded-on-its-ghosts-4bbe) | Internet archaeology with graded evals | 2/0 |
| [I couldn't even read one row... ghost hunter for Oracle](https://dev.to/uptimearchitect/i-couldnt-even-read-one-row-the-session-that-locked-it-was-gone-so-i-built-a-ghost-hunter-for-a99) | Finds orphaned DB lock sessions (author is a past winner) | 2/0 |
| [An ofrenda for the people whose code still runs](https://dev.to/vinimabreu/an-ofrenda-for-the-people-whose-code-still-runs-gemma-4-writes-the-cards-on-my-laptop-and-git-5ea0) | Git-verified memorial cards for code authors | 2/0 |
| [I held a seance for ten dead PyPI packages](https://dev.to/13owen/i-held-a-seance-for-ten-dead-pypi-packages-417b) | Mastra agent over dead packages (author is a past winner) | 0/0 |
| [Revenant: I held a séance for a dead Python library...](https://dev.to/bladeharper_ec7070d6e28be/revenant-i-held-a-seance-for-a-dead-python-library-and-it-came-back-passing-its-tests-43md) | Revived library that passes its tests | 1/0 |
| [The Dead Letter Office](https://dev.to/nightclerk/the-dead-letter-office-write-to-someone-who-died-with-a-gemma-that-never-leaves-your-browser-1k3e) | Letters to the dead, with in-browser WebGPU Gemma | 0/0 |
| [Marigold: an ofrenda made of their own words](https://dev.to/eternity0207/marigold-an-ofrenda-made-of-their-own-words-and-an-ai-that-isnt-allowed-to-speak-for-them-28e4) | Ofrenda where the AI may not speak for the dead | 0/0 |
| [Wayback Séance](https://dev.to/ziwenqingshu/wayback-seance-i-asked-dead-websites-to-tell-their-own-life-stories-and-made-the-ghosts-cite-49cl) | Dead websites narrate their own history, with citations | 0/0 |
| [The Offline Séance: Channeling COBOL Ghosts](https://dev.to/d_teencherry/the-offline-seance-channeling-cobol-ghosts-with-gemma-2b-a2k) | Literal version of the example idea | 1/0 |
| [GitSéance](https://dev.to/fgrandon/gitseance-an-offline-digital-ofrenda-where-local-gemma-summons-deleted-code-and-refuses-to-guess-4hc0) | Git archaeology ofrenda | 0/0 |

**Saturation map.** Counts come from a keyword scan of title plus the first 1,500 characters of the 355 entries. Categories overlap, so the counts sum to more than 355.

| Cluster | Approx. entries | Status |
| --- | --- | --- |
| Haunted terminal / shell / CLI (the page's first example) | ~125 | Very saturated |
| Ofrenda / altar / Día de Muertos memorial (the second example) | ~92 | Very saturated |
| Dead code, git history, abandoned-repo "haunting" | ~86 | Very saturated |
| Séance with a dead language or technology (COBOL, BASIC, PyPI) | ~64 | Saturated |
| Ghost or horror story generator | ~56 | Saturated |
| Family memory / oral history / voice archive | ~39 | Crowded |
| Haunted code-review persona | ~32 | Crowded |
| Games | ~19 | Moderate |
| Security / forensics ("exorcist") | ~17 | Light |
| Old-web / internet archaeology | ~11 | Light |
| Smart-home, sensor, or hardware (the page's fifth example) | ~3 | Nearly empty |

**Repeat winners in the field.** Past winners are competing again this week: anishisbusy, uptimearchitect, 13owen, and scs0209 (see the table above).

## Winning patterns

Each pattern below is backed by the cited evidence.

1. **Lead with a specific human or a specific number, not the technology.** Titles such as "Phone calls are the boss fight of living in Japan" and "Only 45 of 12,562 Listings Named the Model" won. Across 51 winners, 30 titles are first person and 18 contain a number. Losing-looking Week 4 titles are generic product names such as "GhostShell", "Phantom AI", or "AI-Alchemist" with an emoji. ([Weekend winners](https://dev.to/devteam/congrats-to-the-hacktoberfest-weekend-challenge-build-for-a-friend-winners-pgc), [Week 2 winners](https://dev.to/devteam/congrats-to-the-hacktoberfest-open-source-ai-challenge-week-2-side-hustle-winners-2i33))
2. **Let the model explain and let code decide.** Winners say this explicitly: Deis has "Gemma judges, code guarantees", the crochet checker says "the model never counts", and Clearance Desk says *"the model finds and explains while deterministic code judges."* Judges appear to reward guarding against hallucination over raw generation. ([Deis](https://dev.to/muhammadmurtuzahussain/job-hunting-became-my-side-hustle-so-i-built-deis-gemma-4-tinder-for-jobs-swipe-right-gemma-3jcm), [crochet](https://dev.to/heet_ranpura/i-stopped-asking-ai-to-count-now-it-catches-956-of-the-mistakes-in-crochet-patterns-on-a-laptop-1el0), [Sanity winners](https://dev.to/devteam/congrats-to-the-sanity-challenge-winners-1140))
3. **Measure against a baseline, and publish where you lost.** Clockwrit's 30/30 vs 22/30 vs 16/30 and the Tinker winners' before/after numbers are examples. 23 of 51 Hacktoberfest winners have a "what went wrong" section, and Sanity judges praised posts that *"published the rounds they lost."* ([Sanity winners](https://dev.to/devteam/congrats-to-the-sanity-challenge-winners-1140))
4. **Show it landing with a real person.** Week 1 judges valued that builders *"took your projects outside and told us how it went"*. Week 2 judges valued a *"real first user"*. The Week 4 template's optional "The Spirit of It" section asks for exactly this. 17 of 51 winners have such a section. ([Week 1 winners](https://dev.to/devteam/congrats-to-the-hacktoberfest-open-source-ai-challenge-touch-grass-winners-152c), [Week 2 winners](https://dev.to/devteam/congrats-to-the-hacktoberfest-open-source-ai-challenge-week-2-side-hustle-winners-2i33), [challenge page](https://dev.to/challenges/hacktoberfest-week4-2026-10-26))
5. **Make the "why open" answer concrete and essential to the project.** Weekend judges listed *"private data stays at home, tools run without a credit card"*. Week 2 judges cited niche tuning that *"general-purpose APIs miss."* Kharcha put the privacy reason in its headline. A project that works equally well on a closed API scores weakly on Relevance, and about 47 Week 4 entries mention OpenAI or Gemini APIs. ([Weekend winners](https://dev.to/devteam/congrats-to-the-hacktoberfest-weekend-challenge-build-for-a-friend-winners-pgc), [Week 2 winners](https://dev.to/devteam/congrats-to-the-hacktoberfest-open-source-ai-challenge-week-2-side-hustle-winners-2i33))
6. **Partner technology has to carry weight.** Judges wrote that the ElevenLabs voice *"is the entire product"* and that Snowflake *"does real work here rather than sitting underneath as storage."* Tinker explicitly requires a before/after improvement, Sentry requires traces or screenshots, and Ultramarine requires a reported cost. ([Generosity winners](https://dev.to/devteam/congrats-to-the-dev-weekend-challenge-generosity-edition-winners-2mmg), [challenge page](https://dev.to/challenges/hacktoberfest-week4-2026-10-26))
7. **Write long, structured posts with assets.** Winners have a median of about 2,280 words; current Week 4 entries have a median of 746. 42 of 51 winners link GitHub and 28 of 51 include a video or GIF. Writing Quality is weighted most heavily. ([challenge page](https://dev.to/challenges/hacktoberfest-week4-2026-10-26))
8. **Avoid what reads as low effort.** That includes template comments left in the post (44 current entries), no listed prize categories (200 entries), a literal copy of a page example (haunted terminal and ofrenda make up roughly 60% of the field combined), and a generic spooky chatbot or story generator with no evaluation. This pattern is inferred from the saturation data plus the Creativity criterion (*"an original idea, or a fresh take on a familiar problem"*). It is not a judge statement.
9. **Reactions do not decide.** The median winner had 5 reactions, and several had 0. Reactions only break ties. ([contest rules](https://dev.to/page/hacktoberfest-week4-2026-10-26-contest-rules))

### Gaps worth exploiting

These are inferred from the saturation map and the category claim counts:
- **Underused categories.** Tinker (needs a measured fine-tune gain), Arduino UNO Q, Browserbase, Auth0, Ultramarine, SerpApi, and Tiger Data each had about 0 to 2 claimants on Oct 28. TabPFN, DigitalOcean, Temporal, and Mastra had 3 to 5.
- **The theme examples nobody is using.** Sensor-log or smart-home ghost stories had about 3 entries, and old-web or internet archaeology had about 11.
- **Theme angles with few entries.** Spooky security or forensics (about 17) and "past" data-journalism in the eBay-recall or Keepalive style, such as a haunting dataset with a measurable finding (no clear cluster found).
- **Gemma.** Gemma is the default model for the whole field (82 claims). Use it if it helps, but don't count on the Gemma category.

## Open questions

- **Winning two prizes is impossible in Week 4 under the rules.** If the user's goal of "at least 2 tracks" means two prizes, it cannot be met in this contest. Confirm whether the goal is really "enter multiple categories to maximize the chance of one win."
- Judge identities and numeric weights are not published.
- Whether categories claimed only via "Use of Partner Technology" are judged by partner representatives is not stated. **Unverified.**
- Week 3 (Slow and Steady) winners were not yet posted as of Oct 28, so Week 3 patterns are missing.
- The Week 1 overall winner post ([link from the announcement](https://dev.to/mike_kim_692aa79c288bfed8/paper-trail-gemma-writes-your-walk-a-field-card-then-the-screen-goes-away-3mf4)) returned a 404 from the API, so its structure was not analysed.
- Partner credit amounts and availability at hacktoberfest.com/my/promos were not verified (login required).
- The Arduino category needs physical UNO Q hardware. Whether the user has one is unknown.
- Submission counts are a two-day snapshot. About 37 bodies were not fetched because of API rate limits, so the cluster counts are approximate.

## Sources

- Challenge page: https://dev.to/challenges/hacktoberfest-week4-2026-10-26
- Week 4 contest rules: https://dev.to/page/hacktoberfest-week4-2026-10-26-contest-rules
- General Official Rules: https://dev.to/page/official-hackathon-rules
- HF26 hub: https://dev.to/challenges/hf26
- Week 4 launch post: https://dev.to/devteam/join-the-hacktoberfest-open-source-ai-challenge-ghost-in-the-machine-2850-in-prizes-across-21-3cho
- Series announcement: https://dev.to/devteam/hacktoberfest-2026-dev-challenges-five-challenges-one-prompt-a-new-theme-every-week-1e54
- Weekend winners: https://dev.to/devteam/congrats-to-the-hacktoberfest-weekend-challenge-build-for-a-friend-winners-pgc
- Week 1 winners: https://dev.to/devteam/congrats-to-the-hacktoberfest-open-source-ai-challenge-touch-grass-winners-152c
- Week 2 winners: https://dev.to/devteam/congrats-to-the-hacktoberfest-open-source-ai-challenge-week-2-side-hustle-winners-2i33
- Week 3 challenge: https://dev.to/challenges/hacktoberfest-week3-2026-10-19
- Sanity Challenge winners: https://dev.to/devteam/congrats-to-the-sanity-challenge-winners-1140
- Generosity Edition winners: https://dev.to/devteam/congrats-to-the-dev-weekend-challenge-generosity-edition-winners-2mmg
- DevRelay knowledge, Hacktoberfest: https://devrelay.com/knowledge/hacktoberfest
- DevRelay knowledge, DEV Challenges: https://devrelay.com/knowledge/dev-challenges
- DevRelay knowledge, DEV guidelines: https://devrelay.com/knowledge/dev-guidelines
- DEV AI guidelines: https://dev.to/guidelines-for-ai-assisted-articles-on-dev
- DEV agent rules: https://dev.to/llms.txt
- DEV API feeds used for counts: https://dev.to/api/articles/latest?tag=hf26challenge and https://dev.to/api/articles?username=devteam&per_page=40
- Individual winner and entry posts: linked inline above.

## Category competition (as of 2026-10-28, about 16:40 UTC / 09:40 AM PDT)

**Method.** I re-pulled the feed at [https://dev.to/api/articles/latest?tag=hf26challenge](https://dev.to/api/articles/latest?tag=hf26challenge) (429 posts published after Oct 26 16:00 UTC, the same count as the earlier snapshot), then fetched every missing body from `https://dev.to/api/articles/{id}`, about 1.2 seconds apart. Two IDs returned 404 (deleted or unpublished). 382 bodies reference Week 4 ("Ghost in the Machine" or the Week 4 link). For each one I took only the "Prize Categories" section, with HTML comments stripped so template text doesn't count, and matched sponsor names. Then I **read every hit by hand** for the $200 categories and the thin $100 ones, and removed entries that name a sponsor only to say they are *not* entering. Duplicate posts by the same author count once: the rules judge only an author's first entry ([contest rules](https://dev.to/page/hacktoberfest-week4-2026-10-26-contest-rules)).

**This corrects the earlier table.** Tinker drops from 1 claim to **0** and DigitalOcean from 3 to **0**. The only post that named Tinker, [hauntctl](https://dev.to/jrob1799/hauntctl-i-held-a-seance-for-my-git-history-j1l), says *"Not entering Render, TabPFN, Tinker, Arduino, DigitalOcean"*. The posts that named DigitalOcean say *"I considered claiming DigitalOcean and Render and deliberately did not"* ([post](https://dev.to/cadets_atease/i-found-a-bug-in-this-model-and-i-corrected-it-jae)) and *"I am not entering Render, DigitalOcean or .tech"* ([post](https://dev.to/merouane_flame_56f/a-deleted-file-isnt-gone-its-waiting-to-be-overwritten-22dg)).

### Exact claim counts

These are unique authors with a real (non-negated) claim. 140 of the 382 entries have no prize section at all.

| Category | Prize | Claims | Strong competitors* | Value ÷ strong |
| --- | --- | --- | --- | --- |
| Tinker | $200 | **0** | 0 | no competition |
| DigitalOcean | $200 | **0** | 0 | no competition |
| Arduino UNO Q | $200 | **0** (1 UNO Q project that does not list the category) | 0 | no competition, but **needs hardware** |
| TabPFN | $200 | **5** | 2 | $100 |
| Render | $200 | **19** | 6 | ~$33 |
| Gemma (excluded) | $200 | ~99 by keyword | n/a | n/a |
| SerpApi | $100 | **0** | 0 | no competition |
| Auth0 for AI Agents | $100 | **1** | 1 | $100 |
| Browserbase | $100 | **1** | 1 | $100 |
| Ultramarine | $100 | **1** | 1 | $100 |
| Tiger Data | $100 | **2** | 1 to 2 | $50 to $100 |
| MongoDB Atlas | $100 | 3 | not reviewed | — |
| Backboard | $100 | 3 (incl. two ~250-word posts) | not reviewed | — |
| Temporal | $100 | 4 | not reviewed | — |
| Entire | $100 | 4 | not reviewed | — |
| .tech domain | $100 | 4 | not reviewed | — |
| Sentry Agent Tracing | $100 | 6 | not reviewed | — |
| Mastra | $100 | 6 (one project posted from two accounts) | not reviewed | — |
| ElevenLabs | $100 | 7 to 8 | not reviewed | — |
| GitHub Copilot | $100 | ~10 | not reviewed | — |

\*"Strong" means quality 4 or 5 in my rating below **and** real use of the sponsor technology. The quality ratings are my judgment against the published criteria. They are not judge statements.

**One-prize cap effect.** The single Auth0 and Ultramarine claimant, and one of the two Tiger Data claimants, is the same person ([anishisbusy](https://dev.to/anishisbusy/i-wrote-a-program-that-only-runs-after-i-die-53ne), a two-time past winner). That person can win at most one prize ([contest rules](https://dev.to/page/hacktoberfest-week4-2026-10-26-contest-rules)). How judges resolve this is **unverified**, but at least two of those three $100 prizes should go to someone else.

### What each $200 sponsor asks for (exact text, from the [challenge page](https://dev.to/challenges/hacktoberfest-week4-2026-10-26))

- **Render:** *"Use Render as your project's AI runtime, to host an agent's front end, or to run Hermes or OpenClaw."*
- **TabPFN:** *"Use TabPFN, Prior Labs' tabular foundation model, to forecast, predict, classify, or spot anomalies from historical data like a CSV."* Prior Labs recommends TabPFN-3.5 (*"open-weight and free to use once you sign the non-commercial license at platform.priorlabs.ai"*). The stated preference: *"Prior Labs favors projects that use TabPFN inside a wider prediction agent (with or without the MCP server)."*
- **Tinker:** *"Use Thinking Machines' Tinker to fine-tune a model for a specific task, and show a clear improvement in performance, latency, or cost over a baseline."*
- **Arduino:** *"Build with an Arduino UNO Q: run a model on the board, build a physical agent that senses and acts, or optimize a model for it with Qualcomm AI Hub."*
- **DigitalOcean:** *"Build or deploy your project on DigitalOcean: host your app or agent, run an open-weight model on a GPU Droplet (1-Click Models make this quick), or build an agent on the Gradient AI Platform."*
- **Thin $100 ones:** SerpApi: *"Give an agent live web search, ground a RAG app in fresh results, or track news for an open-source project."* Auth0: *"sign users in to an agent, call tools on a user's behalf with Token Vault, ask a person to approve a risky action..., or limit what a RAG pipeline can retrieve with fine-grained authorization."* Browserbase: *"drive a live site end to end using Stagehand's SDK, pull the context an open-weight model reasons over, or turn a one-off agent run into a repeatable workflow."* Ultramarine: *"Call it with the OpenAI or Anthropic SDKs, and say what your run actually cost."* Tiger Data: *"Store embeddings with pgvector, run hybrid keyword and vector search for an agent, or let an agent manage a database through Tiger MCP."*

### Credits and free tiers

- **Hacktoberfest promos.** The challenge page says *"Several partners are giving participants credits and promo codes, including Tinker, Render, Backboard, and a free .tech domain"* at hacktoberfest.com/my/promos. Ultramarine gives *"$5 of free credit"* ([challenge page](https://dev.to/challenges/hacktoberfest-week4-2026-10-26)). **The Tinker and Render promo amounts are unverified** because the page needs a login. The [DevRelay Hacktoberfest guide](https://devrelay.com/knowledge/hacktoberfest) doesn't list them either.
- **Tinker** (pricing as of Oct 19, 2026): usage-based. Qwen3-8B costs $0.195 prefill, $0.60 sample, and $0.44 train per 1M tokens. Qwen3.5-4B costs $0.33, $1.005, and $0.737. GPT-OSS-20B costs $0.18, $0.45, and $0.396. Checkpoint storage is $0.10 per GB per month. The pricing page lists **no free tier** ([Tinker pricing](https://thinkingmachines.ai/tinker/pricing/)). Third-party sites report $150 in starter credits ([everydev](https://www.everydev.ai/tools/tinker), [Beam](https://www.beam.cloud/blog/tinker-model-pricing)); this is **unverified**. For scale, a Week 1 Tinker winner distilled a model *"for $1.60"* ([post](https://dev.to/soumyadeepdey/i-distilled-a-397b-model-into-a-4b-one-for-160-it-now-catches-28-of-33-park-alerts-that-should-bic)).
- **DigitalOcean:** new customers get *"free credit up to $200"* to use within 60 days. A valid credit card is required, and the offer is for people who have never been paying customers ([DO free trial](https://try.digitalocean.com/freetrialoffer)). DigitalOcean is also Hacktoberfest's presenting partner, and connecting a DO account earns a sticker ([DevRelay Hacktoberfest guide](https://devrelay.com/knowledge/hacktoberfest)). I did not verify Gradient AI Platform pricing.
- **Render:** each workspace gets 750 free instance hours a month, and free web services spin down after 15 minutes without traffic ([Render docs](https://render.com/docs/free)). Several entrants report 30 to 60 second cold starts (for example [Revenant](https://dev.to/bladeharper_ec7070d6e28be/revenant-i-held-a-seance-for-a-dead-python-library-and-it-came-back-passing-its-tests-43md)).
- **TabPFN:** the TabPFN-3.5 weights are under a non-commercial license. Prior Labs' API has a free tier with *"free daily & monthly limits"* running TabPFN-3-Plus with Thinking mode ([Prior Labs pricing](https://priorlabs.ai/pricing), [gated-model docs](https://docs.priorlabs.ai/how-to-access-gated-models)). Whether the free API serves 3.5 itself is **unverified**. Running locally on CPU works for small CSVs; [Titanic Séance](https://dev.to/khushi886987/titanic-seance-ask-the-891-passengers-what-the-night-would-have-done-to-you-5c5j) fit it on Kaggle.
- **Arduino:** you need a UNO Q board. Online, the only Hacktoberfest route to one is the Completionist raffle ([DevRelay Hacktoberfest guide](https://devrelay.com/knowledge/hacktoberfest)), which won't arrive in time.

### Competitors: TabPFN (5)

| Entry | Idea | Real TabPFN use? | Words* | Demo / repo | Quality |
| --- | --- | --- | --- | --- | --- |
| [Titanic Séance](https://dev.to/khushi886987/titanic-seance-ask-the-891-passengers-what-the-night-would-have-done-to-you-5c5j) | Enter who you'd have been in 1912. TabPFN-3.5 predicts survival, then Gemma voices a real passenger. | **Yes.** 5-fold CV against TabPFN v2, logistic regression, and a "women survive" rule (accuracy 0.825, AUC 0.857). | ~1,160 | Live on Render / GitHub embed | **4.** Measured and honest, but uses the Kaggle Titanic set (a cliché) and no agent around TabPFN |
| [MergeMeter](https://dev.to/rostyslavdzhohola/mergemeter-the-ghosts-of-closed-prs-predict-which-open-ones-will-merge-1n0o) | The "ghosts" of a repo's 300 closed PRs predict whether open PRs will merge. | **Yes.** On 8 repos with 5-fold CV, TabPFN beats logistic regression on 7 (AUC 0.853 vs 0.824), with an EVAL.md. | ~655 | Video / repo / session | **4 technically, 3 overall.** Thin write-up, weak spooky angle |
| [GitGeist](https://dev.to/ravi_jaipal_/gitgeist-the-ghost-in-the-machine-15g3) (posted twice) | TabPFN "haunting forecaster" over git telemetry, with Gemma explanations | Claimed. No numbers or evaluation shown. | ~1,300 | No live demo / repo | **2.** Generic, duplicate post |
| [NecroGit Enterprise](https://dev.to/kunalchoudhary/necrogit-enterprise-autonomous-codebase-exorcist-zombie-branch-necromancer-4fi3) | TabPFN-3.5 classifies dead code and zombie branches | Claimed. No evaluation. The anecdote reads as fictional, so the use is **unverified**. | ~1,400 | No live demo / repo | **2** |
| [PhantasmLocal](https://dev.to/riyadhami13/ghost-in-the-machine-where-90s-retro-horror-meets-the-digital-ofrenda-3nd4) | Retro-horror terminal plus ofrenda | **No.** The post itself calls it *"a simulated TabPFN"* engine. | ~480 | Live / repo | **1** |

\*Word counts are of the raw markdown, so they include code and embeds, and are approximate.

**Gap:** no TabPFN entrant does what Prior Labs says it favors, *"TabPFN inside a wider prediction agent"*. None uses Halloween or real-world risk data.

### Competitors: Render (19)

Use strength: **AI** means Render runs the model or agent. **Host** means a deployed front end or API. **Blueprint** means only a `render.yaml` with no live link.

| Entry | Idea | Render use | Words | Demo / repo | Quality |
| --- | --- | --- | --- | --- | --- |
| [What Happens When You Put an AI in a Ghost Story?](https://dev.to/scs0209/what-happens-when-you-put-an-ai-in-a-ghost-story-32h2) | 3D haunted house; Gemma voices objects behind a code guardrail (leaks fell from 8.6% to 0 of 478) | **AI.** A Docker service with Gemma E4B, health check, cache, rate limit, and queue | ~2,900 | Video, live / repo, session | **5** (past winner) |
| [Revenant](https://dev.to/bladeharper_ec7070d6e28be/revenant-i-held-a-seance-for-a-dead-python-library-and-it-came-back-passing-its-tests-43md) | A dead Python library speaks from its own history and is revived until its tests pass | Host plus a verified live cited answer | ~2,900 | Live / repo, session | **4 to 5** |
| [My AI was in the cloud. I brought it home.](https://dev.to/thomasbnt/my-ai-was-in-the-cloud-i-brought-it-home-4hp4) | OpenClaw agent on a home NAS | Host (static front end). It does use OpenClaw, which Render names. | ~1,300 | Live / repo | **4** |
| [I left Whisper alone in an empty room](https://dev.to/abjt01/i-left-whisper-alone-in-an-empty-room-it-started-saying-peoples-names-3pfm) | Spirit box made from Whisper hallucinating on silence | Host (static, cross-origin isolation headers, CI-gated deploy) | ~1,570 | Video, live / no repo link detected | **4** |
| [Titanic Séance](https://dev.to/khushi886987/titanic-seance-ask-the-891-passengers-what-the-night-would-have-done-to-you-5c5j) | See TabPFN above | Host (whole app plus Gemma API calls) | ~1,160 | Live / repo | **4** |
| [Marigold (eternity0207)](https://dev.to/eternity0207/marigold-an-ofrenda-made-of-their-own-words-and-an-ai-that-isnt-allowed-to-speak-for-them-28e4) | Ofrenda built from a loved one's chat messages, with a checked in-browser Gemma | Host (static plus headers) | ~2,170 | Live / no repo link detected | **4** |
| [ZEMNE](https://dev.to/9jadevo/zemne-distance-shouldnt-erase-participation-in-remembrance-5699) | Virtual memorial hall where approved tributes are synthesized by Gemma | Host plus an inference job runtime | ~1,800 | Video, live / repo | 3 to 4 |
| [Afterlight](https://dev.to/faraz_s_0a6e70a4bbdc6622/afterlight-a-haunted-museum-where-medical-history-has-to-show-its-sources-24b4) | Haunted museum of medical history that must cite sources | Host | ~1,700 | Live / repo | 3 to 4 |
| [Ofrenda (joegeorge022)](https://dev.to/joegeorge022/ofrenda-a-ghost-that-only-knows-what-you-tell-it-2k4k) | Local memory altar with a citation gate | Host | ~1,540 | Live / repo | 3 |
| [RepoGhost](https://dev.to/egbutaify2ui/repoghost-bringing-quiet-open-source-projects-back-to-life-with-gemma-4-3oii) | Question a GitHub profile | Host | ~1,220 | Live / repo | 3 |
| [bhoot.sh](https://dev.to/parth_kulkarni_f56a656693/bhootsh-i-put-the-ghost-of-a-frustrated-indian-senior-dev-on-my-desktop-100-local-with-gemma-2-17i2) | Desktop "senior dev ghost" that roasts you | Host (telemetry dashboard, not the AI) | ~1,680 | Video, live / repo | 3 |
| [GitSéance (fgrandon)](https://dev.to/fgrandon/gitseance-an-offline-digital-ofrenda-where-local-gemma-summons-deleted-code-and-refuses-to-guess-4hc0) (posted twice) | Git ofrenda for deleted code | Host (static) | ~2,680 | Live / repo | 2 to 3 |
| [OfrendaViva](https://dev.to/premsai5142/ofrendaviva-a-local-first-dia-de-los-muertos-altar-ghost-in-the-machine-seance-with-1fgj) | Offline altar plus séance | Blueprint | ~1,510 | No live / repo | 2 |
| [GitGeist](https://dev.to/ravi_jaipal_/gitgeist-the-ghost-in-the-machine-15g3) | See TabPFN above | Blueprint | ~1,300 | No live / repo | 2 |
| [Git Séance (meganeshpatel404)](https://dev.to/meganeshpatel404/git-seance-your-code-forgot-why-git-remembers-1il9) | Git-history Q&A | Heading only, no description | ~650 | No live / repo | 2 |
| [GhostCommit](https://dev.to/anushka_sharma_df05737b55/ghostcommit-find-what-haunts-your-code-g4c) | Haunted code review | Host | ~550 | Live / repo | 2 |
| [PhantomTerminal AI](https://dev.to/dien/phantomterminal-ai-ghost-in-the-machine-code-seances-dia-de-los-muertos-altar-2b63) | Code séance plus altar | Host (gateway on the free tier) | ~750 | Live / repo | 2 |
| [Lazy](https://dev.to/nareshkumawatstar/submit-to-the-week-4-dev-challenge-30h1) (title left as "Submit to the week 4 DEV Challenge") | File organizer ghost | Blueprint *"designed to"* | ~1,000 | Live / repo | 1 to 2 |
| [GhostShell AI](https://dev.to/ro_bit07/ghostshell-ai-the-ghost-that-guards-youre-code-55kh) | Terminal command explainer | Claimed *"if the deployed implementation meets the challenge requirements"* | ~510 | None / none | 1 |

### Competitors: Tinker, DigitalOcean, Arduino (0 claims each)

- **Tinker:** none.
- **DigitalOcean:** none.
- **Arduino:** none claimed. [SlothMesh](https://dev.to/yashwan7/rest-mesh-arduinouno-q-and-open-weight-models-5798) (~770 words, video, repo, session) builds a TinyML network monitor around the UNO Q with Gemma 4 E4B, but doesn't list the category. Quality 2 to 3: a generic network monitor with a thin spooky angle. **Flag: the user likely lacks the hardware.**

### Competitors: thinnest $100 categories

| Category | Entry | Use | Quality |
| --- | --- | --- | --- |
| SerpApi | none | — | — |
| Auth0 | [I wrote a program that only runs after I die](https://dev.to/anishisbusy/i-wrote-a-program-that-only-runs-after-i-die-53ne) (~2,200 words, video, live, repo, session) | Real: sign-in, CIBA with Guardian push approval, and FGA gating every question. *"0 leaks in 126 answers."* | **5** |
| Ultramarine | same post | `ultramarine-1-flash` writes the family handbook | 5 |
| Tiger Data | same post; [Marigold (tharun634)](https://dev.to/tharun634/marigold-an-altar-that-will-not-invent-the-dead-9i3) (~1,380 words, video, repo, session) | The first uses hybrid BM25 and DiskANN with reciprocal rank fusion. Marigold uses halfvec HNSW plus `pg_textsearch` BM25 fusion and a hypertable. | 5; 3 to 4 |
| Browserbase | [Revenant](https://dev.to/bladeharper_ec7070d6e28be/revenant-i-held-a-seance-for-a-dead-python-library-and-it-came-back-passing-its-tests-43md) | Collects dead docs pages into the ghost's memory | 4 |

### Ranking: prize value ÷ strong competitors, with feasibility for a solo TS/Python dev with 3 days left

1. **Tinker ($200, 0 claims).** Most open. It requires a fine-tune *plus* a measured before/after against a baseline, which the user can do in Python (LoRA on Qwen3-8B or Qwen3.5-4B, a few hundred labeled examples, a held-out evaluation). Cost should be a few dollars at the listed prices, but it is **paid**: no free tier is listed, and the promo amount is unverified. Risk: the dataset and evaluation take a full day, so it's tight but feasible.
2. **DigitalOcean ($200, 0 claims).** Easiest to qualify for, but bare hosting may read as weak "meaningful use". It's stronger if the open-weight model is served from DO (GPU Droplet or Gradient). Requires a card. Feasible in under a day. DigitalOcean is the presenting partner, so late claimants are likely.
3. **TabPFN ($200, 2 strong).** A real gap exists: nobody uses TabPFN inside an agent, as Prior Labs prefers, and nobody uses real-world risk data. Feasible in about a day using the local weights or the free API.
4. **SerpApi ($100, 0 claims).** Free tier not verified. Easy to add to an agent.
5. **Browserbase, Auth0, Ultramarine ($100, 1 strong each).** One strong entrant each, and the cap means anishisbusy can take only one.
6. **Render ($200, 6 strong).** About $33 per strong rival. Only worth claiming as a bonus.
7. **Arduino ($200, 0 claims).** Not feasible without the board.

**Stacking.** One entry can be judged in every category it meaningfully uses ([contest rules](https://dev.to/page/hacktoberfest-week4-2026-10-26-contest-rules)). A single project that fine-tunes on Tinker with a measured gain, uses TabPFN for the tabular prediction step, and serves the model on DigitalOcean would be in contention for three $200 categories that currently have 0, 2, and 0 strong rivals.

**Caveats.** This is a snapshot with about 3.5 days left, and late entries are typical. The matching covers only the prize section, so an entrant who names a sponsor only in the body is missed. 2 posts were unreadable (404). Whether a category with no valid entries gets awarded at all is **unverified**.

## Real Halloween problems (sourced)

**Competition check.** I searched the titles and bodies of all 382 Week 4 entries ([feed](https://dev.to/api/articles/latest?tag=hf26challenge)) for each topic's keywords. Matches turned out to be metaphors (for example "haunted house") or unrelated uses (network "traffic", job scams). **No Week 4 entry addresses any of the real-world problems below.** The field is almost entirely haunted terminals, ofrendas, git séances, and story generators (see the saturation map above). Older or secondary sources are labelled as such.

| # | Problem | Evidence (source) | Week 4 entries addressing it | Natural partner fit |
| --- | --- | --- | --- | --- |
| 1 | **Child pedestrian deaths on Halloween evening** | A JAMA Pediatrics study of 1975–2016 US data found 43% higher odds of pedestrian death on Halloween evening, and a 10-fold increase for ages 4 to 8 ([JAMA Pediatrics abstract](https://jamanetwork.com/journals/jamapediatrics/article-abstract/2725859), [UBC release](https://advancinghealth.ubc.ca/research-in-action/press-release-pedestrian-fatalities-increase-on-halloween-particularly-among-children-2)). A MoneyGeek analysis of 2010–2024 counts 45 children killed walking on Oct 31, 24 of them between 6 and 9 PM ([MoneyGeek](https://www.moneygeek.com/living/driving/halloween-pedestrian-deaths/)). | 0 | **TabPFN** on public NHTSA FARS crash CSVs (risk by hour, light, road type) inside an agent that rates a family's trick-or-treat route. Deploy on DigitalOcean. |
| 2 | **Drunk driving on Halloween night** | NHTSA: 44% of people killed on Halloween night in 2012–2016 were in crashes involving a drunk driver. This is a secondary citation; the [DOT advisory](https://www.transportation.gov/briefing-room/safety-advisory-celebrating-halloween) returned 403 to my fetcher, so **unverified at the primary source**. | 0 | TabPFN on FARS; SerpApi for local ride and road-closure news |
| 3 | **Food allergies at trick-or-treat** | FARE's Teal Pumpkin Project signals non-food treats ([FARE](https://www.foodallergy.org/fare-blog/leading-food-allergy-organizations-join-support-teal-pumpkin-project)). The "1 in 13 children" figure is attributed to FARE in news coverage ([Nemours](https://blog.nemours.org/2016/10/allergy-halloween-go-teal/)). **Not checked at FARE's primary page.** | 0 | **Tinker**: fine-tune a small model to extract allergens and "may contain" warnings from candy label text or photos, measured against the base model |
| 4 | **Fun-size candy differs from full size** | Laffy Taffy: the large size lists egg, while the fun size drops egg and adds soy ([NBC Connecticut](https://www.nbcconnecticut.com/news/national-international/fun-size-candy-bigger-concern-kids-food-allergies/3781015/)). A full-size Hershey bar has no advisory, while the snack size warns of shared almond equipment ([Kids With Food Allergies](https://community.kidswithfoodallergies.org/blog/459827228912935071)). The AAAAI warns fun-size candy *"may contain different ingredients"* ([AAAAI](https://www.aaaai.org/tools-for-the-public/conditions-library/allergies/avoid-the-danger-of-anaphylaxis-this-halloween)). See also [Food Allergy Canada](https://foodallergycanada.ca/mythbuster-do-trick-or-treat-sized-candies-chocolates-always-have-the-same-ingredient-list-as-the-full-sized-versions/). | 0 | **Tinker** (label-reading fine-tune with a measured gain); Browserbase or SerpApi to fetch current manufacturer labels |
| 5 | **THC edibles that look like candy** | The FDA reported 10,448 poison-center exposure cases for THC edibles from Jan 2021 to May 2022; 77% of patients were 19 or younger ([FDA](https://www.fda.gov/food/alerts-advisories-safety-information/fda-warns-consumers-about-accidental-ingestion-children-food-products-containing-thc)). The DEA says incidents of drugs being handed out on Halloween are rare ([DEA](https://dea.gov/es/node/203666)). | 0 (3 keyword hits are unrelated) | Tinker, using a vision model such as Nemotron-VL listed on [Tinker pricing](https://thinkingmachines.ai/tinker/pricing/): copycat-package detection versus the base model. Handle the fear-mongering risk honestly. |
| 6 | **Decorative contact lens eye injuries** | The FDA says decorative lenses are medical devices that need a prescription, and lists Halloween stores and novelty shops as places not to buy them ([FDA](https://www.fda.gov/medical-devices/contact-lenses/decorative-contact-lenses-halloween-and-more), [FDA consumer update](https://www.fda.gov/consumers/consumer-updates/colored-and-decorative-contact-lenses-prescription-must)). The FDA cites corneal ulcers and infections that can cause blindness. | 0 | Browserbase or SerpApi agent that checks whether a lens seller requires a prescription |
| 7 | **Pumpkin carving and Halloween ER injuries** | About 3,200 Halloween-related ER injuries a year in 2020–2023, 55% from pumpkin carving (CPSC estimates via [AAOS](https://www.aaos.org/aaos-home/newsroom/press-releases/avoid-injuries-halloween/)). For 2018, CPSC reported 44% ([CPSC infographic](https://www.cpsc.gov/s3fs-public/Halloween%20injury%20infographic%202019FINAL%20_0.pdf)). | 0 | Weak AI fit |
| 8 | **Costume flammability and burns** | The Flammable Fabrics Act requires retail costumes to be flame-resistant; CPSC advises a "Flame Resistant" label and flameless lights in jack-o'-lanterns ([CPSC 2013](https://www.cpsc.gov/Newsroom/News-Releases/2013/Halloween-Safety-Tips-for-Selecting-Costumes-and-Decor), [CPSC 2010](https://www.cpsc.gov/Newsroom/News-Releases/2010/CPSC-Warns-Dont-Be-Haunted-by-Burn-and-Laceration-Hazards-this-Halloween)) | 0 | Browserbase to check product listings against CPSC recalls |
| 9 | **Decoration and candle home fires** | NFPA estimates about 835 home fires a year started by decorations in 2020–2024; nearly half had decorations too close to heat, and about a third were started by candles (via [Fire & Safety Journal Americas](https://fireandsafetyjournalamericas.com/halloween-fire-safety-tips-shared-by-nfpa-amid-home-decoration-risks/); **secondary**). This also bears on ofrenda candles. | 0 | Weak; could be an ofrenda candle-safety checker |
| 10 | **Pet poisoning from chocolate and xylitol** | The ASPCA warns about Halloween treats ([ASPCA](https://www.aspca.org/about-us/press-releases/aspca-takes-trick-out-halloween-treats)). Poison-control calls rise about 10% in Halloween week ([NBC News](https://www.nbcnews.com/health/health-news/halloween-hazard-xylitol-laced-treats-could-kill-your-dog-flna1c6436756)) or about 12% ([Farmers' Almanac](https://www.farmersalmanac.com/halloween-pet-safety)); both are **secondary and older**. Over 2,500 xylitol calls in 2010 (NBC). | 0 | **Tinker**: fine-tune a model to map an ingredient list plus pet weight to a "call poison control" triage, measured against the base model. Don't present dosing as medical advice. |
| 11 | **Pets lost on Halloween** | San Diego Humane Society says shelters see *"a substantial increase in lost pets around Halloween"* (qualitative, no count) ([SDHS](https://www.sdhumane.org/about-us/news-center/stories/free-microchips-during-october.html)). | 0 | Weak data; image matching with an open vision model |
| 12 | **Fake online costume and décor stores** | BBB Scam Tracker reports of costumes that never arrive, stolen reviews, and impostor sites ([WMBF 2025](https://www.wmbfnews.com/2025/10/27/tricks-treats-traps-bbb-shares-tips-smart-scam-free-halloween-shopping/), [WIBW 2025](https://www.wibw.com/2025/10/16/scammers-ripping-off-people-search-halloween-costumes-decor/)) | 0 (one job-scam entry, [Offer lens](https://dev.to/api/articles/4930103), is a different domain) | **Browserbase** (inspect the live store) plus **SerpApi** (search "name + scam"); TabPFN on site features; Tinker classifier |
| 13 | **Halloween vandalism** | HLDI: Halloween averaged 1,253 vehicle vandalism claims a day in 2008–2012, against an overall daily average of 692 ([IIHS/HLDI](https://www.iihs.org/news/detail/vehicle-vandalism-peaks-on-halloween-with-nearly-twice-as-many-claims-as-usual)). Aviva (UK, 2021–2024) reports malicious-damage claims up 19% and theft up 25% in Oct–Nov ([Insurance Business](https://www.insurancebusinessmag.com/uk/news/claims/the-halloween-season-also-comes-with-a-scary-rise-in-insurance-claims-553692.aspx)). | 0 | TabPFN, but there's no open per-address data |
| 14 | **Autistic and sensory-sensitive trick-or-treaters** | The blue-bucket signal divides parents; some suggest "sensory-safe" houses or hours instead ([WPTV](https://www.wptv.com/news/national/why-blue-pumpkin-candy-buckets-are-dividing-the-autism-community), [ABC 33/40](https://abc3340.com/news/nation-world/parents-concerned-blue-buckets-may-single-out-trick-or-treaters-with-autism)). No survey numbers found. | 0 | A sensory-friendly route or house map; DigitalOcean or Render hosting; weak for the $200 categories |
| 15 | **Pumpkin food waste (UK)** | About 18,000 tonnes of pumpkin are binned each Halloween ([Worcestershire CC](https://cms.worcestershire.gov.uk/news/halloween-horror-18000-tonnes-pumpkins-wasted-every-year)). Hubbub estimates range from 15 million pumpkins uneaten (2016) to up to 22 million binned of 39.9 million bought (date unclear) ([Hubbub 2016](https://issuu.com/hubbubuk/docs/hubbub_2018.11.23._pumpkin_rescue_p), [Hubbub 2024 results](https://issuu.com/hubbubuk/docs/eat_your_pumpkin_2024_campaign_results)). | 0 | Tinker fine-tune for leftover-pumpkin recipes (weak to measure) |
| 16 | **How much candy to buy and how many trick-or-treaters to expect** | NRF projects record spending of $13.5B in 2026, $4.1B of it on candy ([NRF 2026](https://nrf.com/media-center/press-releases/nrf-halloween-survey-shows-consumer-spending-expected-to-reach-13-5-billion); 2025 was $13.1B, [NRF 2025](https://nrf.com/media-center/press-releases/nrf-consumer-survey-finds-halloween-spending-to-reach-record-13-1-billion)). Nextdoor 2024: 62% hand out candy, and 46% of trick-or-treating happens between 6 and 7 PM ([Nextdoor](https://business.nextdoor.com/en-us/blog/halloween-2024-insights)). No public headcount dataset exists. | 0 | **TabPFN** forecast of trick-or-treater counts from a household's past-year logs, weather, and weekday. Data is scarce, so this is weak for judges. |
| 17 | **Haunted attraction safety** | FDNY closed a Queens home haunted house as a *"death trap"*; at least five people sued over injuries on a slide ([NBC News](https://www.nbcnews.com/news/us-news/death-trap-queens-haunted-house-sued-injuries-alleged-safety-hazards-rcna176530)). No systematic injury data found. | 0 (13 "haunted house" hits are metaphors) | Weak AI fit |
| 18 | **Día de los Muertos: cempasúchil cost and supply** | Guadalajara bunches are estimated at 60 to 120 pesos for 2026 ([Azteca Jalisco](https://www.aztecajalisco.com/noticias-jalisco-local/cempasuchil-en-guadalajara-este-seria-el-precio-del-ramo-para-dia-de-muertos-2026/)). In 2025, rain flooded fields and pushed prices up in Campeche ([Por Esto](https://www.poresto.com/campeche/ciudad-carmen/2025/10/16/dia-de-muertos-sube-el-precio-del-cempasuchil-por-inundaciones-en-sembradios.html)). US vendors claim sales are down 90% since 2011 ([AOL](https://www.aol.com/d-los-muertos-marigold-flower-192418763.html); vendor claim, **unverified**). | 0 for price or supply (44 entries mention marigolds only as decoration) | TabPFN price forecast; data is thin |

**Not found:** sourced data on Día de los Muertos family-photo problems (such as restoring or digitizing old photos for altars), on Mexican altar-candle fire statistics (the only source looked unreliable), and on lost-pet counts specific to Halloween. The ofrenda cluster (~92 entries) already covers memorial and photo-adjacent ideas.

**Best fits with zero competition:** #1 child pedestrian risk with TabPFN on FARS, #3/#4 allergen label reading with Tinker, #10 pet-toxin triage with Tinker, and #12 fake-store checking with Browserbase and SerpApi. #1 and #3/#4 have the strongest public data for a measured baseline.

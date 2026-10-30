#!/bin/bash
# Paste this whole file as "User data" when creating a DigitalOcean droplet (Ubuntu 24.04, 16 GB RAM).
# Fill in the two Browserbase lines first (or leave them empty to use the droplet's own Chromium).
# About 10 minutes after the droplet starts, the site is live at https://<droplet-ip-with-dashes>.sslip.io
BROWSERBASE_API_KEY=""
BROWSERBASE_PROJECT_ID=""
REPO="https://github.com/ronaksarda/ghost-text.git"
MODEL_URL="https://huggingface.co/Qwen/Qwen3-8B-GGUF/resolve/main/Qwen3-8B-Q4_K_M.gguf"

set -euo pipefail
exec > /var/log/ghost-text-setup.log 2>&1
apt-get update
apt-get install -y docker.io docker-compose-v2 git curl
git clone "$REPO" /opt/ghost-text
cd /opt/ghost-text

IP=$(curl -s http://169.254.169.254/metadata/v1/interfaces/public/0/ipv4/address)
JUDGE_KEY=$(head -c 24 /dev/urandom | base64 | tr -dc 'A-Za-z0-9')
umask 077
cat > .env <<EOF
BROWSERBASE_API_KEY=$BROWSERBASE_API_KEY
BROWSERBASE_PROJECT_ID=$BROWSERBASE_PROJECT_ID
EOF
cat > deploy/.env <<EOF
SITE=${IP//./-}.sslip.io
JUDGE_KEY=$JUDGE_KEY
EOF

mkdir -p deploy/models
curl -fL --retry 5 -o deploy/models/judge.gguf "$MODEL_URL"
cd deploy
docker compose up -d --build
echo "Ghost Text is starting at https://${IP//./-}.sslip.io"

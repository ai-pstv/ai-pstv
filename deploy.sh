#!/usr/bin/env bash
# Build y despliegue del preview en publicidadsegmentadatv.com/ai-web
set -euo pipefail

cd "$(dirname "$0")"

SSH_KEY="$HOME/.ssh/publicidadsegmentada_deploy"
REMOTE_HOST="publicidadsegmentadatv@hl1464.dinaserver.com"
REMOTE_PATH="~/www/ai-web/"

echo "==> Construyendo el sitio (astro build)"
pnpm run build

echo "==> Subiendo dist/ a $REMOTE_HOST:$REMOTE_PATH"
rsync -avz --delete -e "ssh -i $SSH_KEY" dist/ "$REMOTE_HOST:$REMOTE_PATH"

echo "==> Listo: https://publicidadsegmentadatv.com/ai-web/"

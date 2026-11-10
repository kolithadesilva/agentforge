#!/usr/bin/env bash
# AgentForge Skill Installer
# TL;DR: Downloads a skill from AgentForge into your project directory.
# Default target agent: GitHub Copilot (.github/skills/<skill-name>/)

set -e

REPO_ORG="kolithadesilva"
REPO_NAME="agentforge"
BRANCH="main"
RAW_BASE="https://raw.githubusercontent.com/${REPO_ORG}/${REPO_NAME}/${BRANCH}"

SKILL_NAME="$1"
AGENT_TARGET="${2:-copilot}"

if [ -z "$SKILL_NAME" ]; then
  echo "Usage: curl -fsSL <install-url> | bash -s <skill-name> [copilot|antigravity|cursor|claude]"
  echo ""
  echo "Example:"
  echo "  bash install.sh pull-request-security-check copilot"
  exit 1
fi

case "$AGENT_TARGET" in
  copilot)
    DEST_DIR=".github/skills/${SKILL_NAME}"
    ;;
  antigravity)
    DEST_DIR=".agents/skills/${SKILL_NAME}"
    ;;
  cursor)
    DEST_DIR=".cursor/skills/${SKILL_NAME}"
    ;;
  claude)
    DEST_DIR=".claude/skills/${SKILL_NAME}"
    ;;
  *)
    echo "[Error] Unknown agent: '${AGENT_TARGET}'. Supported: copilot, antigravity, cursor, claude."
    exit 1
    ;;
esac

echo "=== AgentForge Skill Installer ==="
echo "Skill:  ${SKILL_NAME}"
echo "Agent:  ${AGENT_TARGET}"
echo "Target: ${DEST_DIR}"
echo ""

# Check local catalog first, then remote
if [ -f "catalog/catalog.json" ]; then
  CATALOG_DATA=$(cat catalog/catalog.json)
else
  CATALOG_URL="${RAW_BASE}/catalog/catalog.json"
  echo "Fetching catalog from ${CATALOG_URL}..."
  CATALOG_DATA=$(curl -fsSL "$CATALOG_URL" 2>/dev/null || true)
fi

if [ -z "$CATALOG_DATA" ]; then
  echo "[Error] Failed to fetch catalog.json from AgentForge."
  exit 1
fi

# Locate skill path
SKILL_PATH=$(python3 -c "
import json, sys
data = json.loads('''$CATALOG_DATA''')
for item in data:
    if item.get('name') == '$SKILL_NAME':
        print(item.get('path'))
        sys.exit(0)
sys.exit(1)
" 2>/dev/null || true)

if [ -z "$SKILL_PATH" ]; then
  echo "[Error] Skill '${SKILL_NAME}' was not found in catalog.json."
  exit 1
fi

mkdir -p "$DEST_DIR"

# Copy local file if available, otherwise curl
if [ -f "${SKILL_PATH}/SKILL.md" ]; then
  cp "${SKILL_PATH}/SKILL.md" "${DEST_DIR}/SKILL.md"
  if [ -d "${SKILL_PATH}/scripts" ]; then
    cp -r "${SKILL_PATH}/scripts" "${DEST_DIR}/"
  fi
else
  SKILL_FILE_URL="${RAW_BASE}/${SKILL_PATH}/SKILL.md"
  echo "Downloading SKILL.md from ${SKILL_FILE_URL}..."
  curl -fsSL "$SKILL_FILE_URL" -o "${DEST_DIR}/SKILL.md"
fi

echo "✔ Installation complete!"
echo "Installed to: ${DEST_DIR}/SKILL.md"
echo "Target Agent: ${AGENT_TARGET}"

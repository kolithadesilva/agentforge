#!/usr/bin/env node

/**
 * AgentForge CLI (ASD-STE100 / TL;DR)
 * Install and list AI agent skills for GitHub Copilot, Antigravity, Cursor, and Claude Code.
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const REPO_ORG = 'kolithadesilva';
const REPO_NAME = 'agentforge';
const BRANCH = 'main';
const RAW_BASE = `https://raw.githubusercontent.com/${REPO_ORG}/${REPO_NAME}/${BRANCH}`;

const AGENT_PATHS = {
  copilot: (name) => `.github/skills/${name}`,
  antigravity: (name) => `.agents/skills/${name}`,
  cursor: (name) => `.cursor/skills/${name}`,
  claude: (name) => `.claude/skills/${name}`,
};

function fetchText(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return fetchText(res.headers.location).then(resolve).catch(reject);
      }
      if (res.statusCode !== 200) {
        return reject(new Error(`HTTP ${res.statusCode} for ${url}`));
      }
      let data = '';
      res.on('data', (chunk) => (data += chunk));
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

async function loadCatalog() {
  const localCatalog = path.resolve(__dirname, '../catalog/catalog.json');
  if (fs.existsSync(localCatalog)) {
    return JSON.parse(fs.readFileSync(localCatalog, 'utf8'));
  }
  const raw = await fetchText(`${RAW_BASE}/catalog/catalog.json`);
  return JSON.parse(raw);
}

async function listSkills() {
  const catalog = await loadCatalog();
  console.log('\n=== Available Agent Skills ===\n');
  catalog.forEach((s) => {
    console.log(`• ${s.name} (${s.sdlc_phase})`);
    console.log(`  Benefit: ${s.observed_benefit}`);
    console.log(`  Agents:  ${s.tested_with ? s.tested_with.join(', ') : 'All'}\n`);
  });
  console.log('To install a skill, run:');
  console.log('  npx agentforge add <skill-name> [--agent copilot]\n');
}

async function addSkill(skillName, targetAgent = 'copilot') {
  if (!skillName) {
    console.error('Error: Skill name is required.');
    console.log('Usage: npx agentforge add <skill-name> [--agent copilot]');
    process.exit(1);
  }

  const agentKey = targetAgent.toLowerCase();
  const pathResolver = AGENT_PATHS[agentKey];
  if (!pathResolver) {
    console.error(`Error: Unknown agent '${targetAgent}'. Supported: copilot, antigravity, cursor, claude.`);
    process.exit(1);
  }

  const catalog = await loadCatalog();
  const entry = catalog.find((s) => s.name === skillName);
  if (!entry) {
    console.error(`Error: Skill '${skillName}' not found in catalog.`);
    process.exit(1);
  }

  const destDir = path.resolve(process.cwd(), pathResolver(skillName));
  fs.mkdirSync(destDir, { recursive: true });

  const destFile = path.join(destDir, 'SKILL.md');
  const localSource = path.resolve(__dirname, `../${entry.path}/SKILL.md`);

  if (fs.existsSync(localSource)) {
    fs.copyFileSync(localSource, destFile);
  } else {
    console.log(`Downloading ${skillName}...`);
    const content = await fetchText(`${RAW_BASE}/${entry.path}/SKILL.md`);
    fs.writeFileSync(destFile, content, 'utf8');
  }

  console.log(`\n✔ Installed skill: ${skillName}`);
  console.log(`Target Agent:   ${targetAgent}`);
  console.log(`Location:       ${destFile}\n`);
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === '--help' || command === '-h') {
    console.log(`
AgentForge CLI - Install AI Agent Skills

Usage:
  npx agentforge add <skill-name> [--agent copilot|antigravity|cursor|claude]
  npx agentforge list

Supported Agents:
  copilot      .github/skills/<skill-name>/SKILL.md (Default)
  antigravity  .agents/skills/<skill-name>/SKILL.md
  cursor       .cursor/skills/<skill-name>/SKILL.md
  claude       .claude/skills/<skill-name>/SKILL.md
`);
    return;
  }

  if (command === 'list') {
    await listSkills();
  } else if (command === 'add') {
    const skillName = args[1];
    let agent = 'copilot';
    const agentIdx = args.indexOf('--agent') !== -1 ? args.indexOf('--agent') : args.indexOf('-a');
    if (agentIdx !== -1 && args[agentIdx + 1]) {
      agent = args[agentIdx + 1];
    }
    await addSkill(skillName, agent);
  } else {
    console.error(`Unknown command '${command}'. Run 'agentforge --help' for usage.`);
  }
}

main().catch((err) => {
  console.error(`Execution failed: ${err.message}`);
  process.exit(1);
});

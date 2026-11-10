# AgentForge: AI-Native SDLC Skill Library

## Overview (TL;DR)
This repository collects AI agent skills created by engineers across our organization.
These skills improve productivity in daily software development work.
Share skills that give proven results.
Automation organizes approved skills into the library.

---

## SDLC Categories

Skills belong to one of six SDLC categories:

1. **`plan-and-spec`**: Requirements, specs, and user story breakdown.
2. **`architecture`**: Architecture design records (ADRs), data models, and API design.
3. **`coding-and-refactor`**: Code generation, pattern migration, and refactoring.
4. **`testing-and-qa`**: Unit tests, mock generation, and edge-case testing.
5. **`review-and-security`**: Pull request reviews, security checks, and code quality.
6. **`deploy-and-ops`**: CI/CD workflows, Kubernetes diagnostics, and incident support.

---

## How to Submit an Existing Skill

Do not create a skill from zero.
Submit a skill that you already use and trust.

### Procedure

1. Make a new Git branch:
   ```bash
   git checkout -b submit/<skill-name>
   ```

2. Copy your skill folder into the `submissions/` directory:
   ```text
   submissions/
   └── <skill-name>/
       ├── SKILL.md
       └── scripts/ (optional)
   ```

3. Ensure `SKILL.md` conforms to the Agent Skills standard:
   ```yaml
   ---
   name: your-skill-name
   description: >-
     State what the skill does and when the agent must use it.
     Use third-person voice.
   metadata:
     sdlc-phase: review-and-security
     observed-benefit: "Saves 20 minutes on each pull request review."
     author: "@your-github-handle"
     tested-with: "github-copilot, antigravity, cursor, claude-code"
   ---
   ```

4. Push your branch and open a Pull Request (PR).

5. Complete the three questions in the PR template.

---

## Review and Approval Process

1. A repository moderator examines your PR.
2. The moderator verifies that no passwords, API keys, or private tokens exist in the files.
3. The moderator approves and merges the PR.
4. GitHub Actions automatically moves your skill into `skills/<sdlc_phase>/<skill-name>/`.
5. GitHub Actions updates the [CATALOG.md](CATALOG.md) file.

---

## How to Install a Skill in Your Project

Engineers can install skills into their project using either `npx skills` (standard package manager) or a zero-dependency `curl` one-liner.

---

### Option 1: Using `npx skills` (Recommended)

`agentforge` is 100% compatible with the open [`vercel-labs/skills`](https://github.com/vercel-labs/skills) standard.

#### 1. Interactive Picker
Browse and select skills interactively in your terminal:
```bash
npx skills add kolithadesilva/agentforge
```

#### 2. Install a Specific Skill for GitHub Copilot
Install directly into `.github/skills/`:
```bash
npx skills add kolithadesilva/agentforge --skill pull-request-security-check -a copilot
```

#### 3. Install for Other Coding Agents
```bash
# For Google Antigravity
npx skills add kolithadesilva/agentforge --skill pull-request-security-check -a antigravity

# For Cursor
npx skills add kolithadesilva/agentforge --skill pull-request-security-check -a cursor

# For Claude Code
npx skills add kolithadesilva/agentforge --skill pull-request-security-check -a claude-code
```

#### 4. Global Installation
Install a skill globally so all your local projects have it:
```bash
npx skills add kolithadesilva/agentforge --skill pull-request-security-check -g
```

---

### Option 2: Zero-Dependency Scripts (No Node Required)

If you do not have Node.js or `npx` installed, use the native shell installer for your operating system.

#### macOS & Linux (Bash / Zsh)
```bash
# Default: Installs for GitHub Copilot (.github/skills/<skill-name>/)
curl -fsSL https://raw.githubusercontent.com/kolithadesilva/agentforge/main/install.sh | bash -s <skill-name>

# Specify other agents: copilot | antigravity | cursor | claude
curl -fsSL https://raw.githubusercontent.com/kolithadesilva/agentforge/main/install.sh | bash -s <skill-name> cursor
```

#### Windows (PowerShell)
Open PowerShell in your project directory:
```powershell
# Default: Installs for GitHub Copilot (.github/skills/<skill-name>/)
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/kolithadesilva/agentforge/main/install.ps1))) <skill-name>

# Specify other agents: copilot | antigravity | cursor | claude
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/kolithadesilva/agentforge/main/install.ps1))) <skill-name> cursor
```

---

### Agent Directory Mapping

Each coding agent reads skills from a specific directory:

| Coding Agent | Project Installation Path |
| :--- | :--- |
| **GitHub Copilot** | `.github/skills/<skill-name>/SKILL.md` |
| **Antigravity** | `.agents/skills/<skill-name>/SKILL.md` |
| **Cursor** | `.cursor/skills/<skill-name>/SKILL.md` |
| **Claude Code** | `.claude/skills/<skill-name>/SKILL.md` |

---

## Security Rules

- **Do not** add corporate passwords or API tokens.
- **Do not** add private customer data.
- Use environment variables for secrets in scripts.

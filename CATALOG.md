# AI-Native SDLC Agent Skills Catalog

## Summary
This catalog lists **2** agent skills verified by engineers across our organization.
Each skill includes the observed benefit in real development workflows.

### How to Install a Skill
Inside your project repository, run either `npx skills` or the zero-dependency `curl` command:

#### Option 1: Using `npx skills` (Vercel Skills Package Manager)
```bash
# Interactive picker for this repository:
npx skills add kolithadesilva/agentforge

# Direct install for GitHub Copilot (.github/skills/<skill-name>/):
npx skills add kolithadesilva/agentforge --skill <skill-name> -a copilot
```

#### Option 2: Zero-Dependency Scripts (No Node Required)
**macOS / Linux (Bash):**
```bash
# Default: Installs for GitHub Copilot (.github/skills/<skill-name>/)
curl -fsSL https://raw.githubusercontent.com/kolithadesilva/agentforge/main/install.sh | bash -s <skill-name>

# Specify target agent: copilot | antigravity | cursor | claude
curl -fsSL https://raw.githubusercontent.com/kolithadesilva/agentforge/main/install.sh | bash -s <skill-name> <agent>
```

**Windows (PowerShell):**
```powershell
# Default: Installs for GitHub Copilot (.github/skills/<skill-name>/)
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/kolithadesilva/agentforge/main/install.ps1))) <skill-name>

# Specify target agent: copilot | antigravity | cursor | claude
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/kolithadesilva/agentforge/main/install.ps1))) <skill-name> <agent>
```

---

### Plan And Spec (`plan-and-spec`)

*No skills currently registered for this phase.*

### Architecture (`architecture`)

*No skills currently registered for this phase.*

### Coding And Refactor (`coding-and-refactor`)

*No skills currently registered for this phase.*

### Testing And Qa (`testing-and-qa`)

| Skill Name | Description | Observed Benefit | Tested Agents | Author |
| :--- | :--- | :--- | :--- | :--- |
| **[edge-case-unit-test-generator](skills/testing-and-qa/edge-case-unit-test-generator/SKILL.md)** | Generate boundary and failure condition tests for existing functions. Use this skill when adding unit tests, increasing test coverage, or testing edge cases. | Generates boundary condition tests (nulls, empty strings, timeouts). Increases test coverage by ~25%. | github-copilot, antigravity, cursor | @qa-guild |

### Review And Security (`review-and-security`)

| Skill Name | Description | Observed Benefit | Tested Agents | Author |
| :--- | :--- | :--- | :--- | :--- |
| **[pull-request-security-check](skills/review-and-security/pull-request-security-check/SKILL.md)** | Inspect git diffs for security vulnerabilities, hardcoded secrets, and missing authentication guards. Use this skill when reviewing pull requests or preparing code for review. | Finds missing authorization checks and exposed test keys before human code review. Saves ~20 minutes per PR. | github-copilot, antigravity, cursor, claude-code | @appsec-team |

### Deploy And Ops (`deploy-and-ops`)

*No skills currently registered for this phase.*

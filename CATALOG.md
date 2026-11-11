# AI-Native SDLC Agent Skills Catalog

## Summary
This catalog lists **3** agent skills verified by engineers across our organization.
Each skill includes the observed benefit in real development workflows.

### How to Install a Skill
Requires **Node.js 18+ and npx** ([nodejs.org](https://nodejs.org/)).

Inside your project repository, run:
```bash
# Interactive picker for this repository:
npx skills add kolithadesilva/agentforge

# Direct install for GitHub Copilot (.github/skills/<skill-name>/):
npx skills add kolithadesilva/agentforge --skill <skill-name> -a github-copilot

# Direct install for other coding agents:
npx skills add kolithadesilva/agentforge --skill <skill-name> -a [antigravity|cursor|claude-code]
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

| Skill Name | Description | Observed Benefit | Tested Agents | Author |
| :--- | :--- | :--- | :--- | :--- |
| **[k8s-crashloop-diagnostics](skills/deploy-and-ops/k8s-crashloop-diagnostics/SKILL.md)** | Diagnose Kubernetes pods stuck in CrashLoopBackOff or Error states. Use this skill when pods fail to start, crash unexpectedly, or report OOMKilled events. | Isolates root cause of pod failures in under 2 minutes. Saves ~30 minutes of manual log searching. | github-copilot, antigravity, cursor, claude-code | @devops-guild |

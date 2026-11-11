#!/usr/bin/env python3
"""
Curate and Catalog Script for AgentForge.

Conforms to the open Agent Skills specification (name, description, and metadata map).

TL;DR:
1. Moves approved skills from `submissions/` to `skills/<sdlc_phase>/`.
2. Normalizes skill metadata.
3. Rebuilds CATALOG.md and catalog/catalog.json.
"""

import os
import re
import sys
import json
import shutil
from pathlib import Path

VALID_PHASES = [
    "plan-and-spec",
    "architecture",
    "coding-and-refactor",
    "testing-and-qa",
    "review-and-security",
    "deploy-and-ops",
]

REPO_ROOT = Path(__file__).resolve().parent.parent
SUBMISSIONS_DIR = REPO_ROOT / "submissions"
SKILLS_DIR = REPO_ROOT / "skills"
CATALOG_MD = REPO_ROOT / "CATALOG.md"
CATALOG_JSON_DIR = REPO_ROOT / "catalog"
CATALOG_JSON = CATALOG_JSON_DIR / "catalog.json"


def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter into a dictionary, supporting standard metadata map."""
    pattern = r"^---\s*\n(.*?)\n---\s*\n(.*)$"
    match = re.match(pattern, content, re.DOTALL)
    if not match:
        return {}, content

    yaml_block = match.group(1)
    body = match.group(2)
    result = {"metadata": {}}

    in_metadata = False
    current_multiline_key = None
    multiline_buf = []

    for raw_line in yaml_block.splitlines():
        line = raw_line.rstrip()
        if not line or line.strip().startswith("#"):
            continue

        indent = len(line) - len(line.lstrip())
        stripped = line.strip()

        # Handle multiline description continuation
        if current_multiline_key and indent > 0 and ":" not in stripped:
            multiline_buf.append(stripped)
            continue
        elif current_multiline_key and (indent == 0 or (":" in stripped and not stripped.startswith("-"))):
            combined = " ".join(multiline_buf).strip()
            if in_metadata:
                result["metadata"][current_multiline_key] = combined
            else:
                result[current_multiline_key] = combined
            current_multiline_key = None
            multiline_buf = []

        if stripped == "metadata:":
            in_metadata = True
            continue

        if ":" in stripped:
            key, val = stripped.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")

            if val in (">-", ">", "|", "|-"):
                current_multiline_key = key
                multiline_buf = []
                continue

            target = result["metadata"] if in_metadata and indent > 0 else result
            if indent == 0 and in_metadata:
                in_metadata = False
                target = result

            if val.startswith("[") and val.endswith("]"):
                items = [item.strip().strip('"').strip("'") for item in val[1:-1].split(",") if item.strip()]
                target[key] = items
            else:
                target[key] = val

    if current_multiline_key:
        combined = " ".join(multiline_buf).strip()
        if in_metadata:
            result["metadata"][current_multiline_key] = combined
        else:
            result[current_multiline_key] = combined

    return result, body


def get_skill_attribute(parsed: dict, key: str, default=""):
    """Fetch attribute from top-level or from standard 'metadata' map."""
    if key in parsed:
        return parsed[key]
    # Check with hyphens or underscores
    hyphen_key = key.replace("_", "-")
    underscore_key = key.replace("-", "_")

    meta = parsed.get("metadata", {})
    if key in meta:
        return meta[key]
    if hyphen_key in meta:
        return meta[hyphen_key]
    if underscore_key in meta:
        return meta[underscore_key]
    if hyphen_key in parsed:
        return parsed[hyphen_key]
    if underscore_key in parsed:
        return parsed[underscore_key]

    return default


def organize_submissions():
    """Move folders from submissions/ to skills/<sdlc_phase>/."""
    if not SUBMISSIONS_DIR.exists():
        return 0

    moved_count = 0
    for item in SUBMISSIONS_DIR.iterdir():
        if not item.is_dir() or item.name.startswith("."):
            continue

        skill_dir = item
        skill_name = item.name
        skill_file = skill_dir / "SKILL.md"

        metadata = {}
        if skill_file.exists():
            content = skill_file.read_text(encoding="utf-8")
            metadata, _ = parse_frontmatter(content)

        sdlc_phase = get_skill_attribute(metadata, "sdlc_phase", "").lower()
        if sdlc_phase not in VALID_PHASES:
            print(f"[Notice] Skill '{skill_name}' has unrecognized phase '{sdlc_phase}'. Defaulting to 'coding-and-refactor'.")
            sdlc_phase = "coding-and-refactor"

        target_dir = SKILLS_DIR / sdlc_phase / skill_name
        target_dir.parent.mkdir(parents=True, exist_ok=True)

        if target_dir.exists():
            print(f"[Warning] Target '{target_dir}' already exists. Overwriting.")
            shutil.rmtree(target_dir)

        shutil.move(str(skill_dir), str(target_dir))
        print(f"[Organized] Moved '{skill_name}' -> 'skills/{sdlc_phase}/{skill_name}'")
        moved_count += 1

    return moved_count


def scan_skills():
    """Scan all skills in skills/ and collect metadata."""
    skills = []
    if not SKILLS_DIR.exists():
        return skills

    for phase_dir in SKILLS_DIR.iterdir():
        if not phase_dir.is_dir() or phase_dir.name.startswith("."):
            continue
        phase = phase_dir.name

        for skill_dir in phase_dir.iterdir():
            if not skill_dir.is_dir() or skill_dir.name.startswith("."):
                continue

            skill_name = skill_dir.name
            skill_file = skill_dir / "SKILL.md"
            meta = {
                "name": skill_name,
                "description": "",
                "sdlc_phase": phase,
                "observed_benefit": "Not specified",
                "author": "Community",
                "tested_with": [],
                "tags": [],
                "path": f"skills/{phase}/{skill_name}",
            }

            if skill_file.exists():
                content = skill_file.read_text(encoding="utf-8")
                parsed, _ = parse_frontmatter(content)
                meta["name"] = parsed.get("name", skill_name)
                meta["description"] = parsed.get("description", "")
                meta["observed_benefit"] = get_skill_attribute(parsed, "observed_benefit", "Not specified")
                meta["author"] = get_skill_attribute(parsed, "author", "Community")
                tested = get_skill_attribute(parsed, "tested_with", [])
                if isinstance(tested, str):
                    tested = [t.strip() for t in tested.split(",") if t.strip()]
                meta["tested_with"] = tested
                meta["path"] = f"skills/{phase}/{skill_name}"
                meta["sdlc_phase"] = phase

            skills.append(meta)

    return sorted(skills, key=lambda x: (x["sdlc_phase"], x["name"]))


def generate_catalog(skills):
    """Write CATALOG.md and catalog.json."""
    CATALOG_JSON_DIR.mkdir(parents=True, exist_ok=True)
    with open(CATALOG_JSON, "w", encoding="utf-8") as f:
        json.dump(skills, f, indent=2)
    print(f"[Catalog] Wrote {len(skills)} skills to {CATALOG_JSON}")

    lines = [
        "# AI-Native SDLC Agent Skills Catalog",
        "",
        "## Summary",
        f"This catalog lists **{len(skills)}** agent skills verified by engineers across our organization.",
        "Each skill includes the observed benefit in real development workflows.",
        "",
        "### How to Install a Skill",
        "Requires **Node.js 18+ and npx** ([nodejs.org](https://nodejs.org/)).",
        "",
        "Inside your project repository, run:",
        "```bash",
        "# Interactive picker for this repository:",
        "npx skills add kolithadesilva/agentforge",
        "",
        "# Direct install for GitHub Copilot (.github/skills/<skill-name>/):",
        "npx skills add kolithadesilva/agentforge --skill <skill-name> -a github-copilot",
        "",
        "# Direct install for other coding agents:",
        "npx skills add kolithadesilva/agentforge --skill <skill-name> -a [antigravity|cursor|claude-code]",
        "```",
        "",
        "---",
        "",
    ]

    for phase in VALID_PHASES:
        phase_skills = [s for s in skills if s.get("sdlc_phase") == phase]
        phase_title = phase.replace("-", " ").title()
        lines.append(f"### {phase_title} (`{phase}`)")
        lines.append("")

        if not phase_skills:
            lines.append("*No skills currently registered for this phase.*")
            lines.append("")
            continue

        lines.append("| Skill Name | Description | Observed Benefit | Tested Agents | Author |")
        lines.append("| :--- | :--- | :--- | :--- | :--- |")

        for s in phase_skills:
            name_link = f"[{s['name']}]({s['path']}/SKILL.md)"
            desc = s.get("description", "").replace("\n", " ")
            benefit = s.get("observed_benefit", "None provided")
            agents = ", ".join(s.get("tested_with", [])) if s.get("tested_with") else "Not listed"
            author = s.get("author", "Community")
            lines.append(f"| **{name_link}** | {desc} | {benefit} | {agents} | {author} |")

        lines.append("")

    CATALOG_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"[Catalog] Wrote updated catalog to {CATALOG_MD}")


def main():
    print("=== Running AgentForge Curation ===")
    moved = organize_submissions()
    skills = scan_skills()
    generate_catalog(skills)
    print(f"=== Complete: {moved} skills organized, {len(skills)} skills cataloged ===")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
AgentForge Skill Validation Script (ASD-STE100 / TL;DR)

Validates that submitted skills follow the Agent Skills standard and SDLC rules.
Exits with code 1 if any validation checks fail.
"""

import sys
import re
from pathlib import Path

VALID_PHASES = [
    "plan-and-spec",
    "architecture",
    "coding-and-refactor",
    "testing-and-qa",
    "review-and-security",
    "deploy-and-ops",
]

SECRET_PATTERNS = [
    (r"ghp_[a-zA-Z0-9]{36}", "GitHub Personal Access Token"),
    (r"gho_[a-zA-Z0-9]{36}", "GitHub OAuth Token"),
    (r"AKIA[0-9A-Z]{16}", "AWS Access Key ID"),
    (r"-----BEGIN (RSA|EC|DSA|OPENSSH|PRIVATE) KEY-----", "Private Cryptographic Key"),
    (r"sk-[a-zA-Z0-9]{20,}", "API Secret Key"),
    (r"(password|passwd|secret|token)\s*[:=]\s*['\"][^'\"]{6,}['\"]", "Hardcoded Password or Secret"),
]

REPO_ROOT = Path(__file__).resolve().parent.parent
SUBMISSIONS_DIR = REPO_ROOT / "submissions"


def parse_frontmatter(content: str):
    """Extract YAML frontmatter into a dictionary."""
    pattern = r"^---\s*\n(.*?)\n---\s*\n(.*)$"
    match = re.match(pattern, content, re.DOTALL)
    if not match:
        return None, content

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


def validate_submission_dir(skill_dir: Path):
    """Validate a single skill submission directory."""
    errors = []
    folder_name = skill_dir.name

    # Rule 1: Directory name must be lowercase kebab-case
    if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", folder_name):
        errors.append(
            f"Invalid folder name '{folder_name}'. Must use lowercase letters, numbers, and hyphens only (e.g. 'my-skill')."
        )

    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        errors.append(f"Missing required file: submissions/{folder_name}/SKILL.md")
        return errors

    content = skill_file.read_text(encoding="utf-8")

    # Rule 2: Secret / Token Scan
    for pattern, desc in SECRET_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            errors.append(f"Security Alert: Potential {desc} detected in {folder_name}/SKILL.md.")

    # Rule 3: Valid YAML frontmatter
    parsed, body = parse_frontmatter(content)
    if parsed is None:
        errors.append(f"Missing or malformed YAML frontmatter in {folder_name}/SKILL.md (must start and end with '---').")
        return errors

    # Rule 4: Required 'name' field
    skill_name = parsed.get("name", "").strip()
    if not skill_name:
        errors.append(f"Missing required top-level field 'name' in {folder_name}/SKILL.md.")
    elif skill_name != folder_name:
        errors.append(f"Name mismatch: 'name: {skill_name}' does not match directory name '{folder_name}'.")

    # Rule 5: Required 'description' field
    description = parsed.get("description", "").strip()
    if not description:
        errors.append(f"Missing required top-level field 'description' in {folder_name}/SKILL.md.")
    elif len(description) < 20:
        errors.append(
            f"Description in {folder_name}/SKILL.md is too short ({len(description)} chars). Minimum is 20 characters."
        )

    # Rule 6: Required 'sdlc-phase' in metadata
    sdlc_phase = get_skill_attribute(parsed, "sdlc_phase", "").strip().lower()
    if not sdlc_phase:
        errors.append(
            f"Missing required metadata field 'sdlc-phase' in {folder_name}/SKILL.md.\n"
            f"Allowed values: {', '.join(VALID_PHASES)}"
        )
    elif sdlc_phase not in VALID_PHASES:
        errors.append(
            f"Invalid 'sdlc-phase: {sdlc_phase}' in {folder_name}/SKILL.md.\n"
            f"Must be one of: {', '.join(VALID_PHASES)}"
        )

    return errors


def main():
    if not SUBMISSIONS_DIR.exists():
        print("No submissions/ directory found. Validation passed.")
        sys.exit(0)

    subdirs = [d for d in SUBMISSIONS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")]
    if not subdirs:
        print("No pending submissions to validate.")
        sys.exit(0)

    print(f"=== Validating {len(subdirs)} submission(s) ===")
    all_errors = []

    for d in subdirs:
        errors = validate_submission_dir(d)
        if errors:
            all_errors.extend(errors)

    if all_errors:
        print("\n[VALIDATION FAILED] The submission violates repository guidelines:\n")
        for idx, err in enumerate(all_errors, 1):
            print(f"  {idx}. {err}")
        print("\nPlease fix these errors before requesting moderator review.\n")
        sys.exit(1)

    print("[SUCCESS] All submission checks passed successfully!")
    sys.exit(0)


if __name__ == "__main__":
    main()

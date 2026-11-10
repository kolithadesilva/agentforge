---
name: pull-request-security-check
description: >-
  Inspect git diffs for security vulnerabilities, hardcoded secrets, and missing authentication guards.
  Use this skill when reviewing pull requests or preparing code for review.
metadata:
  sdlc-phase: review-and-security
  observed-benefit: "Finds missing authorization checks and exposed test keys before human code review. Saves ~20 minutes per PR."
  author: "@appsec-team"
  tested-with: "github-copilot, antigravity, cursor, claude-code"
---

# Pull Request Security Check

## Purpose (TL;DR)
This skill analyzes git diffs for common security vulnerabilities before you request human review.

## Prerequisites
- Git command line installed.
- Uncommitted or branch changes ready for review.

## Step-by-Step Procedure
1. Execute `git diff origin/main...HEAD` to inspect changes.
2. Search for hardcoded secrets, database credentials, and unencrypted private keys.
3. Verify that every new HTTP endpoint includes authentication middleware.
4. Verify that all external user input passes validation before database queries.
5. Generate a markdown table summarizing findings and required fixes.

## Guardrails
- **Do not** approve pull requests automatically.
- **Do not** send private repository code to external networks.

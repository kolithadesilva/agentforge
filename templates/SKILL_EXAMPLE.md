---
name: pull-request-security-check
description: >-
  Inspect git diffs for security vulnerabilities, hardcoded secrets, and missing authentication guards.
  Use this skill when reviewing pull requests or preparing code for review.
metadata:
  sdlc-phase: review-and-security
  observed-benefit: "Finds missing authorization checks before human code review. Saves 20 minutes per PR."
  author: "@jane-doe"
  tested-with: "github-copilot, antigravity, cursor, claude-code"
---

# Pull Request Security Check

## Purpose (TL;DR)
This skill checks git diffs for common security vulnerabilities before code review.

## Prerequisites
- Git command line installed.
- Access to the target git repository.

## Step-by-Step Procedure
1. Inspect the git diff of the current branch.
2. Search for hardcoded credentials, test passwords, and unencrypted keys.
3. Verify that all new API endpoints have authentication guards.
4. Report detected issues in a structured table.

## Guardrails
- **Do not** approve pull requests automatically.
- **Do not** send code contents to external endpoints.

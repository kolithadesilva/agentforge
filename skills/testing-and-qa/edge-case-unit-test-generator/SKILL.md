---
name: edge-case-unit-test-generator
description: >-
  Generate boundary and failure condition tests for existing functions.
  Use this skill when adding unit tests, increasing test coverage, or testing edge cases.
metadata:
  sdlc-phase: testing-and-qa
  observed-benefit: "Generates boundary condition tests (nulls, empty strings, timeouts). Increases test coverage by ~25%."
  author: "@qa-guild"
  tested-with: "github-copilot, antigravity, cursor"
---

# Edge-Case Unit Test Generator

## Purpose (TL;DR)
This skill generates boundary and failure condition tests for existing functions.

## Prerequisites
- Target source file with functions to test.
- Existing test framework configured in the project (for example: Jest, PyTest, or Go test).

## Step-by-Step Procedure
1. Read the target function and identify all parameter types.
2. Generate tests for these input conditions:
   - Null, empty, or undefined values.
   - Values that exceed numeric boundaries (for example: negative numbers, zero, max integers).
   - Network timeouts and downstream exception handling.
3. Write test functions matching the existing project test style.
4. Execute the test runner to confirm that all generated tests pass.

## Guardrails
- **Do not** modify the source code file while writing tests.
- **Do not** introduce new external testing libraries.

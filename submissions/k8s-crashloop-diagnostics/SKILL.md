---
name: k8s-crashloop-diagnostics
description: >-
  Diagnose Kubernetes pods stuck in CrashLoopBackOff or Error states.
  Use this skill when pods fail to start, crash unexpectedly, or report OOMKilled events.
metadata:
  sdlc-phase: deploy-and-ops
  observed-benefit: "Isolates root cause of pod failures in under 2 minutes. Saves ~30 minutes of manual log searching."
  author: "@devops-guild"
  tested-with: "github-copilot, antigravity, cursor, claude-code"
---

# Kubernetes CrashLoopBackOff Diagnostics

## Purpose (TL;DR)
This skill analyzes failing Kubernetes pods, inspects recent termination events, and identifies root causes.

## Prerequisites
- `kubectl` CLI installed and configured.
- Read permissions for the target cluster namespace.

## Step-by-Step Procedure
1. Execute `kubectl get pods -n <namespace>` to identify crashing pods.
2. Execute `kubectl describe pod <pod-name> -n <namespace>` to inspect the last termination state and exit code.
3. If exit code is 137 (`OOMKilled`), inspect memory requests and limits against historical usage.
4. If exit code is 1 or non-zero, run `kubectl logs <pod-name> -n <namespace> --previous` to inspect crash logs.
5. Provide a summary of the failure cause and recommended fix (such as memory limit adjustment or config map correction).

## Guardrails
- **Do not** restart, delete, or modify pods without explicit user confirmation.
- **Do not** output secrets or environment variables in logs.

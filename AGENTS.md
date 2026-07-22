# AGENTS.md

## Project Purpose

This repository supports static privacy assessment of Android APKs and targeted reconstruction of source-code-level evidence from decompiled APK artifacts.

The final deliverable is a publishable report. Claims in that report must be traceable to either:

- Androguard APK metadata and bytecode analysis.
- Decompiled APK evidence from `apktool` output.
- Reviewed reconstructed source or pseudocode derived from the decompiled files.
- Explicitly labeled dynamic/runtime analysis, if added later.

## Current Inputs

- Sample APK: `TikTok_39.2.1_APKPure.apk`
- Primary static report: `tik_tok_report.json`
- Decompiled tree: `tiktok_decompiled/`
- Existing narrative draft: `llm_analysis.md`
- Existing dashboard renderer: `dashboard.py`

There is also an older or duplicate TikTok decompiled tree, `TikTok_39.2.1_APKPure_Decompiled/`. Prefer `tiktok_decompiled/` for the bundled sample unless a task explicitly says otherwise. For other apps, set `APK=...`, `REPORT=...`, and `DECOMPILE_DIR=...`.

## Workflows

Use Taskfile targets for common project operations:

```bash
task setup
task check
task test
task path1-check
task analyze
task decompile
task dashboard
task llm
task corpus-stats
task privacy-keywords
task report-evidence
task report-draft
```

Before changing analysis code, run:

```bash
task check
```

Before calling the Androguard structured-analysis path complete, run:

```bash
task path1-check
```

When regenerating analysis outputs, do not overwrite manual report drafts unless the task explicitly calls for it.

## Evidence Standards

- Separate declared capability from observed behavior.
- Treat a permission declaration as evidence of app capability, not proof of collection.
- Treat a static API reference as evidence that code can call an API, not proof that a user flow triggers it.
- Generate `privacy_evidence_brief.md` deterministically before creating prompted prose.
- Mark prompted prose as draft analysis until checked against source evidence.
- Prefer file path and line references from `tiktok_decompiled/` for publishable findings.
- Keep reconstruction focused on privacy-relevant classes, SDKs, and call paths rather than attempting to fully restore the full application.

## Reconstruction Priorities

Prioritize code related to:

- Device identifiers and advertising identifiers.
- Location, camera, microphone, contacts, media, and installed-app access.
- Local persistence, especially `SharedPreferences`, SQLite, logs, caches, and external storage.
- Network clients, telemetry, analytics, ad SDKs, and endpoint construction.
- Dynamic code loading, reflection, native libraries, anti-tamper, and command execution.
- Exported Android components and deep link entry points.

## Repo Hygiene

- Keep generated bulk outputs out of version control unless they are small, reviewed, and useful for the report.
- Avoid broad refactors while the report evidence path is still being stabilized.
- Do not delete APKs, decompiled trees, reports, or backups without explicit approval.

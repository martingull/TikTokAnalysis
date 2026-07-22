# APK Privacy Analysis

This project statically analyzes consumer Android APKs and builds evidence-backed privacy assessment drafts. The included sample data is for TikTok, but the workflow is intentionally generic: use the same commands for Snapchat, Instagram, or any other APK.

The working premise is that modern consumer tech can be intrusive. The repo still separates that premise from evidence: permissions are capability evidence, static API references are code-presence evidence, and runtime behavior requires dynamic validation.

## Current Report

The current human-consumable report artifact is:

```text
privacy_assessment_report.md
```

See `GENERATED_ARTIFACTS.md` for the full artifact map.

## Workflow

Install dependencies:

```bash
task setup
```

Analyze any APK:

```bash
task analyze APK=/path/to/app.apk REPORT=app_report.json
```

Verify the structured Androguard path for an existing report:

```bash
task path1-check REPORT=app_report.json
```

Decompile any APK:

```bash
task decompile APK=/path/to/app.apk DECOMPILE_DIR=app_decompiled
```

Create reconstruction inventory and prompted report draft:

```bash
task inventory DECOMPILE_DIR=app_decompiled INVENTORY=app_inventory.json INVENTORY_MD=app_inventory.md
task report-draft REPORT=app_report.json INVENTORY=app_inventory.json REPORT_MD=app_privacy_report.md
```

`task report-draft` uses `PRIVACY_PROMPT` from `promps.py` and OpenAI SDK settings from `.env`. It also writes a deterministic evidence brief before prompting:

```bash
task report-evidence REPORT=app_report.json INVENTORY=app_inventory.json EVIDENCE_MD=app_evidence_brief.md
```

To generate the exact prompt payload locally without sending data to a model:

```bash
task report-prompt REPORT=app_report.json INVENTORY=app_inventory.json PROMPT_MD=app_prompt_payload.md
```

The default prompted model is `gpt-5.5`. To override it, pass:

```bash
task report-draft MODEL=your-model-name
```

For the bundled TikTok sample, the defaults are:

```bash
task dashboard
task inventory
task report-draft
```

## Main Files

- `androguard_analysis.py` - creates a structured APK report from Androguard.
- `apk_analysis.py` - decompiles an APK with apktool and scans smali for privacy-relevant patterns.
- `reconstruction_inventory.py` - ranks privacy-relevant smali files and selects first-pass source slices.
- `report_builder.py` - creates a deterministic evidence brief.
- `prompted_report.py` - uses `PRIVACY_PROMPT` to create the final audience-readable report.
- `dashboard.py` - renders a terminal dashboard for the structured report.
- `llm_analysis.py` - optional OpenAI-assisted analysis.
- `ROADMAP.md` - current project roadmap and definition of done.
- `AGENTS.md` - working instructions for future agents.

## Current Path Status

- Path 1, Androguard structured analysis: Milestone 1 complete.
- Path 2, source reconstruction: inventory exists; manual reconstruction with line citations remains.

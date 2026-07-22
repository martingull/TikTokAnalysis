# APK Privacy Analysis

This project statically analyzes consumer Android APKs and builds evidence-backed privacy assessment drafts. The included sample data is for TikTok, but the workflow is intentionally generic: use the same commands for Snapchat, Instagram, or any other APK.

The working premise is that modern consumer tech can be intrusive. The repo still separates that premise from evidence: permissions are capability evidence, static API references are code-presence evidence, and runtime behavior requires dynamic validation.

## Project Direction

This repo is moving toward a repeatable CLI tool in the style of `rectool`: Codex or VS Code Codex can be used as the planner, reviewer, and report assistant, but execution should stay in explicit Taskfile/Python commands. The durable interface is the CLI workflow, not an ad hoc chat transcript.

## Final Product

The deliverable is an evidence-backed APK privacy assessment package.

It consists of:

- A human-consumable privacy report: `privacy_assessment_report.md`
- A reproducible CLI workflow for regenerating the analysis from an APK
- Structured evidence artifacts for permissions, components, certificates, suspicious APIs, and reconstruction targets
- Source review packets that cite apktool smali and optionally include JADX Java-like context
- Clear labels distinguishing declared capability, static code presence, reviewed source behavior, and runtime-observed behavior

The deliverable is not a full reconstructed source tree. Decompiled source is a supporting evidence layer used to explain and verify privacy/security findings.

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

Get a first-pass privacy indication for any APK:

```bash
task privacy-indication APK=/path/to/app.apk REPORT=app_report.json EVIDENCE_MD=app_evidence_brief.md
```

This runs the structured Androguard path and writes a deterministic evidence brief without source reconstruction or an LLM call. It is the quickest answer to: "What privacy concerns does this APK appear to raise?"

Build the full static privacy assessment package:

```bash
task privacy-assessment APK=/path/to/app.apk REPORT=app_report.json DECOMPILE_DIR=app_decompiled INVENTORY=app_inventory.json REPORT_MD=app_privacy_report.md
```

This runs the static metadata path, apktool decompilation, reconstruction inventory, source-finding packets, and the prompted report draft. It is the current main product workflow.

Run individual steps when you need finer control:

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

Optionally create Java-like source with JADX:

```bash
task jadx APK=/path/to/app.apk JADX_DIR=app_jadx
```

For large or obfuscated APKs, prefer targeted JADX classes over a full tree:

```bash
task jadx-class APK=/path/to/app.apk JADX_CLASS=com.example.ClassName JADX_SELECTED_DIR=app_jadx_selected
```

Create reconstruction inventory and prompted report draft:

```bash
task inventory DECOMPILE_DIR=app_decompiled INVENTORY=app_inventory.json INVENTORY_MD=app_inventory.md
task source-findings DECOMPILE_DIR=app_decompiled JADX_DIR=app_jadx INVENTORY=app_inventory.json SOURCE_FINDINGS_MD=app_source_findings.md
task report-draft REPORT=app_report.json INVENTORY=app_inventory.json REPORT_MD=app_privacy_report.md
```

For source reconstruction, JADX is the reading layer and apktool smali is the evidence layer. Use JADX output to understand Java/Kotlin-like control flow, then verify publishable claims against smali line references.

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

Security analysis is a future third path. The repo does not currently define a `SECURITY_PROMPT`; privacy reporting is the active publishable workflow, and command execution / dynamic loading markers are handled as privacy-adjacent static findings until the security workflow is added.

## Main Files

- `androguard_analysis.py` - creates a structured APK report from Androguard.
- `apk_analysis.py` - decompiles an APK with apktool and scans smali for privacy-relevant patterns.
- `reconstruction_inventory.py` - ranks privacy-relevant smali files and selects first-pass source slices.
- `source_findings.py` - builds review packets that pair smali evidence with optional JADX source.
- `report_builder.py` - creates a deterministic evidence brief.
- `prompted_report.py` - uses `PRIVACY_PROMPT` to create the final audience-readable report.
- `dashboard.py` - renders a terminal dashboard for the structured report.
- `llm_analysis.py` - optional OpenAI-assisted analysis.
- `ROADMAP.md` - current project roadmap and definition of done.
- `AGENTS.md` - working instructions for future agents.

## Current Path Status

- Path 1, Androguard structured analysis: Milestone 1 complete.
- Path 2, source reconstruction: inventory and source-finding packet generation exist; manual reconstruction with line citations remains.
- Path 3, security marker analysis: planned; no dedicated prompt or workflow is implemented yet.

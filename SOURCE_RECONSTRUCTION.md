# Source Reconstruction

Source reconstruction in this repo means evidence reconstruction, not full application recovery.

The goal is to turn selected apktool/JADX output into reviewed, line-cited source evidence that can support privacy or security claims. The goal is not to rebuild the original app source tree or maintain a compilable fork of the APK.

## Artifact Ladder

| Stage | Artifact | Purpose |
| --- | --- | --- |
| 1 | `reconstruction_inventory.md` | Ranks privacy/security-relevant smali files and selects first-pass source slices. |
| 2 | `source_findings.md` | Generated review packets with smali line context and optional JADX reading context. |
| 3 | `source_reconstruction_status.md` | Shows which generated packets have reviewed notes and JADX context. |
| 4 | `reviewed_source_notes.md` | Human/Codex-reviewed interpretation, confidence, limits, and report relevance. |
| 5 | `privacy_evidence_brief.md` | Deterministic report evidence including reviewed notes when present. |
| 6 | `privacy_assessment_report.md` | Human-readable report generated from the evidence brief and prompt. |

## Commands

Use the cached source reconstruction path when an apktool tree already exists:

```bash
task source-reconstruction DECOMPILE_DIR=app_decompiled INVENTORY=app_inventory.json SOURCE_FINDINGS=app_source_findings.json SOURCE_FINDINGS_MD=app_source_findings.md SOURCE_RECONSTRUCTION_STATUS_MD=app_source_status.md
```

Use the full source reconstruction path when apktool output must be regenerated:

```bash
task source-reconstruction-full APK=/path/to/app.apk DECOMPILE_DIR=app_decompiled
```

Use targeted JADX for selected classes when readable Java-like context would help:

```bash
task jadx-class APK=/path/to/app.apk JADX_CLASS=com.example.SomeClass JADX_SELECTED_DIR=app_jadx_selected
task source-reconstruction DECOMPILE_DIR=app_decompiled JADX_SELECTED_DIR=app_jadx_selected
```

Full JADX can be useful, but it is not required for publishable evidence:

```bash
task jadx APK=/path/to/app.apk JADX_DIR=app_jadx JADX_HEAP=10g JADX_THREADS=2
```

## Evidence Rules

- apktool smali is the evidence layer.
- JADX is the reading layer.
- `source_findings.md` is generated triage, not reviewed evidence.
- `reviewed_source_notes.md` is where reconstructed behavior, confidence, and limits are recorded.
- Static source reconstruction does not prove runtime triggering, collection, transmission, exploitability, or user impact.
- Publishable claims need reviewed notes plus file/line references.

## Review Workflow

For each selected packet:

1. Read the smali evidence and JADX context if available.
2. Reconstruct what the class or method appears to do in plain language.
3. Identify data or capability touched.
4. Decide whether the marker is strong evidence, weak evidence, or likely false positive.
5. Record confidence and what the evidence does not prove.
6. Add runtime or manual follow-up needed before stronger claims.
7. Regenerate `source_reconstruction_status.md` and the report evidence.

## Current Scope

The practical target is focused reconstruction of source slices tied to:

- identifiers and advertising IDs;
- location, camera, microphone, contacts, media, and installed-app access;
- local persistence and cache/storage behavior;
- network clients, telemetry, analytics, ads, and attribution SDKs;
- dynamic loading, reflection, native libraries, anti-tamper, command execution;
- exported Android components and deep link entry points.

The decompiled source tree is supporting material. It is not the final deliverable.

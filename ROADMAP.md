# Roadmap

## Objective

Bring this repository to a publishable state for Android APK privacy assessments. The bundled sample is TikTok, but the workflow should also support APKs from Snapchat, Instagram, and other consumer apps.

## Final Product

The final product is an evidence-backed APK privacy assessment package, not a full recovered application source tree.

The package should include:

- `privacy_assessment_report.md`: the current human-consumable report for publication or review.
- A repeatable CLI workflow for regenerating analysis artifacts from an APK.
- Structured Androguard evidence for manifest metadata, permissions, components, signing metadata, exported surfaces, and suspicious API references.
- Reconstruction review packets that use apktool smali as line-cited evidence and JADX output as readable context where available.
- Evidence labels that distinguish declared capability, static code presence, reviewed source behavior, and runtime-observed behavior.
- A clear list of unresolved claims that need manual reconstruction or dynamic testing before publication.

The reconstructed source tree is supporting material. Its purpose is to improve signal for humans and LLM-assisted review, not to recreate or maintain the original application.

The work has two evidence paths:

1. Androguard analysis: produce structured APK metadata, permissions, exported components, and suspicious API references.
2. Source reconstruction: turn privacy-relevant apktool smali/resources and optional JADX Java-like output into readable source-level evidence.

The report should combine both paths, with every important claim linked back to a concrete artifact.

The user-facing CLI surface should stay granular:

- `task privacy-indication`: quick static privacy indication from Androguard evidence only.
- `task privacy-assessment`: full static privacy assessment package with apktool inventory, source-finding packets, and prompted report output.
- `task jadx-class`: targeted Java-like reconstruction for one selected class when full JADX output is too large.
- `task dynamic-plan`: runtime phone/proxy validation plan derived from static findings.
- Security-marker analysis: future path for command execution, dynamic loading, injection surfaces, exported-component abuse, and similar bug-bounty-oriented evidence. This path should get a dedicated prompt and task once the privacy workflow is stable.

## Current State

- APK: `TikTok_39.2.1_APKPure.apk` at about 435 MB.
- Static report: `tik_tok_report.json` exists for TikTok `39.2.1`, package `com.zhiliaoapp.musically`.
- Decompiled tree: `tiktok_decompiled/` exists at about 4.5 GB.
- JADX output is optional and should be generated into `jadx_decompiled/` with `task jadx` when `jadx` is installed.
- For large APKs, targeted JADX with `task jadx-class JADX_CLASS=...` is preferred over full-tree generation.
- Decompiled corpus size: about 350,641 files, including about 331,014 `.smali` files across 54 smali roots.
- Decompiled assets/resources: about 423 asset files, 18,532 resource files, and 471 native library files.
- Dashboard: `dashboard.py` exists, but its expected JSON keys do not match the current `tik_tok_report.json` shape.

Current `tik_tok_report.json` highlights:

- 51 declared permissions.
- 407 activities, 83 services, 42 broadcast receivers, and 24 content providers.
- 53 exported components.
- Static suspicious API references for dynamic code loading, camera/location access, and command execution.

Current source-reconstruction signals from `tiktok_decompiled/`:

- `getDeviceId`: 325 matches.
- `getSubscriberId`: 1 match.
- `getSimSerialNumber`: 1 match.
- `getLastKnownLocation`: 12 matches.
- `getLatitude`: 43 matches.
- `getLongitude`: 41 matches.
- `getAccounts`: 21 matches.
- `getInstalledPackages`: 3 matches.
- `getMacAddress`: 2 matches.
- `getAdvertisingIdInfo`: 11 matches.
- `System.loadLibrary`: 5 matches.
- `DexClassLoader`: 38 matches.
- `Runtime;->exec`: 14 matches.
- `ProcessBuilder;->start`: 4 matches.
- `SharedPreferences`: 9,430 matches.

## Path Status

### Path 1: Androguard Structured Analysis

**Milestone 1 status:** complete.

This path now provides the structured facts needed by the dashboard, deterministic evidence brief, and prompted report pipeline:

- APK/package/version metadata.
- Permission inventory.
- Android component counts.
- Exported component list.
- Normalized certificate/signing metadata.
- Static suspicious API signals.
- Permission/API mappings with declared-versus-inferred status.
- Evidence-model labels for downstream reports.

Remaining Path 1 work is polish rather than a blocker:

- Expand the suspicious API taxonomy as new APKs reveal additional privacy-sensitive APIs.
- Add deeper exported-component context, especially intent filters and deep link data.
- Add richer signature validation if publication requires cryptographic verification beyond extracted certificate metadata.

### Path 2: Source Reconstruction

**Milestone 1 status:** in progress.

The inventory, shortlist, and source-finding packet generator exist. The publishable source-evidence layer still needs manual reconstruction, pseudocode, confidence labels, and links back to report findings.

JADX is now the preferred reading layer for Java/Kotlin-like app logic when available. apktool smali remains the evidence layer for line-cited claims.

## Outstanding Work

### 1. Stabilize the Analysis Pipeline

- Keep `dashboard.py` compatible with current and legacy Androguard report schemas.
- Keep `apk_analysis.py` accepting CLI arguments for APK and output paths.
- Keep verbose Androguard logging opt-in through `--verbose`.
- Maintain normalized report field names so downstream tools do not need special-case mappings.
- Keep regression checks for report loading, dashboard normalization, and evidence-brief rendering.

### 2. Build a Reconstruction Inventory

- Generate an inventory of packages/classes by smali root and package prefix.
- Identify obfuscated packages versus recognizable third-party and TikTok/ByteDance packages.
- Rank files by privacy-relevant keyword hits.
- Create a reviewed shortlist of classes to reconstruct first.
- Generate optional JADX Java-like source with `task jadx` when `jadx` is installed.
- Prefer targeted JADX source with `task jadx-class` for classes selected by the inventory or keyword scans.
- Generate source reconstruction review packets with `task source-findings`.

### 3. Reconstruct Privacy-Relevant Source Slices

Full reconstruction of roughly 331k smali files is not realistic as a first milestone. The practical target is source-level reconstruction for the code that supports report findings.

Initial slices:

- Device and advertising identifiers.
- Location access.
- Camera and microphone access.
- Contacts and account access.
- Local persistence and cache/storage behavior.
- Exported components and deep link handlers.
- Network, telemetry, analytics, ad, and attribution SDK integrations.
- Dynamic loading, reflection, native libraries, anti-tamper, and shell command execution.

Each reconstructed slice should include:

- Original smali file path and line references.
- JADX source path and readable Java-like context when available.
- Decompiled or reconstructed readable code/pseudocode.
- Explanation of the data touched.
- Confidence level and unresolved ambiguity.
- Link to the report finding it supports.

### 4. Upgrade the Report

- Generate `privacy_evidence_brief.md` deterministically from structured evidence.
- Generate `privacy_assessment_report.md` with `PRIVACY_PROMPT` for a wider audience.
- Add an executive summary that distinguishes privacy risk, security risk, and uncertainty.
- Add an evidence table for each finding.
- Add a methodology section explaining Androguard, apktool, static limits, and any dynamic-analysis gaps.
- Add a limitations section that clearly says static analysis does not prove runtime collection.
- Add remediation or user-impact notes only where the evidence supports them.

### 5. Dashboard and Publishing

- Decide whether `dashboard.py` remains a terminal dashboard or becomes a Streamlit/web dashboard.
- Show counts, permissions, exported components, suspicious APIs, and reconstruction status.
- Include links or paths to evidence files.
- Add a repeatable publish target once the final report format is chosen.

### 6. Dynamic Privacy Validation

- Generate `dynamic_privacy_validation_plan.md` from the static report and source finding packets.
- Use a test device or emulator with a proxy such as Burp Suite, mitmproxy, or Charles.
- Validate static findings against named flows: launch, login, idle, browse, search, profile, post, media upload, contact sync, permission grant/deny, logout.
- Label every active result as `observed`, `not observed`, `blocked`, or `needs source review`.
- Keep raw captures private and publish only minimized evidence needed to support claims.

### 7. Security Marker Path

- Add `SECURITY_PROMPT` only after the expected evidence schema is defined.
- Build a deterministic marker report for shell execution, process spawning, dynamic class loading, native loading, WebView JavaScript bridges, exported component entry points, unsafe deserialization, and network/TLS weaknesses.
- Keep this path bug-bounty-oriented: every issue needs triggerability notes, affected component or call path, exploit preconditions, and confidence.
- Avoid claiming arbitrary code execution unless a reviewed source slice or dynamic test shows a controllable path into execution.

## Definition of Done

The repo is ready for publication when:

- `task check` passes.
- `task test` passes.
- `task path1-check` passes for the selected Androguard report.
- `task analyze` can regenerate `tik_tok_report.json` from the APK.
- `task dashboard` renders the regenerated report without schema mismatches.
- `task corpus-stats` and `task privacy-keywords` give reproducible reconstruction triage.
- `task privacy-indication` produces a deterministic first-pass privacy brief for a supplied APK/report pair.
- `task dynamic-plan` produces a runtime validation plan from the static artifacts.
- The final report uses evidence tables with file paths, line numbers, and confidence labels.
- Every high-severity claim is backed by both structured report data and reviewed source-level evidence, or is explicitly labeled as static-only.

## First Milestone Status

The first milestone is implemented when these commands run for the selected APK/report/decompile tree:

1. `task dashboard`
2. `task inventory`
3. `task report-draft`

The remaining manual work after that milestone is to review the selected source slices and replace automated reconstruction notes with hand-checked pseudocode and line citations. If OpenAI credentials are unavailable, use `task report-evidence` to regenerate the deterministic source material without calling a model.

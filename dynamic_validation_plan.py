import argparse
from pathlib import Path

from report_builder import dangerous_permissions, load_json, metadata, unique_items


PERMISSION_VALIDATION = {
    "android.permission.CAMERA": {
        "concern": "Camera access",
        "flows": "Open camera, record video, upload a draft, deny camera and repeat.",
        "traffic": "Media upload metadata, camera mode flags, device/sensor metadata, unexpected background telemetry.",
        "question": "Is camera-related telemetry sent only after a clear camera-facing user action?",
    },
    "android.permission.RECORD_AUDIO": {
        "concern": "Microphone access",
        "flows": "Record video with sound, use live/audio features, deny microphone and repeat.",
        "traffic": "Audio capture metadata, upload requests, feature flags, microphone permission state.",
        "question": "Is microphone-related data sent only during explicit recording or audio flows?",
    },
    "android.permission.READ_CONTACTS": {
        "concern": "Contacts access",
        "flows": "Open friend-finder/contact-sync flows before and after granting contacts.",
        "traffic": "Contact hashes, phone/email hashes, address-book counts, sync endpoints.",
        "question": "Are contacts or contact-derived identifiers transmitted only after consent?",
    },
    "android.permission.ACCESS_FINE_LOCATION": {
        "concern": "Precise location access",
        "flows": "Open location-tagging, nearby, search, ads, and posting flows with location granted and denied.",
        "traffic": "Latitude/longitude, geohash, location accuracy, location permission state.",
        "question": "Is precise location transmitted only for user-visible location features?",
    },
    "android.permission.ACCESS_COARSE_LOCATION": {
        "concern": "Approximate location access",
        "flows": "Launch app, browse feed, search, post content, and compare location granted versus denied.",
        "traffic": "Coarse location, region, city, geohash, IP-derived location labels.",
        "question": "Is approximate location use explained by the active feature or consent state?",
    },
    "android.permission.READ_MEDIA_IMAGES": {
        "concern": "Image library access",
        "flows": "Upload an image from the gallery and compare with a camera-created image.",
        "traffic": "EXIF fields, filenames, media IDs, gallery metadata, upload side-channel metadata.",
        "question": "Is image metadata minimized before upload?",
    },
    "android.permission.READ_MEDIA_VIDEO": {
        "concern": "Video library access",
        "flows": "Upload a video from the gallery and compare with an in-app recording.",
        "traffic": "EXIF/media metadata, filenames, codec metadata, local paths, upload identifiers.",
        "question": "Is video metadata minimized before upload?",
    },
    "android.permission.READ_EXTERNAL_STORAGE": {
        "concern": "External storage read access",
        "flows": "Open media picker, upload gallery media, deny storage/media permissions and repeat.",
        "traffic": "Local paths, filenames, media-library metadata, unexpected file inventory data.",
        "question": "Does traffic avoid leaking local file paths or unrelated storage metadata?",
    },
    "android.permission.WRITE_EXTERNAL_STORAGE": {
        "concern": "External storage write access",
        "flows": "Download media, save drafts, export edited video, then inspect local files and traffic.",
        "traffic": "Saved-file paths, cache identifiers, exported media metadata.",
        "question": "Are written files and related telemetry limited to expected user actions?",
    },
    "android.permission.ACCESS_ADSERVICES_AD_ID": {
        "concern": "Advertising identifier access",
        "flows": "Launch before login, login, browse feed, reset ad ID if possible, compare requests.",
        "traffic": "Advertising ID, app set ID, attribution IDs, ad SDK identifiers, consent fields.",
        "question": "Are advertising identifiers gated by platform policy and consent state?",
    },
    "com.google.android.gms.permission.AD_ID": {
        "concern": "Google advertising identifier access",
        "flows": "Launch before login, login, browse feed, reset ad ID if possible, compare requests.",
        "traffic": "Advertising ID, app set ID, attribution IDs, ad SDK identifiers, consent fields.",
        "question": "Are advertising identifiers gated by platform policy and consent state?",
    },
}


CATEGORY_VALIDATION = {
    "identifiers": {
        "concern": "Device and advertising identifiers",
        "flows": "Cold launch, login, browse feed, open ads, reset advertising ID and repeat.",
        "traffic": "Advertising ID, Android ID, install ID, device ID, session IDs, hashed identifiers.",
        "question": "Which identifiers are transmitted, and are they resettable or user-controllable?",
    },
    "location": {
        "concern": "Location access",
        "flows": "Browse feed, search, post with location, deny location and repeat.",
        "traffic": "Latitude/longitude, geohash, city/region, accuracy, permission state.",
        "question": "Does location traffic match a visible location feature?",
    },
    "camera_microphone": {
        "concern": "Camera and microphone capture",
        "flows": "Record, edit, upload, live/cast if available, deny permissions and repeat.",
        "traffic": "Capture metadata, upload metadata, audio/video feature flags, sensor state.",
        "question": "Is capture-related telemetry limited to explicit capture flows?",
    },
    "contacts_accounts": {
        "concern": "Contacts and accounts",
        "flows": "Find friends, contact sync, invite flows, account-linking flows.",
        "traffic": "Contact hashes, phone/email hashes, account identifiers, sync counts.",
        "question": "Is contact/account data sent only after clear consent?",
    },
    "installed_apps": {
        "concern": "Installed-app or intent query behavior",
        "flows": "Share, login with third parties, open links, install/remove common apps and compare.",
        "traffic": "Package names, app-presence flags, capability probes, intent-resolution results.",
        "question": "Does the app transmit installed-app presence beyond user-triggered integrations?",
    },
    "local_storage": {
        "concern": "Local persistence",
        "flows": "Login, logout, save drafts, change privacy settings, inspect app data on a test device.",
        "traffic": "Tokens or identifiers echoed from local state, cache keys, preference-derived IDs.",
        "question": "Are sensitive local values protected and cleared after logout where appropriate?",
    },
    "network_telemetry": {
        "concern": "Network telemetry",
        "flows": "Launch, idle, browse feed, search, view profile, post content, logout.",
        "traffic": "Event names, tap/scroll telemetry, profile/content IDs, third-party endpoints.",
        "question": "Is telemetry proportionate to the user-visible flow and consent state?",
    },
    "dynamic_loading": {
        "concern": "Dynamic loading",
        "flows": "Launch, login, open media effects, ads, live, payment, and plugin-like features.",
        "traffic": "Downloaded dex/jar/so files, plugin manifests, remote config enabling modules.",
        "question": "Is executable or plugin-like content fetched, verified, and scoped?",
    },
    "command_execution": {
        "concern": "Command execution markers",
        "flows": "Exercise media editing, diagnostics, live/cast, wallet/payment, and export flows.",
        "traffic": "Remote config or parameters that appear to influence local command behavior.",
        "question": "Is command execution reachable, and can any server/client input influence commands?",
    },
}


BASELINE_FLOWS = [
    "Fresh install, first launch, no login.",
    "Login with a test account and capture account bootstrap traffic.",
    "Idle for 5-10 minutes after login.",
    "Browse feed, search, view profile, and open comments/messages if available.",
    "Grant and deny each sensitive permission, repeating the same flow after each change.",
    "Logout, force stop, relaunch, and compare persistent identifiers and post-logout traffic.",
]


def source_categories(source_findings):
    categories = set()
    for finding in (source_findings or {}).get("findings", []):
        categories.update((finding.get("category_counts") or {}).keys())
    return sorted(categories)


def source_evidence_summary(source_findings, category):
    rows = []
    for finding in (source_findings or {}).get("findings", []):
        if category not in (finding.get("category_counts") or {}):
            continue
        rows.append(f"`{finding.get('smali_file')}`")
        if len(rows) >= 3:
            break
    return ", ".join(rows) or "source category signal"


def add_table(lines, headers, rows):
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        lines.append("| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |")


def build_permission_rows(analysis):
    info = metadata(analysis)
    declared_sensitive = dangerous_permissions(info["permissions"])
    rows = []
    for permission, privacy_area in declared_sensitive:
        validation = PERMISSION_VALIDATION.get(permission)
        if not validation:
            continue
        rows.append(
            [
                validation["concern"],
                f"`{permission}` ({privacy_area})",
                validation["flows"],
                validation["traffic"],
                validation["question"],
            ]
        )
    return rows


def build_category_rows(source_findings):
    rows = []
    for category in source_categories(source_findings):
        validation = CATEGORY_VALIDATION.get(category)
        if not validation:
            continue
        rows.append(
            [
                validation["concern"],
                f"`{category}` in {source_evidence_summary(source_findings, category)}",
                validation["flows"],
                validation["traffic"],
                validation["question"],
            ]
        )
    return rows


def build_plan(analysis, source_findings=None):
    info = metadata(analysis)
    exported_components = unique_items(analysis.get("exported_components", []))
    permission_rows = build_permission_rows(analysis)
    category_rows = build_category_rows(source_findings)

    lines = [
        f"# Dynamic Privacy Validation Plan: {info['app_name']}",
        "",
        "## Scope",
        "",
        f"- APK path: `{info['apk_path']}`",
        f"- Package: `{info['package_name']}`",
        f"- Version: `{info['version_name']}` / `{info['version_code']}`",
        f"- Static report input: generated Androguard evidence",
        f"- Source packet input: {'present' if source_findings else 'not supplied'}",
        "",
        "This plan translates static privacy findings into runtime checks. It should be run against a test account and a controlled device or emulator. The goal is to label static concerns as `observed`, `not observed`, or `blocked`, not to infer runtime behavior from code presence alone.",
        "",
        "## Capture Setup",
        "",
        "- Use a spare Android phone or emulator with a clean test account.",
        "- Route device traffic through Burp Suite, mitmproxy, or Charles.",
        "- Install the proxy CA certificate where permitted by the device/app configuration.",
        "- Record app version, APK hash, device model, Android version, region, account state, and permission state.",
        "- Keep raw captures private; publish only minimized evidence needed to support a claim.",
        "",
        "## Baseline Flows",
        "",
    ]
    lines.extend(f"- {flow}" for flow in BASELINE_FLOWS)

    lines.extend(["", "## Permission-Driven Checks", ""])
    if permission_rows:
        add_table(
            lines,
            ["Concern", "Static evidence", "Runtime flow", "Traffic to inspect", "Validation question"],
            permission_rows,
        )
    else:
        lines.append("No high-signal sensitive permissions from the local checklist were found.")

    lines.extend(["", "## Source-Packet-Driven Checks", ""])
    if category_rows:
        add_table(
            lines,
            ["Concern", "Static evidence", "Runtime flow", "Traffic to inspect", "Validation question"],
            category_rows,
        )
    else:
        lines.append("No source finding packets were supplied. Run `task source-findings` to generate targeted runtime checks.")

    lines.extend([
        "",
        "## Exported Component Follow-Up",
        "",
        f"The static report lists {len(exported_components)} exported components. For privacy validation, prioritize components that process links, sharing, login, payment, media capture, or account authorization.",
        "",
    ])
    if exported_components:
        add_table(lines, ["Priority", "Component"], [[index, component] for index, component in enumerate(exported_components[:15], start=1)])
        if len(exported_components) > 15:
            lines.append("")
            lines.append(f"Only the first 15 exported components are listed here; total exported components: {len(exported_components)}.")
    else:
        lines.append("No exported components were found in the structured report.")

    lines.extend([
        "",
        "## Vulnerable Or High-Concern Traffic Patterns",
        "",
        "- Sensitive identifiers or PII in URLs, query strings, referrers, logs, or third-party requests.",
        "- Contacts, phone/email hashes, exact location, media metadata, or installed-app data sent before consent or without a visible related feature.",
        "- Auth tokens, upload URLs, private media URLs, or account identifiers accepted across users or after logout.",
        "- Server responses that expose private, deleted, draft, or account-scoped resources through predictable IDs.",
        "- Remote configuration that changes privacy-sensitive collection without a corresponding local permission or consent state.",
        "- Executable/plugin-like downloads or command parameters that are not clearly integrity-checked.",
        "",
        "## Result Labels",
        "",
        "- `observed`: captured in traffic or device state during a named flow.",
        "- `not observed`: specifically tested in a named flow and not seen.",
        "- `blocked`: not testable because of certificate pinning, login, region gating, feature flags, or missing device capability.",
        "- `needs source review`: static signal exists, but runtime triggerability is unknown.",
        "",
        "## Evidence Template",
        "",
        "| Finding | Flow | Permission state | Endpoint/domain | Data observed | Evidence file | Label | Notes |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
        "|  |  |  |  |  |  |  |  |",
    ])

    return "\n".join(lines).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description="Build a dynamic privacy validation plan from static APK evidence.")
    parser.add_argument("-a", "--analysis", default="apk_analysis_report.json", help="Androguard JSON report path")
    parser.add_argument("-s", "--source-findings", default=None, help="Optional source findings JSON path")
    parser.add_argument("-o", "--output", default="dynamic_privacy_validation_plan.md", help="Markdown output path")
    args = parser.parse_args()

    analysis = load_json(args.analysis)
    source_findings = load_json(args.source_findings) if args.source_findings else None
    Path(args.output).write_text(build_plan(analysis, source_findings))
    print(f"Dynamic privacy validation plan saved to: {args.output}")


if __name__ == "__main__":
    main()

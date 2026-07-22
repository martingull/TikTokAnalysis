import argparse
import json
from pathlib import Path


DANGEROUS_PERMISSION_NOTES = {
    "android.permission.ACCESS_FINE_LOCATION": "precise location",
    "android.permission.ACCESS_COARSE_LOCATION": "approximate location",
    "android.permission.CAMERA": "camera",
    "android.permission.RECORD_AUDIO": "microphone",
    "android.permission.READ_CONTACTS": "contacts",
    "android.permission.READ_MEDIA_IMAGES": "images",
    "android.permission.READ_MEDIA_VIDEO": "videos",
    "android.permission.READ_MEDIA_AUDIO": "audio",
    "android.permission.READ_EXTERNAL_STORAGE": "external storage",
    "android.permission.WRITE_EXTERNAL_STORAGE": "external storage writes",
    "android.permission.POST_NOTIFICATIONS": "notifications",
    "android.permission.BLUETOOTH_CONNECT": "nearby Bluetooth devices",
    "android.permission.ACCESS_ADSERVICES_AD_ID": "advertising identifier",
    "com.google.android.gms.permission.AD_ID": "Google advertising identifier",
}


def load_json(path):
    return json.loads(Path(path).read_text())


def metadata(report):
    nested = report.get("metadata", {})
    return {
        "app_name": report.get("app_name") or nested.get("App Name") or "Unknown app",
        "package_name": report.get("package_name") or nested.get("Package Name") or "unknown.package",
        "version_name": report.get("version_name") or nested.get("Version Name") or "unknown",
        "version_code": report.get("version_code") or nested.get("Version Code") or "unknown",
        "apk_path": report.get("apk_path") or "unknown",
        "permissions": report.get("permissions") or nested.get("Permissions", []),
        "main_activity": nested.get("Main Activity"),
        "target_sdk": nested.get("Target SDK"),
        "min_sdk": nested.get("Min SDK"),
    }


def component_counts(report):
    nested = report.get("metadata", {})
    return report.get("component_counts") or {
        "permissions": len(report.get("permissions") or nested.get("Permissions", [])),
        "activities": len(nested.get("Activities", [])),
        "services": len(nested.get("Services", [])),
        "broadcast_receivers": len(nested.get("Broadcast Receivers", [])),
        "content_providers": len(nested.get("Content Providers", [])),
    }


def dangerous_permissions(perms):
    return [(perm, DANGEROUS_PERMISSION_NOTES[perm]) for perm in sorted(set(perms)) if perm in DANGEROUS_PERMISSION_NOTES]


def unique_items(items):
    return sorted(set(items or []))


def normalize_permission_api_entry(data):
    if isinstance(data, dict):
        return {
            "declared": data.get("declared"),
            "references": unique_items(data.get("references", [])),
        }
    return {
        "declared": None,
        "references": unique_items(data),
    }


def source_packet_rows(source_findings, limit=8):
    rows = []
    for finding in (source_findings or {}).get("findings", [])[:limit]:
        evidence_lines = [
            f"{context.get('line')}:{context.get('category')}:{context.get('keyword')}"
            for context in finding.get("smali_context", [])[:3]
        ]
        rows.append(
            [
                finding.get("priority", ""),
                finding.get("smali_file", ""),
                finding.get("class_name") or "unknown",
                finding.get("jadx_file") or "not supplied",
                ", ".join(finding.get("category_counts", {}).keys()),
                ", ".join(evidence_lines) or "none",
            ]
        )
    return rows


def source_packet_excerpt(finding, max_contexts=2, max_jadx=2):
    lines = [
        f"#### `{finding.get('smali_file', 'unknown')}`",
        "",
        f"- Class: `{finding.get('class_name') or 'unknown'}`",
        f"- JADX source: `{finding.get('jadx_file') or 'not supplied'}`",
        f"- Categories: {', '.join(f'`{name}`' for name in finding.get('category_counts', {})) or '`none`'}",
        "",
    ]

    smali_contexts = finding.get("smali_context", [])[:max_contexts]
    if smali_contexts:
        lines.append("Smali evidence:")
        for context in smali_contexts:
            center_line = next(
                (
                    row["code"].strip()
                    for row in context.get("context", [])
                    if row.get("line") == context.get("line")
                ),
                "",
            )
            lines.append(
                f"- Line {context.get('line')}, `{context.get('category')}`, `{context.get('keyword')}`: `{short_text(center_line)}`"
            )
        lines.append("")

    jadx_matches = finding.get("jadx_matches", [])[:max_jadx]
    if jadx_matches:
        lines.append("JADX reading context:")
        for match in jadx_matches:
            lines.append(f"- Line {match.get('line')}: `{short_text(match.get('code', ''))}`")
        lines.append("")

    return lines


def certificate_summary(report):
    certificate = report.get("certificate_info", {})
    certificates = certificate.get("certificates", [])
    first_certificate = certificates[0] if certificates else {}
    return {
        "is_signed": certificate.get("is_signed", certificate.get("Is signed")),
        "is_signed_v1": certificate.get("is_signed_v1"),
        "is_signed_v2": certificate.get("is_signed_v2"),
        "is_signed_v3": certificate.get("is_signed_v3"),
        "certificate_count": len(certificates) or len(certificate.get("Signatures", [])),
        "subject": first_certificate.get("subject"),
        "issuer": first_certificate.get("issuer"),
        "not_valid_before": first_certificate.get("not_valid_before"),
        "not_valid_after": first_certificate.get("not_valid_after"),
        "sha1": first_certificate.get("sha1"),
        "sha256": first_certificate.get("sha256"),
    }


def evidence_grade(label, source, confidence):
    return f"**Evidence grade:** {label}. **Source:** {source}. **Confidence:** {confidence}."


def add_table(lines, headers, rows):
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        lines.append("| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |")


def short_text(value, limit=280):
    text = " ".join(str(value or "").split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def build_report(analysis, inventory=None, source_findings=None):
    info = metadata(analysis)
    counts = component_counts(analysis)
    exported_components = unique_items(analysis.get("exported_components", []))
    suspicious = {
        category: unique_items(methods)
        for category, methods in analysis.get("suspicious_behavior", {}).items()
    }
    permission_api_map = {
        permission: normalize_permission_api_entry(data)
        for permission, data in analysis.get("permission_api_map", {}).items()
    }
    cert = certificate_summary(analysis)
    dangerous = dangerous_permissions(info["permissions"])
    selected_slices = (inventory or {}).get("selected_source_slices", [])
    source_packets = (source_findings or {}).get("findings", [])

    lines = [
        f"# Android APK Privacy Assessment: {info['app_name']}",
        "",
        "## Scope",
        "",
        f"- APK path: `{info['apk_path']}`",
        f"- Package: `{info['package_name']}`",
        f"- Version: `{info['version_name']}` / `{info['version_code']}`",
        f"- Main activity: `{info['main_activity']}`",
        f"- SDK range: min `{info['min_sdk']}`, target `{info['target_sdk']}`",
        "",
        "This report is written for arbitrary consumer Android APKs, including TikTok, Snapchat, Instagram, or similar social apps. The working premise is that modern consumer tech can be intrusive, but every claim below is limited to the evidence found in the analyzed APK.",
        "",
        "## Executive Summary",
        "",
        f"The APK declares {counts.get('permissions', len(info['permissions']))} permissions and {len(exported_components)} exported components. Static analysis found privacy-relevant API references and source-reconstruction targets, but no dynamic runtime testing has been performed in this milestone.",
        "",
        "The strongest publishable claims at this stage are capability and code-presence claims. Runtime collection, transmission, and user-flow triggering still need dynamic validation before they are described as observed behavior.",
        "",
        "## Evidence Model",
        "",
        "- Declared permission: capability appears in the manifest; this does not prove collection.",
        "- Static API reference: bytecode or smali references an API; this does not prove a user flow triggers it.",
        "- Source reconstruction: a smali class has been selected for readable reconstruction because it supports a finding.",
        "- Source finding packet: line-cited smali evidence and optional JADX reading context have been extracted for review.",
        "- Runtime behavior: not assessed in this milestone.",
        "",
        "## App Surface",
        "",
    ]

    add_table(
        lines,
        ["Metric", "Count"],
        [
            ["Permissions", counts.get("permissions", len(info["permissions"]))],
            ["Activities", counts.get("activities", 0)],
            ["Services", counts.get("services", 0)],
            ["Broadcast receivers", counts.get("broadcast_receivers", 0)],
            ["Content providers", counts.get("content_providers", 0)],
            ["Exported components", len(exported_components)],
        ],
    )

    lines.extend(["", "## Findings", ""])

    lines.extend(["### Certificate And Signing", ""])
    lines.append(evidence_grade("APK signing metadata", "Androguard certificate extraction", "high"))
    lines.append("")
    add_table(
        lines,
        ["Field", "Value"],
        [
            ["Signed", cert["is_signed"]],
            ["V1 signature", cert["is_signed_v1"]],
            ["V2 signature", cert["is_signed_v2"]],
            ["V3 signature", cert["is_signed_v3"]],
            ["Certificate count", cert["certificate_count"]],
            ["Subject", cert["subject"] or "not available in this report schema"],
            ["Issuer", cert["issuer"] or "not available in this report schema"],
            ["Valid from", cert["not_valid_before"] or "not available in this report schema"],
            ["Valid until", cert["not_valid_after"] or "not available in this report schema"],
            ["SHA-256", cert["sha256"] or "not available in this report schema"],
        ],
    )
    lines.extend([
        "",
        "Certificate metadata identifies the APK signer and helps compare whether two APK samples share the same signing lineage. It is not, by itself, proof that the analyzed APK came from an official app store channel.",
        "",
    ])

    lines.extend([
        "### Sensitive Permissions",
        "",
        evidence_grade("declared permission", "AndroidManifest.xml via Androguard report", "high"),
        "",
    ])
    if dangerous:
        add_table(lines, ["Permission", "Privacy area"], dangerous)
    else:
        lines.append("No high-signal dangerous permissions from the local checklist were found.")

    lines.extend(["", "### Exported Components", ""])
    lines.append(evidence_grade("manifest declaration", "Androguard exported component extraction", "medium"))
    lines.append("")
    if exported_components:
        add_table(lines, ["Component"], [[item] for item in exported_components[:25]])
        if len(exported_components) > 25:
            lines.append("")
            lines.append(f"Only the first 25 exported components are shown here; total exported components: {len(exported_components)}.")
    else:
        lines.append("No exported components were found in the structured report.")

    lines.extend(["", "### Static API Signals", ""])
    lines.append(evidence_grade("static API reference", "Androguard bytecode analysis", "medium"))
    lines.append("")
    rows = []
    for category, methods in suspicious.items():
        rows.append([category, len(methods), ", ".join(methods[:5])])
    if rows:
        add_table(lines, ["Category", "Unique references", "Examples"], rows)
    else:
        lines.append("No suspicious API references were found in the structured report.")

    lines.extend(["", "### Permission-To-API Mapping", ""])
    lines.append(evidence_grade("static API reference", "Androguard permission/API map", "medium"))
    lines.append("")
    if permission_api_map:
        add_table(
            lines,
            ["Permission", "Declared in manifest", "Mapped references"],
            [
                [
                    permission,
                    "unknown" if data["declared"] is None else data["declared"],
                    ", ".join(data["references"]),
                ]
                for permission, data in permission_api_map.items()
            ],
        )
    else:
        lines.append("No permission/API mappings were found in the structured report.")

    lines.extend(["", "## Source Reconstruction Targets", ""])
    lines.append(evidence_grade("source reconstruction shortlist", "privacy keyword inventory over decompiled smali", "medium"))
    lines.append("")
    if selected_slices:
        add_table(
            lines,
            ["File", "Class", "Categories", "Matches"],
            [
                [
                    item["file"],
                    item.get("class_name") or "unknown",
                    ", ".join(item.get("category_counts", {}).keys()),
                    item.get("total_matches", 0),
                ]
                for item in selected_slices
            ],
        )
    else:
        lines.append("No reconstruction inventory was supplied.")

    lines.extend(["", "## Source Finding Packets", ""])
    lines.append(evidence_grade("line-cited static source evidence", "apktool smali with optional JADX context", "medium"))
    lines.append("")
    packet_rows = source_packet_rows(source_findings)
    if packet_rows:
        add_table(
            lines,
            ["Priority", "Smali file", "Class", "JADX source", "Categories", "Evidence lines"],
            packet_rows,
        )
        lines.append("")
        lines.append("The excerpts below are review aids. Publishable claims still need human confirmation of control flow and triggerability.")
        lines.append("")
        for finding in source_packets[:3]:
            lines.extend(source_packet_excerpt(finding))
    else:
        lines.append("No source finding packets were supplied. Run `task source-findings` after `task inventory` to add line-cited source context.")

    lines.extend([
        "",
        "## Methodology",
        "",
        "1. Androguard parsed the APK metadata, manifest-derived surfaces, and selected bytecode API references.",
        "2. apktool output was scanned for privacy-relevant smali keywords.",
        "3. The reconstruction inventory selected a small set of high-signal source slices from a very large decompiled corpus.",
        "4. Source finding packets added line-cited smali context and optional JADX reading context where available.",
        "5. Findings were labeled by evidence type to avoid overstating static analysis as runtime proof.",
        "",
        "## Limitations",
        "",
        "- Static analysis can miss behavior hidden behind obfuscation, native code, encrypted strings, feature flags, or server-controlled paths.",
        "- Static analysis can also overstate risk when a referenced API is unreachable, dead code, guarded by consent checks, or only used by third-party SDK internals.",
        "- No dynamic analysis, network interception, account login, or device-flow testing is included in this milestone.",
        "",
        "## Next Steps",
        "",
        "- Manually reconstruct the selected source slices into readable pseudocode with file and line citations.",
        "- Add dynamic validation for the highest-impact findings.",
        "- Compare findings across additional APKs, such as Snapchat and Instagram, using the same evidence model.",
    ])

    return "\n".join(lines).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description="Build an evidence-labeled APK privacy report from structured analysis artifacts.")
    parser.add_argument("-a", "--analysis", default="apk_analysis_report.json", help="Androguard JSON report path")
    parser.add_argument("-i", "--inventory", default=None, help="Optional reconstruction inventory JSON path")
    parser.add_argument("-s", "--source-findings", default=None, help="Optional source findings JSON path")
    parser.add_argument("-o", "--output", default="privacy_assessment_report.md", help="Markdown report output path")
    args = parser.parse_args()

    analysis = load_json(args.analysis)
    inventory = load_json(args.inventory) if args.inventory else None
    source_findings = load_json(args.source_findings) if args.source_findings else None
    Path(args.output).write_text(build_report(analysis, inventory, source_findings))
    print(f"Privacy assessment report saved to: {args.output}")


if __name__ == "__main__":
    main()

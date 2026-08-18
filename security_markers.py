import argparse
import json
import re
import shutil
import subprocess
import tempfile
from collections import Counter, defaultdict
from pathlib import Path


MARKER_CATEGORIES = {
    "command_execution": {
        "severity": "high",
        "markers": [
            {"label": "Runtime.exec", "needle": "Ljava/lang/Runtime;->exec("},
            {"label": "ProcessBuilder.start", "needle": "Ljava/lang/ProcessBuilder;->start("},
        ],
        "review_focus": "Determine whether command arguments are fixed or attacker-controlled.",
    },
    "dynamic_code_loading": {
        "severity": "high",
        "markers": [
            {"label": "DexClassLoader", "regex": r"\bDexClassLoader\b"},
            {"label": "PathClassLoader", "regex": r"\bPathClassLoader\b"},
            {"label": "InMemoryDexClassLoader", "regex": r"\bInMemoryDexClassLoader\b"},
            {"label": "BaseDexClassLoader", "regex": r"\bBaseDexClassLoader\b"},
            {"label": "ClassLoader.loadClass", "needle": "Ljava/lang/ClassLoader;->loadClass("},
        ],
        "review_focus": "Identify source of loaded code, integrity checks, and writable directories.",
    },
    "native_loading": {
        "severity": "medium-high",
        "markers": [
            {"label": "System.loadLibrary", "needle": "Ljava/lang/System;->loadLibrary("},
            {"label": "System.load", "needle": "Ljava/lang/System;->load("},
            {"label": "Runtime.loadLibrary", "needle": "Ljava/lang/Runtime;->loadLibrary("},
            {"label": "Runtime.load", "needle": "Ljava/lang/Runtime;->load("},
            {"label": "native method", "needle": " native ", "regex": r"^\.method\b.*\bnative\b"},
        ],
        "review_focus": "Map Java/JNI boundaries and decide whether native libraries need Ghidra review.",
    },
    "reflection": {
        "severity": "medium",
        "markers": [
            {"label": "Class.forName", "needle": "Ljava/lang/Class;->forName("},
            {"label": "Method.invoke", "needle": "Ljava/lang/reflect/Method;->invoke("},
            {"label": "Field.get", "needle": "Ljava/lang/reflect/Field;->get("},
            {"label": "Field.set", "needle": "Ljava/lang/reflect/Field;->set("},
            {"label": "Constructor.newInstance", "needle": "Ljava/lang/reflect/Constructor;->newInstance("},
        ],
        "review_focus": "Check whether reflection targets come from constants, configuration, or external input.",
    },
    "webview_bridge": {
        "severity": "high",
        "markers": [
            {"label": "addJavascriptInterface", "needle": "->addJavascriptInterface("},
            {"label": "setJavaScriptEnabled", "needle": "->setJavaScriptEnabled("},
            {"label": "WebViewClient", "regex": r"\bWebViewClient\b"},
            {"label": "shouldOverrideUrlLoading", "needle": "shouldOverrideUrlLoading("},
        ],
        "review_focus": "Review bridge exposure, trusted origins, URL validation, and exported entry points.",
    },
    "tls_trust": {
        "severity": "high",
        "markers": [
            {"label": "X509TrustManager", "regex": r"\bX509TrustManager\b"},
            {"label": "checkServerTrusted", "needle": "checkServerTrusted("},
            {"label": "HostnameVerifier", "regex": r"\bHostnameVerifier\b"},
            {"label": "setHostnameVerifier", "needle": "->setHostnameVerifier("},
            {"label": "setSSLSocketFactory", "needle": "->setSSLSocketFactory("},
            {"label": "TrustManager", "regex": r"\bTrustManager\b"},
        ],
        "review_focus": "Look for trust-all behavior, hostname bypasses, and custom certificate validation.",
    },
    "file_uri_content": {
        "severity": "medium",
        "markers": [
            {"label": "FileProvider", "regex": r"\bFileProvider\b"},
            {"label": "ContentProvider", "regex": r"\bContentProvider\b"},
            {"label": "openFile", "needle": "->openFile("},
            {"label": "openAssetFile", "needle": "->openAssetFile("},
            {"label": "grantUriPermission", "needle": "->grantUriPermission("},
            {"label": "FLAG_GRANT_READ_URI_PERMISSION", "needle": "FLAG_GRANT_READ_URI_PERMISSION"},
            {"label": "FLAG_GRANT_WRITE_URI_PERMISSION", "needle": "FLAG_GRANT_WRITE_URI_PERMISSION"},
        ],
        "review_focus": "Review content/file URI exposure and caller permission checks.",
    },
    "intent_entrypoints": {
        "severity": "medium",
        "markers": [
            {"label": "Activity.getIntent", "needle": "Landroid/app/Activity;->getIntent("},
            {"label": "Intent.getData", "needle": "Landroid/content/Intent;->getData("},
            {"label": "Intent.getExtras", "needle": "Landroid/content/Intent;->getExtras("},
            {"label": "startActivityForResult", "needle": "->startActivityForResult("},
            {"label": "onActivityResult", "needle": "onActivityResult("},
        ],
        "review_focus": "Correlate with exported components and deep links before making bug claims.",
    },
}

CATEGORY_WEIGHTS = {
    "command_execution": 12,
    "dynamic_code_loading": 11,
    "webview_bridge": 10,
    "tls_trust": 10,
    "native_loading": 8,
    "file_uri_content": 7,
    "reflection": 5,
    "intent_entrypoints": 3,
}

CATEGORY_REVIEW_ORDER = [
    "command_execution",
    "dynamic_code_loading",
    "webview_bridge",
    "tls_trust",
    "native_loading",
    "file_uri_content",
    "reflection",
    "intent_entrypoints",
]


def load_json(path):
    return json.loads(Path(path).read_text())


def flatten_keywords():
    pairs = []
    for category, details in MARKER_CATEGORIES.items():
        for marker in details["markers"]:
            marker = dict(marker)
            marker["category"] = category
            if "needle" not in marker:
                marker["needle"] = marker["label"]
            if "regex" in marker:
                marker["compiled_regex"] = re.compile(marker["regex"])
            pairs.append(marker)
    return pairs


def class_name_from_line(line):
    parts = line.strip().split()
    if len(parts) < 2:
        return None
    return parts[-1].strip(";")


def find_candidate_files(decompile_dir):
    if shutil.which("rg") is None:
        return sorted(decompile_dir.rglob("*.smali"))

    keywords = [marker["needle"] for marker in flatten_keywords()]
    with tempfile.NamedTemporaryFile("w", delete=False) as pattern_file:
        pattern_path = Path(pattern_file.name)
        pattern_file.write("\n".join(keywords))

    try:
        result = subprocess.run(
            ["rg", "-l", "-F", "-f", str(pattern_path), str(decompile_dir), "-g", "*.smali"],
            check=False,
            capture_output=True,
            text=True,
        )
    finally:
        pattern_path.unlink(missing_ok=True)

    if result.returncode not in (0, 1):
        raise SystemExit(result.stderr.strip() or "ripgrep marker discovery failed")

    return sorted(Path(line) for line in result.stdout.splitlines() if line.strip())


def marker_matches_line(marker, line, stripped):
    if "compiled_regex" in marker:
        return marker["compiled_regex"].search(stripped) is not None
    return marker["needle"] in line


def scan_file(path, decompile_dir, markers, max_findings):
    relative_path = str(path.relative_to(decompile_dir))
    category_counts = Counter()
    keyword_counts = Counter()
    findings = []
    class_name = None
    current_method = None

    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if stripped.startswith(".class "):
                class_name = class_name_from_line(stripped)
            elif stripped.startswith(".method "):
                current_method = stripped
            elif stripped.startswith(".end method"):
                current_method = None

            for marker in markers:
                if not marker_matches_line(marker, line, stripped):
                    continue
                category = marker["category"]
                keyword = marker["label"]
                category_counts[category] += 1
                keyword_counts[keyword] += 1
                if len(findings) < max_findings:
                    findings.append(
                        {
                            "line": line_number,
                            "category": category,
                            "keyword": keyword,
                            "method": current_method,
                            "code": stripped,
                        }
                    )

    if not keyword_counts:
        return None

    weighted_score = sum(
        category_counts[category] * CATEGORY_WEIGHTS.get(category, 1)
        for category in category_counts
    )

    return {
        "file": relative_path,
        "class_name": class_name,
        "weighted_score": weighted_score,
        "total_matches": sum(keyword_counts.values()),
        "category_counts": dict(sorted(category_counts.items())),
        "keyword_counts": dict(sorted(keyword_counts.items())),
        "findings": findings,
        "triage": {
            "triggerability": "unknown",
            "review_status": "needs source review",
            "claim_boundary": "static marker only; not a vulnerability until input control and reachable flow are shown",
        },
    }


def exported_components(analysis):
    return sorted(set(analysis.get("exported_components", []) or []))


def select_marker_files(records, limit, per_category=3):
    selected = []
    selected_files = set()

    for category in CATEGORY_REVIEW_ORDER:
        candidates = [
            item for item in records
            if category in item["category_counts"] and item["file"] not in selected_files
        ]
        candidates.sort(
            key=lambda item: (
                item["category_counts"].get(category, 0),
                item["weighted_score"],
                item["total_matches"],
                item["file"],
            ),
            reverse=True,
        )
        for item in candidates[:per_category]:
            selected.append(item)
            selected_files.add(item["file"])
            if len(selected) >= limit:
                return selected

    for item in records:
        if item["file"] in selected_files:
            continue
        selected.append(item)
        selected_files.add(item["file"])
        if len(selected) >= limit:
            break

    return selected


def scan_security_markers(analysis, decompile_dir, limit, max_findings):
    keywords = flatten_keywords()
    candidate_paths = find_candidate_files(decompile_dir)
    records = []
    category_totals = Counter()
    category_files = defaultdict(int)
    keyword_totals = Counter()

    for path in candidate_paths:
        record = scan_file(path, decompile_dir, keywords, max_findings)
        if not record:
            continue
        records.append(record)
        category_totals.update(record["category_counts"])
        keyword_totals.update(record["keyword_counts"])
        for category in record["category_counts"]:
            category_files[category] += 1

    records.sort(
        key=lambda item: (item["weighted_score"], item["total_matches"], item["file"]),
        reverse=True,
    )

    components = exported_components(analysis)
    return {
        "analysis_schema_version": "security-markers-v1",
        "apk_path": analysis.get("apk_path"),
        "package_name": analysis.get("package_name") or analysis.get("metadata", {}).get("Package Name"),
        "version_name": analysis.get("version_name") or analysis.get("metadata", {}).get("Version Name"),
        "decompile_dir": str(decompile_dir),
        "evidence_model": {
            "marker": "static code or manifest signal",
            "not_proof_of": "triggerability, exploitability, malicious intent, or runtime behavior",
            "next_step": "manual source review and dynamic validation for reachable, input-controlled paths",
        },
        "categories": {
            category: {
                "severity": details["severity"],
                "review_focus": details["review_focus"],
                "total_matches": category_totals.get(category, 0),
                "file_count": category_files.get(category, 0),
            }
            for category, details in MARKER_CATEGORIES.items()
        },
        "keyword_totals": dict(sorted(keyword_totals.items())),
        "candidate_file_count": len(candidate_paths),
        "file_count_with_markers": len(records),
        "exported_components": components,
        "exported_component_count": len(components),
        "selection_strategy": {
            "order": CATEGORY_REVIEW_ORDER,
            "per_category_first_pass": 3,
            "then": "highest weighted score until limit",
        },
        "selected_files": select_marker_files(records, limit),
    }


def add_table(lines, headers, rows):
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        lines.append("| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |")


def short_text(value, limit=180):
    text = " ".join(str(value or "").split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def write_markdown(payload, output_path, component_limit):
    lines = [
        "# Security Marker Triage",
        "",
        "This artifact is a deterministic static triage layer. It identifies security-relevant markers for review, but it does not claim exploitability.",
        "",
        "## Scope",
        "",
        f"- APK path: `{payload.get('apk_path') or 'unknown'}`",
        f"- Package: `{payload.get('package_name') or 'unknown'}`",
        f"- Version: `{payload.get('version_name') or 'unknown'}`",
        f"- Decompiled directory: `{payload['decompile_dir']}`",
        "",
        "## Evidence Model",
        "",
        "- Marker: static code or manifest signal.",
        "- Triggerability: unknown until a reachable flow and input source are reviewed.",
        "- Vulnerability: not claimed unless manual review or dynamic testing shows control, impact, and preconditions.",
        "",
        "## Marker Categories",
        "",
    ]

    category_rows = []
    for category, details in payload["categories"].items():
        category_rows.append(
            [
                category,
                details["severity"],
                details["total_matches"],
                details["file_count"],
                details["review_focus"],
            ]
        )
    add_table(lines, ["Category", "Severity", "Matches", "Files", "Review focus"], category_rows)

    lines.extend(
        [
            "",
            "## Exported Components",
            "",
            f"Exported component count: `{payload['exported_component_count']}`",
            "",
        ]
    )
    component_rows = [[component] for component in payload["exported_components"][:component_limit]]
    if component_rows:
        add_table(lines, ["Component"], component_rows)
    else:
        lines.append("No exported components were supplied in the analysis report.")

    lines.extend(["", "## Selected Marker Files", ""])
    selected_rows = []
    for item in payload["selected_files"]:
        selected_rows.append(
            [
                item["file"],
                item.get("class_name") or "unknown",
                item["weighted_score"],
                item["total_matches"],
                ", ".join(item["category_counts"]),
            ]
        )
    if selected_rows:
        add_table(lines, ["File", "Class", "Score", "Matches", "Categories"], selected_rows)
    else:
        lines.append("No marker files were found.")

    lines.extend(["", "## Review Packets", ""])
    for item in payload["selected_files"]:
        lines.extend(
            [
                f"### `{item['file']}`",
                "",
                f"- Class: `{item.get('class_name') or 'unknown'}`",
                f"- Categories: {', '.join(f'`{name}`' for name in item['category_counts'])}",
                f"- Triggerability: `{item['triage']['triggerability']}`",
                f"- Claim boundary: {item['triage']['claim_boundary']}",
                "",
                "Findings:",
            ]
        )
        for finding in item["findings"]:
            method = finding.get("method") or "unknown method"
            lines.append(
                f"- Line {finding['line']}, `{finding['category']}`, `{finding['keyword']}`, `{method}`: `{short_text(finding['code'])}`"
            )
        lines.append("")

    lines.extend(
        [
            "## Next Review Steps",
            "",
            "1. Start with `command_execution`, `dynamic_code_loading`, `webview_bridge`, and `tls_trust` packets.",
            "2. For each packet, determine whether inputs are fixed, app-controlled, remotely configured, or externally attacker-controlled.",
            "3. Correlate risky markers with exported components and deep links before making bug-bounty-style claims.",
            "4. Escalate native-library findings to Ghidra only when Java/smali evidence points into JNI or `.so` behavior that affects privacy or security.",
            "5. Record reviewed conclusions separately from this generated marker output.",
            "",
        ]
    )

    output_path.write_text("\n".join(lines).rstrip() + "\n")


def main():
    parser = argparse.ArgumentParser(description="Generate deterministic security marker triage from APK analysis and apktool smali.")
    parser.add_argument("-a", "--analysis", default="tik_tok_report.json", help="Androguard JSON report path")
    parser.add_argument("-d", "--decompile-dir", default="tiktok_decompiled", help="apktool decompiled directory")
    parser.add_argument("-o", "--output", default="security_markers.json", help="JSON output path")
    parser.add_argument("-m", "--markdown", default="security_markers.md", help="Markdown output path")
    parser.add_argument("--limit", type=int, default=30, help="Maximum marker files to include")
    parser.add_argument("--max-findings", type=int, default=8, help="Maximum line findings per selected file")
    parser.add_argument("--component-limit", type=int, default=60, help="Maximum exported components to include in Markdown")
    args = parser.parse_args()

    analysis_path = Path(args.analysis)
    decompile_dir = Path(args.decompile_dir)
    if not analysis_path.is_file():
        raise SystemExit(f"Analysis JSON not found: {analysis_path}")
    if not decompile_dir.is_dir():
        raise SystemExit(f"apktool decompiled directory not found: {decompile_dir}")

    payload = scan_security_markers(load_json(analysis_path), decompile_dir, args.limit, args.max_findings)
    Path(args.output).write_text(json.dumps(payload, indent=2))
    write_markdown(payload, Path(args.markdown), args.component_limit)
    print(f"Security markers JSON saved to: {args.output}")
    print(f"Security markers markdown saved to: {args.markdown}")


if __name__ == "__main__":
    main()

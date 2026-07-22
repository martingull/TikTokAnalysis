import argparse
import json
import shutil
import subprocess
import tempfile
from collections import Counter, defaultdict
from pathlib import Path


KEYWORD_CATEGORIES = {
    "identifiers": [
        "getDeviceId",
        "getSubscriberId",
        "getSimSerialNumber",
        "getMacAddress",
        "getAdvertisingIdInfo",
        "AdvertisingId",
        "android_id",
    ],
    "location": [
        "getLastKnownLocation",
        "getLatitude",
        "getLongitude",
        "LocationManager",
        "ACCESS_FINE_LOCATION",
        "ACCESS_COARSE_LOCATION",
    ],
    "camera_microphone": [
        "Camera;->open",
        "android.permission.CAMERA",
        "MediaRecorder;->start",
        "AudioRecord",
        "RECORD_AUDIO",
    ],
    "contacts_accounts": [
        "READ_CONTACTS",
        "getAccounts",
        "AccountManager",
        "ContactsContract",
    ],
    "installed_apps": [
        "getInstalledPackages",
        "queryIntentActivities",
        "QUERY_ALL_PACKAGES",
    ],
    "local_storage": [
        "SharedPreferences",
        "SQLiteDatabase",
        "openOrCreateDatabase",
        "WRITE_EXTERNAL_STORAGE",
        "READ_EXTERNAL_STORAGE",
    ],
    "network_telemetry": [
        "okhttp",
        "retrofit",
        "HttpURLConnection",
        "Appsflyer",
        "Firebase",
        "analytics",
        "ad_id",
    ],
    "dynamic_loading": [
        "DexClassLoader",
        "PathClassLoader",
        "ClassLoader",
        "Method;->invoke",
        "System.loadLibrary",
    ],
    "command_execution": [
        "Runtime;->exec",
        "ProcessBuilder;->start",
    ],
}

CATEGORY_WEIGHTS = {
    "identifiers": 10,
    "location": 9,
    "camera_microphone": 9,
    "contacts_accounts": 8,
    "installed_apps": 8,
    "dynamic_loading": 7,
    "command_execution": 7,
    "network_telemetry": 5,
    "local_storage": 3,
}


def flatten_keywords():
    keywords = []
    for category, values in KEYWORD_CATEGORIES.items():
        for value in values:
            keywords.append((category, value))
    return keywords


def class_name_from_line(line):
    parts = line.strip().split()
    if len(parts) < 2:
        return None
    return parts[-1].strip(";")


def scan_file(path, decompile_dir, keywords):
    relative_path = str(path.relative_to(decompile_dir))
    file_counts = Counter()
    category_counts = Counter()
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

            for category, keyword in keywords:
                if keyword in line:
                    file_counts[keyword] += 1
                    category_counts[category] += 1
                    if len(findings) < 40:
                        findings.append(
                            {
                                "line": line_number,
                                "category": category,
                                "keyword": keyword,
                                "method": current_method,
                                "code": stripped,
                            }
                        )

    if not file_counts:
        return None

    weighted_score = sum(
        category_counts[category] * CATEGORY_WEIGHTS.get(category, 1)
        for category in category_counts
    )

    return {
        "file": relative_path,
        "class_name": class_name,
        "weighted_score": weighted_score,
        "total_matches": sum(file_counts.values()),
        "keyword_counts": dict(sorted(file_counts.items())),
        "category_counts": dict(sorted(category_counts.items())),
        "findings": findings,
    }


def scan_decompiled_tree(decompile_dir):
    keywords = flatten_keywords()
    candidate_paths = find_candidate_files(decompile_dir)
    records = []
    totals = Counter()
    category_totals = Counter()

    for path in candidate_paths:
        record = scan_file(path, decompile_dir, keywords)
        if not record:
            continue
        records.append(record)
        totals.update(record["keyword_counts"])
        category_totals.update(record["category_counts"])

    records.sort(key=lambda item: (item["weighted_score"], item["total_matches"], item["file"]), reverse=True)

    return {
        "decompile_dir": str(decompile_dir),
        "candidate_file_count": len(candidate_paths),
        "file_count_with_findings": len(records),
        "keyword_totals": dict(sorted(totals.items())),
        "category_totals": dict(sorted(category_totals.items())),
        "files": records,
    }


def find_candidate_files(decompile_dir):
    if shutil.which("rg") is None:
        return sorted(decompile_dir.rglob("*.smali"))

    all_keywords = [keyword for _, keyword in flatten_keywords()]
    with tempfile.NamedTemporaryFile("w", delete=False) as pattern_file:
        pattern_path = Path(pattern_file.name)
        pattern_file.write("\n".join(all_keywords))

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
        raise SystemExit(result.stderr.strip() or "ripgrep candidate discovery failed")

    return sorted(Path(line) for line in result.stdout.splitlines() if line.strip())


def select_source_slices(inventory, max_slices):
    selected = []
    selected_files = set()
    files = inventory["files"]

    for category in KEYWORD_CATEGORIES:
        category_files = [
            item for item in files
            if category in item["category_counts"] and item["file"] not in selected_files
        ]
        category_files.sort(
            key=lambda item: (
                item["category_counts"].get(category, 0),
                item["weighted_score"],
                item["total_matches"],
            ),
            reverse=True,
        )
        if category_files:
            selected.append(category_files[0])
            selected_files.add(category_files[0]["file"])
        if len(selected) >= max_slices:
            return selected

    for item in files:
        if item["file"] in selected_files:
            continue
        selected.append(item)
        selected_files.add(item["file"])
        if len(selected) >= max_slices:
            break

    return selected


def describe_slice(record):
    categories = ", ".join(record["category_counts"])
    class_name = record.get("class_name") or "unknown class"
    return (
        f"`{record['file']}` maps to `{class_name}` and contains static references in "
        f"these categories: {categories}. Treat this as source-reconstruction evidence "
        "that the class participates in these capability areas; runtime triggering still "
        "requires dynamic validation."
    )


def write_markdown(inventory, selected, output_path):
    lines = [
        "# Reconstruction Inventory",
        "",
        "This artifact ranks privacy-relevant smali files for source reconstruction. It is static evidence only.",
        "",
        "## Corpus Summary",
        "",
        f"- Decompiled directory: `{inventory['decompile_dir']}`",
        f"- Candidate smali files from keyword discovery: {inventory['candidate_file_count']}",
        f"- Files with privacy-relevant findings: {inventory['file_count_with_findings']}",
        "",
        "## Category Totals",
        "",
        "| Category | Matches |",
        "| --- | ---: |",
    ]

    for category, count in inventory["category_totals"].items():
        lines.append(f"| `{category}` | {count} |")

    lines.extend([
        "",
        "## Keyword Totals",
        "",
        "| Keyword | Matches |",
        "| --- | ---: |",
    ])

    for keyword, count in inventory["keyword_totals"].items():
        lines.append(f"| `{keyword}` | {count} |")

    lines.extend([
        "",
        "## Source Slices To Reconstruct First",
        "",
    ])

    for index, record in enumerate(selected, start=1):
        lines.extend([
            f"### {index}. `{record['file']}`",
            "",
            f"- Class: `{record.get('class_name') or 'unknown'}`",
            f"- Weighted score: {record['weighted_score']}",
            f"- Total matches: {record['total_matches']}",
            f"- Categories: {', '.join(f'`{name}`' for name in record['category_counts'])}",
            f"- Reconstruction note: {describe_slice(record)}",
            "",
            "| Line | Category | Keyword | Method | Code |",
            "| ---: | --- | --- | --- | --- |",
        ])
        for finding in record["findings"][:10]:
            method = (finding.get("method") or "").replace("|", "\\|")
            code = finding["code"].replace("|", "\\|")
            lines.append(
                f"| {finding['line']} | `{finding['category']}` | `{finding['keyword']}` | `{method}` | `{code}` |"
            )
        lines.append("")

    output_path.write_text("\n".join(lines).rstrip() + "\n")


def write_json(inventory, selected, output_path):
    payload = {
        **inventory,
        "selected_source_slices": selected,
    }
    output_path.write_text(json.dumps(payload, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Build a privacy-focused reconstruction inventory from apktool smali output.")
    parser.add_argument("decompile_dir", help="Path to an apktool decompiled directory")
    parser.add_argument("-o", "--output", default="reconstruction_inventory.json", help="JSON inventory output path")
    parser.add_argument("-m", "--markdown", default="reconstruction_inventory.md", help="Markdown summary output path")
    parser.add_argument("--max-slices", type=int, default=10, help="Number of first-pass source slices to select")
    args = parser.parse_args()

    decompile_dir = Path(args.decompile_dir)
    if not decompile_dir.is_dir():
        raise SystemExit(f"Decompiled directory not found: {decompile_dir}")

    inventory = scan_decompiled_tree(decompile_dir)
    selected = select_source_slices(inventory, args.max_slices)
    write_json(inventory, selected, Path(args.output))
    write_markdown(inventory, selected, Path(args.markdown))
    print(f"Inventory JSON saved to: {args.output}")
    print(f"Inventory markdown saved to: {args.markdown}")


if __name__ == "__main__":
    main()

import argparse
import json
from pathlib import Path


def load_json(path):
    return json.loads(Path(path).read_text())


def smali_class_to_java_path(class_name, jadx_dir):
    if not class_name:
        return None
    normalized = class_name.strip(";")
    if normalized.startswith("L"):
        normalized = normalized[1:]
    return Path(jadx_dir) / "sources" / f"{normalized}.java"


def read_lines(path):
    return path.read_text(encoding="utf-8", errors="ignore").splitlines()


def line_window(lines, center, radius):
    start = max(center - radius, 1)
    end = min(center + radius, len(lines))
    return [
        {
            "line": index,
            "code": lines[index - 1],
        }
        for index in range(start, end + 1)
    ]


def extract_smali_context(decompile_dir, relative_file, findings, radius):
    path = Path(decompile_dir) / relative_file
    if not path.is_file():
        return []

    lines = read_lines(path)
    contexts = []
    for finding in findings:
        contexts.append(
            {
                "line": finding["line"],
                "category": finding["category"],
                "keyword": finding["keyword"],
                "method": finding.get("method"),
                "context": line_window(lines, finding["line"], radius),
            }
        )
    return contexts


def extract_jadx_matches(jadx_path, keywords, max_matches, radius):
    if not jadx_path or not jadx_path.is_file():
        return []

    lines = read_lines(jadx_path)
    matches = []
    for index, line in enumerate(lines, start=1):
        if not any(keyword in line for keyword in keywords):
            continue
        matches.append(
            {
                "line": index,
                "code": line.strip(),
                "context": line_window(lines, index, radius),
            }
        )
        if len(matches) >= max_matches:
            break
    return matches


def selected_slices(inventory, limit):
    slices = inventory.get("selected_source_slices") or inventory.get("files", [])
    return slices[:limit]


def build_findings(inventory, decompile_dir, jadx_dir, limit, context_radius, max_findings):
    output = {
        "decompile_dir": str(decompile_dir),
        "jadx_dir": str(jadx_dir) if jadx_dir else None,
        "strategy": {
            "reading_layer": "JADX Java-like source when available",
            "evidence_layer": "apktool smali with line-numbered context",
            "scope": "selected privacy/security source slices, not whole-app reconstruction",
        },
        "findings": [],
    }

    for index, record in enumerate(selected_slices(inventory, limit), start=1):
        class_name = record.get("class_name")
        jadx_path = smali_class_to_java_path(class_name, jadx_dir) if jadx_dir else None
        findings = record.get("findings", [])[:max_findings]
        keywords = sorted({finding["keyword"] for finding in findings})

        output["findings"].append(
            {
                "priority": index,
                "smali_file": record["file"],
                "class_name": class_name,
                "jadx_file": str(jadx_path) if jadx_path and jadx_path.is_file() else None,
                "category_counts": record.get("category_counts", {}),
                "total_matches": record.get("total_matches", 0),
                "weighted_score": record.get("weighted_score", 0),
                "smali_context": extract_smali_context(
                    decompile_dir,
                    record["file"],
                    findings,
                    context_radius,
                ),
                "jadx_matches": extract_jadx_matches(
                    jadx_path,
                    keywords,
                    max_findings,
                    context_radius,
                ),
                "review_template": {
                    "reconstructed_behavior": "",
                    "data_touched": "",
                    "input_source": "unknown",
                    "runtime_observed": False,
                    "confidence": "needs manual review",
                    "report_finding_supported": "",
                    "open_questions": [],
                },
            }
        )

    return output


def add_code_block(lines, language, rows):
    lines.append(f"```{language}")
    lines.extend(rows)
    lines.append("```")


def write_markdown(payload, output_path):
    lines = [
        "# Source Findings Review Packets",
        "",
        "This artifact is the Path 2 working layer. It uses JADX as the reading layer when Java-like source is available and apktool smali as the evidence layer for line-cited review.",
        "",
        "It is not a final report. Each packet needs manual reconstruction notes before it should support a publishable claim.",
        "",
        "## Strategy",
        "",
        f"- Reading layer: {payload['strategy']['reading_layer']}",
        f"- Evidence layer: {payload['strategy']['evidence_layer']}",
        f"- Scope: {payload['strategy']['scope']}",
        "",
        "## Packets",
        "",
    ]

    for finding in payload["findings"]:
        lines.extend(
            [
                f"### {finding['priority']}. `{finding['smali_file']}`",
                "",
                f"- Class: `{finding.get('class_name') or 'unknown'}`",
                f"- JADX source: `{finding.get('jadx_file') or 'not found'}`",
                f"- Categories: {', '.join(f'`{name}`' for name in finding['category_counts'])}",
                f"- Total matches: {finding['total_matches']}",
                f"- Weighted score: {finding['weighted_score']}",
                "",
                "#### Manual Review Template",
                "",
                "- Reconstructed behavior:",
                "- Data touched:",
                "- Input source: `unknown`",
                "- Runtime observed: `false`",
                "- Confidence: `needs manual review`",
                "- Report finding supported:",
                "- Open questions:",
                "",
                "#### Smali Evidence",
                "",
            ]
        )

        for context in finding["smali_context"]:
            lines.extend(
                [
                    f"- Line {context['line']}, `{context['category']}`, `{context['keyword']}`",
                    "",
                ]
            )
            add_code_block(
                lines,
                "smali",
                [
                    f"{row['line']}: {row['code']}"
                    for row in context["context"]
                ],
            )
            lines.append("")

        lines.extend(["#### JADX Reading Context", ""])
        if finding["jadx_matches"]:
            for match in finding["jadx_matches"]:
                lines.extend([f"- Line {match['line']}: `{match['code']}`", ""])
                add_code_block(
                    lines,
                    "java",
                    [
                        f"{row['line']}: {row['code']}"
                        for row in match["context"]
                    ],
                )
                lines.append("")
        else:
            lines.append("No matching JADX source was found. Generate it with `task jadx` or review smali directly.")
            lines.append("")

    output_path.write_text("\n".join(lines).rstrip() + "\n")


def main():
    parser = argparse.ArgumentParser(description="Build source reconstruction review packets from inventory, smali, and optional JADX output.")
    parser.add_argument("-i", "--inventory", default="reconstruction_inventory.json", help="Reconstruction inventory JSON path")
    parser.add_argument("-d", "--decompile-dir", default="tiktok_decompiled", help="apktool decompiled directory")
    parser.add_argument("-j", "--jadx-dir", default=None, help="Optional JADX output directory")
    parser.add_argument("-o", "--output", default="source_findings.json", help="JSON source findings output path")
    parser.add_argument("-m", "--markdown", default="source_findings.md", help="Markdown source findings output path")
    parser.add_argument("--limit", type=int, default=10, help="Maximum selected source slices to include")
    parser.add_argument("--context-radius", type=int, default=6, help="Lines of context around each finding")
    parser.add_argument("--max-findings", type=int, default=6, help="Maximum finding contexts per source slice")
    args = parser.parse_args()

    inventory_path = Path(args.inventory)
    decompile_dir = Path(args.decompile_dir)
    jadx_dir = Path(args.jadx_dir) if args.jadx_dir else None

    if not inventory_path.is_file():
        raise SystemExit(f"Inventory JSON not found: {inventory_path}")
    if not decompile_dir.is_dir():
        raise SystemExit(f"apktool decompiled directory not found: {decompile_dir}")
    if jadx_dir and not jadx_dir.is_dir():
        raise SystemExit(f"JADX directory not found: {jadx_dir}")

    payload = build_findings(
        load_json(inventory_path),
        decompile_dir,
        jadx_dir,
        args.limit,
        args.context_radius,
        args.max_findings,
    )
    Path(args.output).write_text(json.dumps(payload, indent=2))
    write_markdown(payload, Path(args.markdown))
    print(f"Source findings JSON saved to: {args.output}")
    print(f"Source findings markdown saved to: {args.markdown}")


if __name__ == "__main__":
    main()

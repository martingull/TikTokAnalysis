import argparse
import json
import re
from pathlib import Path


SUMMARY_ROW_RE = re.compile(r"^\|\s*\d+\s*\|\s*`([^`]+)`\s*\|\s*([^|]+)\|")


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def reviewed_packets(reviewed_notes_path):
    path = Path(reviewed_notes_path)
    if not path.is_file():
        return {}

    reviewed = {}
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        match = SUMMARY_ROW_RE.match(line)
        if not match:
            continue
        packet, status = match.groups()
        reviewed[packet.strip()] = " ".join(status.split())
    return reviewed


def simple_name(path):
    name = Path(path).name
    return name.removesuffix(".smali")


def review_status_for_packet(smali_file, reviewed):
    if smali_file in reviewed:
        return reviewed[smali_file]

    current_name = simple_name(smali_file)
    for packet, status in reviewed.items():
        if simple_name(packet) == current_name:
            return status
    return "not reviewed"


def build_status(source_findings, reviewed):
    packets = source_findings.get("findings", [])
    rows = []
    reviewed_count = 0
    jadx_count = 0
    false_positive_count = 0

    for packet in packets:
        smali_file = packet.get("smali_file", "")
        status = review_status_for_packet(smali_file, reviewed)
        if status != "not reviewed":
            reviewed_count += 1
        if "false-positive" in status or "false positive" in status:
            false_positive_count += 1
        if packet.get("jadx_file"):
            jadx_count += 1

        rows.append(
            {
                "priority": packet.get("priority", ""),
                "smali_file": smali_file,
                "class_name": packet.get("class_name") or "unknown",
                "categories": ", ".join(packet.get("category_counts", {}).keys()),
                "jadx": "yes" if packet.get("jadx_file") else "no",
                "review_status": status,
            }
        )

    return {
        "packet_count": len(packets),
        "reviewed_count": reviewed_count,
        "not_reviewed_count": len(packets) - reviewed_count,
        "jadx_count": jadx_count,
        "false_positive_count": false_positive_count,
        "rows": rows,
    }


def add_table(lines, headers, rows):
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        lines.append("| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |")


def write_markdown(status, output_path):
    lines = [
        "# Source Reconstruction Status",
        "",
        "This artifact shows the handoff from generated source packets to reviewed source evidence.",
        "",
        "## Summary",
        "",
    ]
    add_table(
        lines,
        ["Metric", "Count"],
        [
            ["Generated packets", status["packet_count"]],
            ["Reviewed packets", status["reviewed_count"]],
            ["Not reviewed", status["not_reviewed_count"]],
            ["Packets with JADX context", status["jadx_count"]],
            ["Reviewed likely false positives", status["false_positive_count"]],
        ],
    )

    lines.extend(
        [
            "",
            "## Packet Status",
            "",
        ]
    )
    add_table(
        lines,
        ["Priority", "Packet", "Class", "Categories", "JADX", "Review status"],
        [
            [
                row["priority"],
                f"`{row['smali_file']}`",
                f"`{row['class_name']}`",
                row["categories"],
                row["jadx"],
                row["review_status"],
            ]
            for row in status["rows"]
        ],
    )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `source_findings.md` is generated triage and should not be treated as reviewed evidence by itself.",
            "- `reviewed_source_notes.md` is the human/Codex-reviewed interpretation layer.",
            "- Publishable source claims should be based on reviewed notes and line-cited smali evidence.",
            "- JADX is a reading aid; apktool smali remains the evidence layer for claims.",
            "",
        ]
    )

    Path(output_path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Summarize generated and reviewed source reconstruction packet status.")
    parser.add_argument("-s", "--source-findings", default="source_findings.json", help="Source findings JSON path")
    parser.add_argument("-r", "--reviewed-notes", default="reviewed_source_notes.md", help="Reviewed source notes Markdown path")
    parser.add_argument("-o", "--output", default="source_reconstruction_status.md", help="Markdown output path")
    args = parser.parse_args()

    source_findings_path = Path(args.source_findings)
    if not source_findings_path.is_file():
        raise SystemExit(f"Source findings JSON not found: {source_findings_path}")

    status = build_status(load_json(source_findings_path), reviewed_packets(args.reviewed_notes))
    write_markdown(status, args.output)
    print(f"Source reconstruction status saved to: {args.output}")


if __name__ == "__main__":
    main()

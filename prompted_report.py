import argparse
import os
from pathlib import Path

from dotenv import load_dotenv

from openai_helpers import DEFAULT_MODEL, complete_with_responses
from promps import PRIVACY_PROMPT
from report_builder import build_report, load_json


def build_evidence_brief(analysis_path, inventory_path, source_findings_path=None):
    analysis = load_json(analysis_path)
    inventory = load_json(inventory_path) if inventory_path else None
    source_findings = load_json(source_findings_path) if source_findings_path else None
    return build_report(analysis, inventory, source_findings)


def build_messages(evidence_brief):
    return [
        {
            "role": "system",
            "content": PRIVACY_PROMPT,
        },
        {
            "role": "user",
            "content": (
                "Create the final publishable privacy assessment report from the evidence below.\n\n"
                "Audience: technical journalists, software engineers, privacy reviewers, and informed readers.\n\n"
                "Required structure:\n"
                "1. Clear headline and one-paragraph summary.\n"
                "2. Key findings ranked by concern level.\n"
                "3. Evidence table that distinguishes manifest permissions, static API references, exported components, and source reconstruction targets.\n"
                "4. Plain-English explanation of why each issue matters.\n"
                "5. Technical appendix with file/class/API references.\n"
                "6. Limitations and what dynamic testing would be needed next.\n\n"
                "Use only the supplied evidence. Do not invent runtime behavior or network traffic.\n\n"
                f"Evidence brief:\n\n{evidence_brief}"
            ),
        },
    ]


def render_prompt_payload(messages):
    rendered = []
    for message in messages:
        rendered.extend([
            f"## {message['role'].title()} Message",
            "",
            message["content"].strip(),
            "",
        ])
    return "\n".join(rendered).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description="Generate a prompted, audience-readable APK privacy report from structured evidence.")
    parser.add_argument("-a", "--analysis", default="apk_analysis_report.json", help="Androguard JSON report path")
    parser.add_argument("-i", "--inventory", default=None, help="Optional reconstruction inventory JSON path")
    parser.add_argument("-s", "--source-findings", default=None, help="Optional source findings JSON path")
    parser.add_argument("-o", "--output", default="privacy_assessment_report.md", help="Markdown report output path")
    parser.add_argument("--evidence-output", default="privacy_evidence_brief.md", help="Deterministic evidence brief output path")
    parser.add_argument("--prompt-output", default="privacy_report_prompt_payload.md", help="Prompt payload output path")
    parser.add_argument("--dry-run", action="store_true", help="Write evidence and prompt payload without calling OpenAI")
    parser.add_argument("--model", default=None, help="OpenAI model name")
    parser.add_argument("--max-output-tokens", type=int, default=4096, help="Maximum report output tokens")
    args = parser.parse_args()

    load_dotenv()

    model = args.model or os.getenv("LLM_MODEL") or os.getenv("OPENAI_MODEL") or DEFAULT_MODEL
    evidence_brief = build_evidence_brief(args.analysis, args.inventory, args.source_findings)
    Path(args.evidence_output).write_text(evidence_brief)
    messages = build_messages(evidence_brief)
    Path(args.prompt_output).write_text(render_prompt_payload(messages))

    if args.dry_run:
        print(f"Evidence brief saved to: {args.evidence_output}")
        print(f"Prompt payload saved to: {args.prompt_output}")
        print("Dry run complete; no model call was made.")
        return

    report = complete_with_responses(
        model=model,
        instructions=PRIVACY_PROMPT,
        prompt=messages[1]["content"],
        api_key=os.getenv("OPENAI_API_KEY"),
        max_output_tokens=args.max_output_tokens,
    )
    Path(args.output).write_text(report)
    print(f"Evidence brief saved to: {args.evidence_output}")
    print(f"Prompt payload saved to: {args.prompt_output}")
    print(f"Prompted privacy assessment report saved to: {args.output}")


if __name__ == "__main__":
    main()

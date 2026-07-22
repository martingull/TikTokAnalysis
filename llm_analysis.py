import argparse
import os

from dotenv import load_dotenv

from openai_helpers import DEFAULT_MODEL, complete_with_responses
from promps import PRIVACY_PROMPT


def main():
    parser = argparse.ArgumentParser(description="Generate an LLM-assisted privacy analysis from an APK JSON report.")
    parser.add_argument("-i", "--input", default="apk_analysis_report.json", help="APK analysis JSON input path")
    parser.add_argument("-o", "--output", default="llm_analysis.md", help="Markdown output path")
    parser.add_argument("--model", default=None, help="OpenAI model name")
    parser.add_argument("--max-output-tokens", type=int, default=4096, help="Maximum output tokens")
    args = parser.parse_args()

    load_dotenv()
    model = args.model or os.getenv("LLM_MODEL") or os.getenv("OPENAI_MODEL") or DEFAULT_MODEL

    with open(args.input, "r") as file:
        report_content = file.read()

    llm_response = complete_with_responses(
        model=model,
        instructions=PRIVACY_PROMPT,
        prompt=report_content,
        api_key=os.getenv("OPENAI_API_KEY"),
        max_output_tokens=args.max_output_tokens,
    )

    print(llm_response)

    with open(args.output, "w") as file:
        file.write(llm_response)


if __name__ == "__main__":
    main()

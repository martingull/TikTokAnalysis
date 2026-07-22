from typing import Any

from openai import OpenAI


DEFAULT_MODEL = "gpt-5.5"


def build_openai_client(api_key: str | None = None, client: OpenAI | None = None) -> OpenAI:
    return client or OpenAI(api_key=api_key)


def complete_with_responses(
    *,
    model: str,
    instructions: str,
    prompt: str,
    api_key: str | None = None,
    max_output_tokens: int = 4096,
    client: OpenAI | None = None,
) -> str:
    openai_client = build_openai_client(api_key=api_key, client=client)
    response = openai_client.responses.create(
        model=model,
        instructions=instructions,
        input=prompt,
        max_output_tokens=max_output_tokens,
    )
    return response_text(response)


def response_text(response: Any) -> str:
    output_text = getattr(response, "output_text", None)
    if output_text:
        return output_text

    chunks = []
    for item in getattr(response, "output", []) or []:
        for content in getattr(item, "content", []) or []:
            text = getattr(content, "text", None)
            if text:
                chunks.append(text)
    return "\n".join(chunks)

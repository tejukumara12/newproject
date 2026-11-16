import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def generate_greeting(name: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Set the OPENAI_API_KEY environment variable.")

    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "Write one friendly, concise greeting for the person, using their name.",
            },
            {"role": "user", "content": name},
        ],
        "max_tokens": 80,
    }
    request = Request(
        f"{base_url}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=30) as response:
            result = json.load(response)
    except HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"LLM API returned HTTP {error.code}: {details}") from error
    except URLError as error:
        raise RuntimeError(f"Could not reach the LLM API: {error.reason}") from error

    try:
        greeting = result["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as error:
        raise RuntimeError("LLM API returned an unexpected response.") from error

    if not isinstance(greeting, str) or not greeting.strip():
        raise RuntimeError("LLM API returned an empty greeting.")
    return greeting.strip()


def main() -> int:
    name = input("Enter your name: ").strip()
    if not name:
        print("Please enter a name.", file=sys.stderr)
        return 1

    try:
        print(generate_greeting(name))
    except RuntimeError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
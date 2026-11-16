# newproject

`name.py` asks for a name and uses an OpenAI-compatible chat-completions API
to generate a greeting. It uses Python's standard library; no package install
is needed.

Set the API key and, optionally, the API base URL and model before running:

```sh
export OPENAI_API_KEY="your-api-key"
# Optional for a compatible provider or a different model:
export OPENAI_BASE_URL="https://api.openai.com/v1"
export OPENAI_MODEL="gpt-4o-mini"
python name.py
```

The API key is sent to the configured provider, and that provider may charge
for API usage.

## Browser frontend

With `OPENAI_API_KEY` set, start the local web server:

```sh
python web.py
```

Then open http://127.0.0.1:8000. The browser sends the entered name to the
local Python server, which calls the LLM API; the API key is not sent to the
browser.
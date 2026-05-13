# FAQ

Technical questions builders commonly hit while shipping AgentAPI projects.

## Why install name is `agentapi-core` but import is `agentapi`?

Python distribution names and import package names are different namespaces.

```bash
pip install agentapi-core
```

```python
import agentapi
```

## Why do I get a configuration error when creating an agent?

The selected provider requires an API key.

- `provider="openai"` needs `OPENAI_API_KEY`
- `provider="gemini"` needs `GEMINI_API_KEY`
- `provider="openrouter"` needs `OPENROUTER_API_KEY`

Set these in `.env` (or environment variables) before startup.

## What is the difference between `agent.run(...)` and `agent.stream(...)`?

- `run` returns one final string and executes tool-calling rounds.
- `stream` returns an async iterator of chunks for SSE streaming.

Use `run` when you need multi-round tool execution before the final answer.
Use `stream` when you need low-latency token output.

## Why do I get `TypeError: object async_generator can't be used in 'await' expression`?

`agent.stream(...)` returns an async generator. Do not `await` it directly.

```python
@app.chat("/stream")
async def stream_chat(message: str):
	return agent.stream(message)
```

## How do I define a tool with explicit model context?

Use `@tool(...)` metadata so the model sees clear guidance.

```python
from agentapi import tool


@tool(
	name="get_weather",
	description="Get current weather conditions for a city.",
	context="Use this when the user asks weather-related questions.",
)
def get_weather(city: str) -> str:
	return f"Weather in {city}: sunny"
```

## How do I limit runaway tool loops?

Use `max_tool_rounds` in `run`:

```python
response = await agent.run("Plan my day", max_tool_rounds=3)
```

## How do I clear conversation state between requests/users?

Call:

```python
agent.reset_memory()
```

For multi-user apps, create one `Agent` per user/session or isolate memory explicitly.

## Why does tool calling work in normal chat but not in my streamed endpoint?

`run` includes the tool loop. `stream` focuses on chunked provider output.

If your route must guarantee tool execution before returning text, call `run`.
Use streamed routes for token delivery and UI responsiveness.

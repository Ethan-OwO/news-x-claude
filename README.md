# news-x-claude

Fetches the top 10 HackerNews stories and uses Claude Haiku to extract structured fields from each one.

## Output

```
[1] "Anonymous GitHub account mass-dropping undisclosed 0-days"
    → topic: undisclosed zero-day exploits disclosure | company: None | sentiment: negative | technical: True

[2] "OpenRA"
    → topic: open source real-time strategy game engine | company: None | sentiment: neutral | technical: True
```

## Setup

1. Clone the repo and install dependencies with [uv](https://github.com/astral-sh/uv):

```bash
uv sync
```

2. Copy `.env.example` to `.env` and add your Anthropic API key:

```bash
cp .env.example .env
```

```
ANTHROPIC_API_KEY=sk-ant-...
```

## Usage

```bash
uv run python main.py
```

## License

MIT

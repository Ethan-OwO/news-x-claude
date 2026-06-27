import json
import anthropic
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError, field_validator

load_dotenv()

client = anthropic.Anthropic()

FEW_SHOT_EXAMPLES = [
    {
        "title": "DSpark: Speculative decoding accelerates LLM inference [pdf]",
        "url": "https://github.com/deepseek-ai/DeepSpec/blob/main/DSpark_paper.pdf",
        "output": 'topic: LLM inference optimization | company: DeepSeek | sentiment: positive | technical: True',
    },
    {
        "title": "Fintech Engineering Handbook",
        "url": "https://w.pitula.me/fintech-engineering-handbook/",
        "output": 'topic: engineering handbook | company: None | sentiment: neutral | technical: True',
    },
    {
        "title": "Long Wave radio era set to end with switch-off",
        "url": "https://www.economist.com/britain/2026/06/25/the-bbc-switches-off-its-oldest-service",
        "output": 'topic: radio broadcast shutdown | company: BBC | sentiment: negative | technical: False',
    },
]


class StoryAnalysis(BaseModel):
    topic: str
    company: str
    sentiment: str
    technical: bool

    @field_validator("sentiment")
    @classmethod
    def sentiment_must_be_valid(cls, v: str) -> str:
        if v not in ("positive", "neutral", "negative"):
            raise ValueError(f"invalid sentiment: {v}")
        return v

    def format(self, index: int, title: str) -> str:
        technical_str = str(self.technical)
        return (
            f'[{index}] "{title}"\n'
            f"    → topic: {self.topic} | company: {self.company} "
            f"| sentiment: {self.sentiment} | technical: {technical_str}"
        )


def build_prompt(title: str, url: str) -> str:
    examples = ""
    for ex in FEW_SHOT_EXAMPLES:
        examples += (
            f"Title: {ex['title']}\n"
            f"URL: {ex['url']}\n"
            f"Output: {ex['output']}\n\n"
        )

    return f"""You are a HackerNews story classifier. Extract structured fields from a story title and URL.

Output MUST be a single JSON object with exactly these keys:
  "topic"     - short phrase describing the subject (string)
  "company"   - company/org name or null if none (string or null)
  "sentiment" - one of: "positive", "neutral", "negative" (string)
  "technical" - true if the story is technical/engineering-related, false otherwise (boolean)

Output ONLY valid JSON. No explanation, no markdown, no extra text.

Examples:
{examples}---

Now classify:
Title: {title}
URL: {url}
Output:"""


def extract_story(title: str, url: str) -> StoryAnalysis | str:
    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=256,
            messages=[
                {"role": "user", "content": build_prompt(title, url)},
                {"role": "assistant", "content": "{"},
            ],
        )
        raw = "{" + response.content[0].text.strip()
        data = json.loads(raw)
        if data.get("company") is None:
            data["company"] = "None"
        return StoryAnalysis(**data)
    except json.JSONDecodeError as e:
        return f"[ERROR] JSON parse failed: {e}"
    except ValidationError as e:
        errors = "; ".join(err["msg"] for err in e.errors())
        return f"[ERROR] Validation failed: {errors}"
    except Exception as e:
        return f"[ERROR] {e}"


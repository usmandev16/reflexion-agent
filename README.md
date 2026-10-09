# reflexion-agent

A small research agent built with LangChain + LangGraph. It answers a question, critiques its own answer, searches the web (Tavily) for what's missing, and then rewrites the answer with citations. It loops like that a few times before giving the final version.

The current prompt is set up as a nutrition "expert" (animal-based diet angle), mostly because it's a fun way to see the reflection step actually push back on the first draft. You can change the persona in `reflexion_agent/prompts.py`.

## How it works

```
respond -> execute_tools -> revisor -> (loop back to execute_tools or end)
```

- **respond** - writes the first draft, a reflection (what's missing / what's unnecessary) and 1-3 search queries
- **execute_tools** - runs those queries through Tavily
- **revisor** - rewrites the answer using the search results and adds references
- stops after `MAX_ITERATIONS` tool runs (default 4)

## Setup

You need Python 3.10+, an OpenAI API key and a Tavily API key (free tier is enough, get one at https://app.tavily.com).

```bash
git clone https://github.com/usmandev16/reflexion-agent.git
cd reflexion-agent

python -m venv .venv
# windows
.venv\Scripts\activate
# mac / linux
source .venv/bin/activate

pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your keys:

```
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
```

If you skip the `.env` file it'll just ask for the keys when you run it.

## Running

With the default question:

```bash
python main.py
```

With your own question:

```bash
python main.py "What should I eat before a morning workout?"
```

It prints the first draft, then each revised answer, then the references from the final one. A full run takes a minute or so since it does several LLM calls and searches.

## Config

All in `.env`:

| variable | default | what it does |
|---|---|---|
| `MODEL_NAME` | `gpt-5-nano` | OpenAI model to use |
| `MAX_ITERATIONS` | `4` | how many search/revise rounds before stopping |
| `MAX_SEARCH_RESULTS` | `3` | results per Tavily query |

## Project layout

```
main.py                  entry point
reflexion_agent/
  config.py              env vars + api keys
  schemas.py             pydantic models for the structured output
  prompts.py             system prompt + revise instructions
  chains.py              llm + responder/revisor chains
  tools.py               tavily search execution
  graph.py               langgraph wiring
```

## Notes

- You'll see some deprecation warnings from `MessageGraph` and `TavilySearchResults` depending on your versions. They still work, I'll move to `StateGraph` / `langchain-tavily` at some point.
- The answers are not medical advice, obviously.

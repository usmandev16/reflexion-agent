import os
import getpass

from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-5-nano")
MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "4"))
MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "3"))


def _set_if_undefined(var: str) -> None:
    if os.environ.get(var):
        return
    os.environ[var] = getpass.getpass(f"{var}: ")


def load_keys() -> None:
    _set_if_undefined("OPENAI_API_KEY")
    _set_if_undefined("TAVILY_API_KEY")

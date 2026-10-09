import argparse
import warnings

from reflexion_agent.config import load_keys

warnings.filterwarnings("ignore")

DEFAULT_QUESTION = """I'm pre-diabetic and need to lower my blood sugar, and I have heart issues.
What breakfast foods should I eat and avoid"""


def collect_answers(responses):
    answers = []
    for msg in reversed(responses):
        if getattr(msg, "tool_calls", None):
            for tool_call in msg.tool_calls:
                answer = tool_call.get("args", {}).get("answer")
                if answer:
                    answers.append(answer)
    return answers


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    load_keys()

    from reflexion_agent import build_graph

    app = build_graph()
    responses = app.invoke(args.question)

    print("--- Initial Draft Answer ---")
    print(responses[1].tool_calls[0]["args"]["answer"])
    print("\n")

    print("--- Intermediate and Final Revised Answers ---")
    answers = collect_answers(responses)
    for i, ans in enumerate(answers):
        label = "Final Revised Answer" if i == 0 else f"Intermediate Step {len(answers) - i}"
        print(f"{label}:\n{ans}\n")

    final_call = responses[-1].tool_calls[0]["args"]
    references = final_call.get("references", [])
    if references:
        print("References:")
        for ref in references:
            print(f"- {ref}")


if __name__ == "__main__":
    main()

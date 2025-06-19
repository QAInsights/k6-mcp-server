"""Entry point for the k6 MCP server.

When executed directly, the script prompts the user to select the LLM model
that will drive the interaction. The choice does not affect server
functionality but is stored in the ``SELECTED_MODEL`` environment variable so
downstream tools can read it if desired.
"""

from k6_server import mcp
import os
import argparse


MODELS = ["gpt-4", "gpt-3.5-turbo", "claude-3"]


def choose_model() -> str:
    """Prompt the user to select an LLM model.

    Returns the chosen model. If the input is invalid, the first option is
    selected by default.
    """

    print("Select the LLM model to use:")
    for idx, model in enumerate(MODELS, start=1):
        print(f"{idx}. {model}")

    choice = input("Enter the number of the model [1]: ").strip()
    try:
        selection = MODELS[int(choice) - 1] if choice else MODELS[0]
    except (ValueError, IndexError):
        print("Invalid choice, defaulting to gpt-4")
        selection = MODELS[0]
    return selection


def main() -> None:
    """Run the k6 MCP server."""

    parser = argparse.ArgumentParser(description="Run the k6 MCP server")
    parser.add_argument(
        "--model",
        choices=MODELS,
        help="LLM model to use. If not provided, the value of the SELECTED_MODEL environment variable is used or you will be prompted.",
    )
    args = parser.parse_args()

    model = args.model or os.getenv("SELECTED_MODEL")
    if model and model not in MODELS:
        print(f"Invalid model '{model}', defaulting to {MODELS[0]}")
        model = MODELS[0]
    if not model:
        model = choose_model()

    os.environ["SELECTED_MODEL"] = model
    print(f"Using model: {model}")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()


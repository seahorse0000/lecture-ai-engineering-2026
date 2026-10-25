"""第1回: 会話履歴を保ちながら素のLLMに質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

最初の質問の後、同じ起動中に追加の質問を続けられる（空行で終了）。
入力トークン数が一定量を超えると、会話履歴を自動で要約して引き継ぐ。
ツールを持たない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"
SUMMARY_TOKEN_THRESHOLD = 2000


def _generate_response(question: str, chat=None):
    if chat is None:
        client = genai.Client(api_key=get_api_key())
        return client.models.generate_content(model=MODEL, contents=question)
    return chat.send_message(question)


def _print_usage(response, label: str = "usage") -> None:
    usage = response.usage_metadata
    if usage is not None:
        print(
            f"[{label}] input: {usage.prompt_token_count} tokens, "
            f"output: {usage.candidates_token_count} tokens"
        )


def ask(question: str, chat=None) -> str:
    response = _generate_response(question, chat)
    _print_usage(response)
    return response.text


def summarize_chat(client, chat):
    history = chat.get_history(curated=True)
    conversation = "\n".join(
        f"{message.role}: {' '.join(part.text for part in message.parts if part.text)}"
        for message in history
    )
    response = client.models.generate_content(
        model=MODEL,
        contents=(
            "次の会話履歴を、後続の質問に必要な事実・目的・未解決事項を保って、"
            "日本語で簡潔に要約してください。不明な点は推測で補わないでください。\n\n"
            f"{conversation}"
        ),
    )
    _print_usage(response, "summary usage")
    if not response.text:
        return chat

    print("[summary] 会話履歴を要約して引き継ぎます")
    return client.chats.create(
        model=MODEL,
        config={
            "system_instruction": (
                "以下はこれまでの会話の要約です。以降の質問に答える際、必要に応じて参照してください。\n\n"
                f"{response.text}"
            )
        },
    )


def maybe_summarize_chat(client, chat, response):
    usage = response.usage_metadata
    if usage is None or usage.prompt_token_count is None:
        return chat
    if usage.prompt_token_count <= SUMMARY_TOKEN_THRESHOLD:
        return chat
    return summarize_chat(client, chat)


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    try:
        client = genai.Client(api_key=get_api_key())
        chat = client.chats.create(model=MODEL)
        print(f"[質問] {args.question}\n")
        response = _generate_response(args.question, chat)
        _print_usage(response)
        print(response.text)
        chat = maybe_summarize_chat(client, chat, response)
        while True:
            try:
                question = input("\n質問（空行または exit で終了）> ").strip()
            except EOFError:
                break
            if question.lower() in {"", "exit", "quit"}:
                break
            print()
            response = _generate_response(question, chat)
            _print_usage(response)
            print(response.text)
            chat = maybe_summarize_chat(client, chat, response)
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()

from types import SimpleNamespace

from app import ask as ask_module


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    response = SimpleNamespace(
        usage_metadata=SimpleNamespace(prompt_token_count=12, candidates_token_count=7),
        text="回答",
    )

    class FakeModels:
        def generate_content(self, **kwargs):
            return response

    class FakeClient:
        def __init__(self, **kwargs):
            self.models = FakeModels()

    monkeypatch.setattr(ask_module.genai, "Client", FakeClient)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")

    assert ask_module.ask("質問") == "回答"
    output = capsys.readouterr().out
    assert "input: 12 tokens" in output
    assert "output: 7 tokens" in output


def test_ask_sends_follow_up_to_existing_chat(capsys):
    class FakeChat:
        def __init__(self):
            self.questions = []

        def send_message(self, question):
            self.questions.append(question)
            return SimpleNamespace(
                usage_metadata=None,
                text=f"{question}への回答",
            )

    chat = FakeChat()

    assert ask_module.ask("最初の質問", chat) == "最初の質問への回答"
    assert ask_module.ask("追加の質問", chat) == "追加の質問への回答"
    assert chat.questions == ["最初の質問", "追加の質問"]


def test_maybe_summarize_chat_replaces_history_above_token_threshold(capsys):
    history = [
        SimpleNamespace(role="user", parts=[SimpleNamespace(text="最初の質問")]),
        SimpleNamespace(role="model", parts=[SimpleNamespace(text="最初の回答")]),
    ]

    class FakeChat:
        def get_history(self, curated):
            return history

    class FakeModels:
        def generate_content(self, **kwargs):
            assert "最初の質問" in kwargs["contents"]
            return SimpleNamespace(usage_metadata=None, text="過去の会話の要約")

    class FakeChats:
        def create(self, **kwargs):
            self.config = kwargs["config"]
            return replacement_chat

    original_chat = FakeChat()
    replacement_chat = FakeChat()
    chats = FakeChats()
    client = SimpleNamespace(models=FakeModels(), chats=chats)
    response = SimpleNamespace(
        usage_metadata=SimpleNamespace(
            prompt_token_count=ask_module.SUMMARY_TOKEN_THRESHOLD + 1
        )
    )

    result = ask_module.maybe_summarize_chat(client, original_chat, response)

    assert result is replacement_chat
    assert "過去の会話の要約" in chats.config["system_instruction"]


def test_maybe_summarize_chat_keeps_history_below_token_threshold():
    chat = object()
    client = object()
    response = SimpleNamespace(
        usage_metadata=SimpleNamespace(
            prompt_token_count=ask_module.SUMMARY_TOKEN_THRESHOLD
        )
    )

    assert ask_module.maybe_summarize_chat(client, chat, response) is chat
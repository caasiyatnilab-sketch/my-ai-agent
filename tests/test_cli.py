from my_ai_agent.cli import main


def test_cli_calc(capsys) -> None:
    exit_code = main(["calc", "10 / 4"])

    assert exit_code == 0
    assert capsys.readouterr().out.strip() == "2.5"


def test_cli_doctor(capsys, monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("MY_AI_AGENT_WORKSPACE", str(tmp_path))
    exit_code = main(["doctor"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "provider=mock" in output
    assert "status=ready" in output


def test_cli_ask_thinking_indicator(capsys, monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("MY_AI_AGENT_MEMORY", str(tmp_path / "mem.jsonl"))
    monkeypatch.setenv("MY_AI_AGENT_WORKSPACE", str(tmp_path))

    # Mock isatty to return True to trigger the indicator
    monkeypatch.setattr("sys.stdout.isatty", lambda: True)

    exit_code = main(["ask", "hello"])

    assert exit_code == 0
    output = capsys.readouterr().out
    # The indicator is written then cleared with \r and spaces.
    # We expect to see "Thinking..." and the clearing sequence in the raw output.
    assert "Thinking..." in output
    assert "\r" in output
    assert "Mock response" in output

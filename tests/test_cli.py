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


def test_cli_ask_thinking_indicator(capsys, monkeypatch) -> None:
    # Mock isatty to return True to trigger the indicator
    monkeypatch.setattr("sys.stdout.isatty", lambda: True)

    exit_code = main(["ask", "hello"])

    assert exit_code == 0
    output = capsys.readouterr().out
    # Check for Thinking indicator and its clearing sequence
    assert "\rThinking..." in output
    assert "\r            \r" in output
    assert "Mock response" in output


def test_cli_ask_spacing_with_tools(capsys) -> None:
    # Ensure tool results are followed by a blank line for readability
    exit_code = main(["ask", "calc: 1 + 1"])

    assert exit_code == 0
    output = capsys.readouterr().out
    # When tools are used, MockProvider returns a specific string
    assert "[calculator:ok] 2\n\nI reviewed the tool output" in output

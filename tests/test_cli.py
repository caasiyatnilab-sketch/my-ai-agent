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


def test_cli_ask_indicator(capsys, monkeypatch) -> None:
    # Simulate a TTY
    monkeypatch.setattr("sys.stdout.isatty", lambda: True)

    exit_code = main(["ask", "hello"])

    assert exit_code == 0
    captured = capsys.readouterr()
    # Check for indicator and clearing sequence
    assert "\rThinking..." in captured.out
    assert "\r            \r" in captured.out
    assert "Mock response" in captured.out

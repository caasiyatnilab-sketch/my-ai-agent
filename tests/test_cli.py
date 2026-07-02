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
    # Mock sys.stderr.isatty() to return True
    monkeypatch.setattr("sys.stderr.isatty", lambda: True)

    exit_code = main(["ask", "hello"])

    assert exit_code == 0
    captured = capsys.readouterr()
    # Check that "Thinking..." was written to stderr and then cleared
    assert "\rThinking..." in captured.err
    assert "\r" + " " * 12 + "\r" in captured.err
    assert "Mock response" in captured.out


def test_cli_ask_formatting_with_tools(capsys) -> None:
    # No tool results: no extra newline
    main(["ask", "hello"])
    out1 = capsys.readouterr().out
    assert out1.startswith("Mock response")

    # With tool results: should have a newline between tool output and answer
    main(["ask", "calc: 2+2"])
    out2 = capsys.readouterr().out
    assert "[calculator:ok] 4\n\nI reviewed" in out2

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


def test_cli_ask_scannability(capsys, monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("MY_AI_AGENT_WORKSPACE", str(tmp_path))
    # Using a prompt that triggers a tool to ensure both tool output and answer are present
    exit_code = main(["ask", "calc: 1 + 1"])

    output = capsys.readouterr().out
    assert exit_code == 0
    # Check for blank line between tool output and final answer
    # The output should look like:
    # [calculator:ok] 2
    #
    # I reviewed the tool output...
    assert "[calculator:ok] 2\n\nI reviewed the tool output" in output

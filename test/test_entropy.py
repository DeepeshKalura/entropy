from click.testing import CliRunner

from src.act import guild


def test_task():
    runner = CliRunner()
    result = runner.invoke(guild)
    assert result.exit_code == 0

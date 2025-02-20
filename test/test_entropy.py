from click.testing import CliRunner

from src.act import task


def test_task():
    runner = CliRunner()
    result = runner.invoke(task)
    assert result.exit_code == 0

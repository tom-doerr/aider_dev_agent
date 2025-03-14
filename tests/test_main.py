from plex.main import cli
from click.testing import CliRunner

def test_cli_basic():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Run the Plex AI analysis loop" in result.output

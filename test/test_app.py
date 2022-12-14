from typer.testing import CliRunner

from . import constants
from fastgen.main import app


def test_app_commands(runner: CliRunner):
    fail_wrong_command = runner.invoke(app, ["something"])
    assert fail_wrong_command.exit_code == 2
    assert "Error" in fail_wrong_command.output
    assert constants.NO_SUCH_COMMAND_ERROR("something") in fail_wrong_command.output


def test_app_options(runner: CliRunner):
    success_help_command = runner.invoke(app, ["--help"])
    assert success_help_command.exit_code == 0
    assert "A CLI for your next FastAPI project" in success_help_command.output
    assert all(
        [(command in success_help_command.output) for command in ["g", "info", "new"]]
    )

    fail_worng_option = runner.invoke(app, ["--something"])
    assert fail_worng_option.exit_code == 2
    assert "Error" in fail_worng_option.output
    # assert constants.NO_SUCH_OPTION_ERROR("something") in fail_worng_option.output


def test_app_args(runner: CliRunner):
    fail_no_command_provided = runner.invoke(app)
    assert fail_no_command_provided.exit_code == 2
    assert "Error" in fail_no_command_provided.output
    assert constants.MISSING_COMMAND_ERROR in fail_no_command_provided.output

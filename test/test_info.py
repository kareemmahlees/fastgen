from typer.testing import CliRunner

from . import constants
from fastgen.main import app


def test_info_command(runner: CliRunner):
    success_result = runner.invoke(app, ["info"])
    assert success_result.exit_code == 0


def test_info_options(runner: CliRunner):
    success = runner.invoke(app, ["info", "--help"])
    fail_wrong_option = runner.invoke(app, ["info", "--something"])
    assert success.exit_code == 0
    assert fail_wrong_option.exit_code == 2
    assert "Error" in fail_wrong_option.output
    assert constants.NO_SUCH_OPTION_ERROR("something") in fail_wrong_option.output


def test_info_args(runner: CliRunner):
    fail_wrong_arg = runner.invoke(app, ["info", "something"])
    assert fail_wrong_arg.exit_code == 2
    assert "Error" in fail_wrong_arg.output
    assert constants.UNEXPECTED_EXTRA_ARG_ERROR("something") in fail_wrong_arg.output

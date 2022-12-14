from typer.testing import CliRunner

from . import constants
from fastgen.main import app


def test_new_command(runner: CliRunner):
    failer_result = runner.invoke(app, ["new"])
    assert failer_result.exit_code == 2
    assert "Error" in failer_result.output
    assert "Missing argument '⭐ Project Name'." in failer_result.output
    assert constants.MISSING_ARG_ERROR("⭐ Project Name")


def test_new_args(runner: CliRunner):
    fail_too_many_args = runner.invoke(app, ["new", "test", "test"])
    assert fail_too_many_args.exit_code == 2


def test_new_options(runner: CliRunner):
    fail_no_such_option = runner.invoke(app, ["new", "test", "--something"])
    assert fail_no_such_option.exit_code == 2
    assert "Error" in fail_no_such_option.output
    # assert constants.NO_SUCH_OPTION_ERROR("something") in fail_no_such_option.output

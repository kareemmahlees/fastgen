from typer.testing import CliRunner

from . import constants
from fastgen.main import app


def test_g_command(runner: CliRunner):
    fail_no_component = runner.invoke(app, ["g"])
    assert fail_no_component.exit_code == 2
    assert constants.MISSING_COMMAND_ERROR in fail_no_component.output


def test_g_router(runner: CliRunner):
    fail_missing_name = runner.invoke(app, ["g", "router"])
    assert fail_missing_name.exit_code == 2
    assert constants.MISSING_ARG_ERROR("NAME") in fail_missing_name.output


def test_g_schema(runner: CliRunner):
    fail_missing_name = runner.invoke(app, ["g", "schema"])
    assert fail_missing_name.exit_code == 2
    assert constants.MISSING_ARG_ERROR("NAME") in fail_missing_name.output


def test_g_model(runner: CliRunner):
    fail_missing_name = runner.invoke(app, ["g", "model"])
    assert fail_missing_name.exit_code == 2
    assert constants.MISSING_ARG_ERROR("NAME") in fail_missing_name.output

NO_SUCH_OPTION_ERROR = lambda option_name: f"No such option: --{option_name}"

UNEXPECTED_EXTRA_ARG_ERROR = (
    lambda arg_name: f"Got unexpected extra argument ({arg_name})"
)

MISSING_ARG_ERROR = lambda arg_name: f"Missing argument '{arg_name}'."

MISSING_COMMAND_ERROR = "Missing command."

NO_SUCH_COMMAND_ERROR = lambda command_name: f"No such command '{command_name}'."

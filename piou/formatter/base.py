import abc
import shutil
from dataclasses import dataclass
from typing import Optional, Callable

from ..command import Command, CommandOption, ParentArgs, CommandGroup


def get_str_side_by_side(a: str, b: str, col_1_size: int, col_2_size: int, space: int):
    while a or b:
        yield f'{a[:col_1_size].ljust(col_1_size):<{col_1_size + space}}{b[:col_2_size]}'
        a = a[col_1_size:]
        b = b[col_2_size:]


def print_size_by_size(print_fn: Callable,
                       *args,
                       col_1_size: int = 20,
                       col_2_size: int = 100,
                       space: int = 4):
    for arg in args:
        if isinstance(arg, str):
            print_fn(arg)
        else:
            _args = [arg] if isinstance(arg, tuple) else arg
            for x in _args:
                for line in get_str_side_by_side(*x,
                                                 col_1_size=col_1_size,
                                                 col_2_size=col_2_size,
                                                 space=space):
                    print_fn(line)


def get_options_str(options: list[CommandOption]) -> list[tuple[Optional[str], str, str]]:
    lines = []
    for _command in options:
        if len(_command.keyword_args) == 0:
            name = None
            other_args = None
        else:
            name, *other_args = _command.keyword_args
            other_args = ' (' + ', '.join(other_args) + ')' if other_args else ''

        lines.append((name, other_args, _command.help))
    return lines


@dataclass(frozen=True)
class Titles:
    GLOBAL_OPTIONS = 'GLOBAL OPTIONS'
    AVAILABLE_CMDS = 'AVAILABLE COMMANDS'
    COMMANDS = 'COMMANDS'
    USAGE = 'USAGE'
    DESCRIPTION = 'DESCRIPTION'
    ARGUMENTS = 'ARGUMENTS'
    OPTIONS = 'OPTIONS'


@dataclass
class Formatter(abc.ABC):
    print_fn: Callable = print
    col_size: int = 20
    col_space: int = 4

    def print_rows(self, *args):
        columns, _ = shutil.get_terminal_size()
        return print_size_by_size(self.print_fn, *args,
                                  col_1_size=self.col_size,
                                  col_2_size=columns - self.col_size - self.col_space,
                                  space=self.col_space)

    def print_help(self, *,
                   group: CommandGroup,
                   command: Optional[Command] = None,
                   parent_args: ParentArgs = None
                   ) -> None:
        # We are printing a command help
        if command:
            self.print_cmd_help(command, group.options, parent_args)
        # In case we are printing help for a command group
        elif parent_args:
            self.print_cmd_group_help(group, parent_args)
        # We are printing the CLI help
        else:
            self.print_cli_help(group)

    @abc.abstractmethod
    def print_cli_help(self, group: CommandGroup) -> None:
        ...

    @abc.abstractmethod
    def print_cmd_group_help(self, group: CommandGroup, parent_args: ParentArgs) -> None:
        ...

    @abc.abstractmethod
    def print_cmd_help(self,
                       command: Command,
                       options: list[CommandOption],
                       parent_args: ParentArgs = None) -> None:
        ...

    def print_cmd_error(self, cmd: str) -> None:
        print(f'Unknown command {cmd!r}')

    def print_param_error(self, key: str) -> None:
        print(f'Could not find value for {key!r}')

    def print_count_error(self, expected_count: int, count: int) -> None:
        print(f'Expected {expected_count} positional arguments but got {count}')

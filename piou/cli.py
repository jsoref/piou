import sys
from dataclasses import dataclass, field
from typing import Optional, Any

from .command import CommandGroup, ShowHelpError
from .exceptions import (
    CommandNotFoundError,
    ParamNotFoundError, PosParamsCountError
)
from .formatter import Formatter, RichFormatter


@dataclass
class Cli:
    description: Optional[str] = None
    formatter: Formatter = field(default_factory=RichFormatter)

    _group: CommandGroup = field(init=False, default_factory=CommandGroup)

    def __post_init__(self):
        self._group.help = self.description

    @property
    def commands(self):
        return self._group.commands

    def run(self):
        try:
            _, *args = sys.argv
        except ValueError:
            return
        self.run_with_args(*args)

    def run_with_args(self, *args):
        try:
            return self._group.run_with_args(*args)
        except CommandNotFoundError as e:
            raise e
        except ShowHelpError as e:
            self.formatter.print_help(group=e.group,
                                      command=e.command,
                                      parent_args=e.parent_args)
        except ParamNotFoundError as e:
            self.formatter.print_param_error(e.key)
            return
        except PosParamsCountError as e:
            self.formatter.print_count_error(e.expected_count, e.count)
            return

    def command(self, cmd: str, help: str = None):
        return self._group.command(cmd=cmd, help=help)

    def add_option(self, default: None, *args, help: str = None, data_type: Any = bool):
        self._group.add_option(default, *args, help=help, data_type=data_type)

    def add_sub_parser(self, cmd: str, description: Optional[str] = None) -> CommandGroup:
        cmd_group = CommandGroup(name=cmd, help=description)
        self._group.add_group(cmd_group)
        return cmd_group

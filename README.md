# Piou  


[![CircleCI](https://circleci.com/gh/Andarius/piou/tree/master.svg?style=shield)](https://app.circleci.com/pipelines/github/Andarius/piou?branch=master)
[![Latest PyPI version](https://img.shields.io/pypi/v/piou?logo=pypi)](https://pypi.python.org/pypi/piou)
[![Latest conda-forge version](https://img.shields.io/conda/vn/conda-forge/piou?logo=conda-forge)](https://anaconda.org/conda-forge/piou)  

A CLI tool to build beautiful command-line interfaces with type validation.

It is as simple as

```python
from piou import Cli, Option

cli = Cli(description='A CLI tool')


@cli.command(cmd='foo',
             help='Run foo command')
def foo_main(
    foo1: int = Option(..., help='Foo arguments'),
    foo2: str = Option(..., '-f', '--foo2', help='Foo2 arguments'),
    foo3: str = Option(None, '-g', '--foo3', help='Foo3 arguments'),
):
    pass

if __name__ == '__main__':
    cli.run()
```
The output will look like this: 

![example](./docs/simple-output.png)


You can also add sub-commands:

```python
from piou import Cli, Option

cli = Cli(description='A CLI tool')

sub_cmd = cli.add_sub_parser(cmd='sub', description='A sub command')

sub_cmd.add_option(False, '-', '--dry-run', help='Run in dry run mode')


@sub_cmd.command(cmd='foo', help='Run baz command')
def baz_bar_main(**kwargs):
    pass


@sub_cmd.command(cmd='bar', help='Run toto command')
def toto_main(
        foo1: int = Option(..., help='Foo arguments'),
        foo2: str = Option(..., '-f', '--foo2', help='Foo2 arguments'),
):
    pass


if __name__ == '__main__':
    cli.run()

```

![example](./docs/sub-cmd-output.png)

Here is a more complete example: 

```python
from piou import Cli, Option

cli = Cli(description='A CLI tool')

cli.add_option(None, '-q', '--quiet', help='Do not output any message')
cli.add_option(None, '--verbose', help='Increase verbosity')


@cli.command(cmd='foo',
             help='Run foo command')
def foo_main(
        quiet: bool,
        verbose: bool,
        foo1: int = Option(..., help='Foo arguments'),
        foo2: str = Option(..., '-f', '--foo2', help='Foo2 arguments'),
        foo3: str = Option(None, '-g', '--foo3', help='Foo3 arguments'),
):
    pass


@cli.command(cmd='bar', help='Run bar command')
def bar_main(**kwargs):
    pass


sub_cmd = cli.add_sub_parser(cmd='sub', description='A sub command')
sub_cmd.add_option(None, '--test', help='Test mode')


@sub_cmd.command(cmd='bar', help='Run baz command')
def baz_bar_main(
        **kwargs
):
    pass


@sub_cmd.command(cmd='toto', help='Run toto command')
def toto_main(
        test: bool,
        quiet: bool,
        verbose: bool,
        foo1: int = Option(..., help='Foo arguments'),
        foo2: str = Option(..., '-f', '--foo2', help='Foo2 arguments'),
):
    pass


if __name__ == '__main__':
    cli.run()
```

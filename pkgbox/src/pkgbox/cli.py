"""
Module that creates a pkgbox CLI.

The run is used as a script entrypoint and should not be invoked.
"""
import click

from . import __version__ as _ver

@click.group
def cli() -> None:
    """
    An extendable packaging tool that packages artifacs as OCI layers.
    """
    pass


@cli.command
def version() -> None:
    """
    Show program version
    """
    click.echo(f'v{_ver}')


def run() -> None:
    """
    Run the CLI, this function exists for the sole purpose of
    being used in an entrypoint script.
    """
    cli()

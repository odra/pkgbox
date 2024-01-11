"""
The cli module is used to run the pkgbox main cli.
"""
import os
import sys
import shutil

import click

from . import errors, env


@click.group
def cli() -> None:
    """
    The main cli group which other subcommands are
    attached to.
    """
    pass

@cli.command
def version() -> None:
    """
    Handles the `pkgbox version` command.
    """
    click.echo('v0.1.0')


@cli.command
def init() -> None:
    """
    Handles the `pkgbox init` command.
    """
    paths = env.get_pkgbox_dirs()

    for k, v in paths.items():
        click.echo(f'{k}: {v}')

    env.ensure_pkgbox_dirs(paths)
    env.bootstrap(paths)


@cli.command
def info() -> None:
    """
    Handles the `pkgbox info` command.
    """
    raise errors.PBNotImplementedError()


@cli.command
def build() -> None:
    """
    Handles the `pkgbox build` command.
    """
    raise errors.PBNotImplementedError()


def main() -> None:
    try:
        cli()
    except errors.PBError as e:
        click.echo(str(e), err=True)
        sys.exit(e.errno)

"""
The cli module is used to run the pkgbox main cli.
"""
import os
import sys
import shutil
import pathlib

import click

from . import errors, env, containerfile


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
@click.argument('path', type=click.Path(exists=True, readable=True))
def inspect(path: click.Path) -> None:
    """
    Inspects a Containerfile and pritns its parsed output.
    """
    c = containerfile.from_path(pathlib.Path(path))

    # base image
    click.echo(f'Base Image: {c.base_image}')
    # labels
    click.echo(f'Labels ({len(c.labels)}):')
    for k, v in c.labels.items():
        click.echo(f'\tName: {k}')
        click.echo(f'\tValue: {v}')
    # env vars
    click.echo(f'Env Vars ({len(c.env_vars)}):')
    for k, v in c.env_vars.items():
        click.echo(f'\tName: {k}')
        click.echo(f'\tValue: {v}')
    # env vars
    click.echo(f'Build Args ({len(c.build_args)}):')
    for k, v in c.build_args.items():
        click.echo(f'\tName: {k}')
        click.echo(f'\tValue: {v}')
    # instructions
    click.echo(f'Insructions ({len(c.instructions)}):')
    for instruction in c.instructions:
        click.echo(f'\tType: {instruction.name}')
        click.echo(f'\tValue: {instruction.value}')
        click.echo(f'\tDigest: {instruction.digest}')
        click.echo(f'\tEphemeral {instruction.is_ephemeral()}')
    

@cli.command
@click.option('-i', '--image', 'image_name', default='registry.fedoraproject.org/fedora:39') 
def build(image_name: str) -> None:
    """
    Handles the `pkgbox build` command.
    """
    # paths = env.get_pkgbox_dirs()
    # data_dir = paths['data_dir']
    # img = image.from_str(image_name)
    # manifest = image.info(img)
    # dest = pathlib.Path(f'{data_dir}/oci-layers')

    # click.echo(f'Fetching data from "{image_name}"...')
    # image.fetch(img, manifest, dest)
    # click.echo(f'Data fetched into {dest}')
    raise errors.PBNotImplementedError()


def main() -> None:
    try:
        cli()
    except errors.PBError as e:
        click.echo(str(e), err=True)
        sys.exit(e.errno)

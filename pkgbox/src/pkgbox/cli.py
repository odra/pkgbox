"""
The cli module is used to run the pkgbox main cli.
"""
import os
import sys
import json
import uuid
import shutil
import pathlib
import subprocess

import click

from . import containerfile, env, errors, image, rootfs


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
@click.argument('path', type=click.Path(exists=True, readable=True))
@click.option('--build-id', default=str(uuid.uuid4()),  help='build unique id or name')
def build(path: click.Path, build_id: str) -> None:
    """
    Handles the `pkgbox build` command.
    """
    # TODO: split this abomination into smaller functions
    # initialize env variables
    pkgbox_dirs = env.get_pkgbox_dirs()
    data_dir = pkgbox_dirs['data_dir']
    cfg_dir = pkgbox_dirs['config_dir']
    # read and parse containerfile 
    containerfile_path = pathlib.Path(path)
    cfile = containerfile.from_path(containerfile_path)
    
    # retrieve base_image manifest info
    click.echo(f'[INFO] Reading manifest data for "{cfile.base_image}"...')
    base_image_manifest = image.get_manifest(cfile.base_image)
    # setup image/build env dir
    click.echo(f'Using build id/name: {build_id}') 
    os.makedirs(f'{data_dir}/builds/{build_id}', exist_ok=True)
    shutil.copy(f'{cfg_dir}/crun/config.json', f'{data_dir}/builds/{build_id}/config.json')
    os.makedirs(f'{data_dir}/builds/{build_id}/rootfs', exist_ok=True)
    # download and extract layers into the build env folder
    layers_dir = f'{data_dir}/oci-layers'
    os.makedirs(layers_dir, exist_ok=True)
    click.echo(f'OCI Layers dir: {layers_dir}')

    # fetch and apply layers from base image
    # TODO: move this logic to the instruction loop
    click.echo(f'Found {len(base_image_manifest.layers)} layer(s).')
    image_name_parts = cfile.base_image.split('/')
    reg = image_name_parts[0]
    namespace, tag = '/'.join(image_name_parts[1:]).split(':')
    image.fetch_layers(reg, namespace, base_image_manifest.layers, layers_dir)
    image.apply_layers(base_image_manifest.layers, layers_dir,  f'{data_dir}/builds/{build_id}/rootfs')
    rootfs_path = pathlib.Path(f'{data_dir}/builds/{build_id}/rootfs')

    # run containerfile instructions
    is_artifact = False
    for idx, instruction in enumerate(cfile.instructions):
        if instruction.name == 'RUN':
            if idx > 0 and cfile.instructions[idx-1].name == 'COMMENT':
                if cfile.instructions[idx-1].value == 'org.pkgbox.artifact=true':
                    is_artifact = True
            crun_cfg = json_read(f'{data_dir}/builds/{build_id}/config.json')
            crun_cfg['process']['args'] = ['bash', '-c', instruction.value]
            json_write(f'{data_dir}/builds/{build_id}/config.json', crun_cfg)
            rf1 = rootfs.from_path(rootfs_path)
            result = run_instruction(f'{data_dir}/builds/{build_id}', build_id)
            rf2 = rootfs.from_path(rootfs_path)
            instruction_digest = instruction.digest.split(':')[1]
            logfile = f'{data_dir}/builds/{build_id}/{instruction_digest}.log'
            
            if result.stderr:
                with open(f'{logfile}.err', 'w+') as f:
                    f.write(f'{instruction.value}\n')
                    f.write(f'{result.stderr}\n')
            else:
                with open(f'{logfile}.out', 'w+') as f:
                    f.write(f'{instruction.value}\n')
                    f.write(f'{result.stdout}\n')
            
            if result.returncode != 0 or result.stderr:
                raise errors.PBError('Instruction failed: {instruction.value}')
            
            diff = rootfs.mgr.diff(rf1, rf2)
            if len(diff) == 0:
                continue
            
            if is_artifact:
                diff_dir = f'{data_dir}/builds/{build_id}/rootfs.{instruction_digest}'
                click.echo(f'Identified rootfs changes, archiving instruction {instruction_digest}')
                os.makedirs(diff_dir, exist_ok=True)               
                for added in diff['add']:
                    os.makedirs( f'{diff_dir}{os.path.dirname(added)}' , exist_ok=True)
                    shutil.copy2(f'{data_dir}/builds/{build_id}/rootfs{added}', f'{diff_dir}{added}')
                rootfs.mgr.archive(rootfs.from_path(pathlib.Path(diff_dir)), f'{diff_dir}.tar.gz')
                shutil.rmtree(diff_dir)
                is_artifact = False


def run_instruction(build_dir: pathlib.Path, build_id: str):
    cmd = [
        'crun',
        'run',
        '--config', f'{build_dir}/config.json',
        '--bundle', build_dir,
        f'{build_id}-build'
    ]
    
    return subprocess.run(cmd, capture_output=True, text=True)


def json_read(path):
    with open(path, 'r') as f:
        return json.load(f)


def json_write(path, data):
    with open(path, 'w+') as f:
        json.dump(data, f, indent=4)


def main() -> None:
    try:
        cli()
    except errors.PBError as e:
        click.echo(str(e), err=True)
        sys.exit(e.errno)

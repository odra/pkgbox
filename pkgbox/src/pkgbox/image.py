import os
import tarfile
import pathlib
from typing import List

import requests

from pkgbox.oci import v1


def get_manifest(image_name: str) -> v1.Manifest:
    """
    Retrieves a container image's  manifest json file from
    an OCI registry.
    """
    parts = image_name.split('/')
    reg = parts[0]
    namespace, tag = '/'.join(parts[1:]).split(':')

    baseurl = f'https://{reg}/v2/{namespace}'
    headers = {
        'Accept': 'application/vnd.oci.image.manifest.v1+json'
    }

    res = requests.get(f'{baseurl}/manifests/{tag}', headers=headers)
    data = res.json()

    return v1.Manifest(
        data['schemaVersion'],
        v1.Descriptor(
            v1.MediaType.from_str(data['config']['mediaType']),
            v1.Digest.from_str(data['config']['digest']),
            data['config']['size']
        ),
        layers=[
            v1.Descriptor(
                v1.MediaType.from_str(l['mediaType']),
                v1.Digest.from_str(l['digest']),
                l['size'],
                urls=l.get('urls', []),
                annotations=l.get('annotations', {})
            )
            for l in data['layers']],
        annotations=data.get('annotations', {})
    )


def layer_exists(layer: v1.Descriptor, dest: pathlib.Path, suffix: str = '.tar.gz') -> bool:
    """
    Validates if a layer has been downloaded already.
    """
    return os.path.exists(f'{dest}/{layer.digest.value}{suffix}')


def fetch_layers(reg: str, namespace: str, layers: List[v1.Descriptor], dest: pathlib.Path):
    """
    Fecthes the all image layers into the `dest` folder.
    """ 
    baseurl = f'https://{reg}/v2/{namespace}'

    for layer in layers:
        if layer_exists(layer, dest):
            continue
        
        with requests.get(f'{baseurl}/blobs/{layer.digest}', allow_redirects=True, stream=True) as stream:
            stream.raise_for_status()
            with open(f'{dest}/{layer.digest.value}.tar.gz', 'wb') as f:
                for chunk in stream.iter_content(chunk_size=8192):
                    f.write(chunk)


def apply_layers(layers: List[v1.Descriptor], layers_dir: pathlib.Path, dest: pathlib.Path) -> None:
    """
    Extract/apply layers into a dest rootfs.
    """
    for layer in layers:
        layer_path = f'{layers_dir}/{layer.digest.value}.tar.gz'
        with tarfile.open(layer_path, 'r:gz') as tar:
            tar.extractall(path=str(dest))

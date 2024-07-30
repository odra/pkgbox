import os
from unittest.mock import patch, mock_open

from pkgbox import errors
from pkgbox.cli import cli


def test_path_miss_error(clirunner, fixdir):
    res = clirunner.invoke(cli, ['inspect', f'{fixdir}/Containerfile.simpl'])

    assert res.exit_code == 2


def test_path_open_error(clirunner, fixdir):
    with patch('builtins.open', mock_open()) as mock_file:
        mock_file.side_effect = OSError("File not found")
        res = clirunner.invoke(cli, ['inspect', f'{fixdir}/Containerfile.simple'])

    assert res.exit_code == 1


def test_ok(clirunner, fixdir):
    expected_output = """Base Image: quay.io/fedora/fedora:latest
Labels (1):
	Name: foo
	Value: bar
Env Vars (1):
	Name: HOME
	Value: /root
Build Args (1):
	Name: TARGETARCH
	Value: amd64
Insructions (6):
	Type: FROM
	Value: quay.io/fedora/fedora:latest
	Digest: sha256:9016769fdc97a418810f966c3a2854656153c5929f2e18169d04267c9d78d01d
	Ephemeral False
	Type: LABEL
	Value: foo=bar
	Digest: sha256:30bb135276dfacaa5c15d7b9860a4d7b3ce7f4158cde259fa07fa8065b555b14
	Ephemeral True
	Type: ARG
	Value: TARGETARCH=amd64
	Digest: sha256:80b8a9ed74fb9ebd6c332cbee9c0788cdde4d65c9e6291e58f880342e32d3bb1
	Ephemeral True
	Type: ENV
	Value: HOME=/root
	Digest: sha256:d9680e961e4c55321434858673d0574b3460b0709867e71a787297eeee7e9ef6
	Ephemeral True
	Type: RUN
	Value: dnf install -y gcc
	Digest: sha256:c5f60a774418c02894f243f1c158a7cde617da8eaea6845722b3be68f577888a
	Ephemeral False
	Type: ENTRYPOINT
	Value: ["/usr/bin/gcc"]
	Digest: sha256:bce6faf76bd6e298ae3471c40445a31a08cac49532b8ff3acc8341ff6b9d8155
	Ephemeral False"""
    res = clirunner.invoke(cli, ['inspect', f'{fixdir}/Containerfile.simple'])

    assert res.exit_code == 0
    assert res.output.strip() == expected_output

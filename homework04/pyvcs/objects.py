import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    """
    Вычисление хэш-суммы

    :version: 0.2.0

    :param data:
    :param fmt:
    :param write:
    :return:
    """
    store = f"{fmt} {len(data)}\0".encode() + data
    hash_sum = hashlib.sha1(store).hexdigest()
    if write:
        folder_name, file_name = hash_sum[:2], hash_sum[2:]
        obj_dir = repo_find() / "objects" / folder_name
        if not obj_dir.exists():
            obj_dir.mkdir()

        with open(obj_dir / file_name, "wb") as f:
            f.write(zlib.compress(store))
    return hash_sum


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    # PUT YOUR CODE HERE
    ...


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    ...


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    # PUT YOUR CODE HERE
    ...


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    # PUT YOUR CODE HERE
    ...


def cat_file(obj_name: str, pretty: bool = True) -> None:
    # PUT YOUR CODE HERE
    ...


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    ...

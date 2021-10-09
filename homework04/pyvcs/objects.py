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


def resolve_object(obj_name: str,
                   gitdir: pathlib.Path) -> tp.List[str]:
    """
    Ищет захэшированные файлы

    :version: 0.3.0

    :param obj_name:
    :param gitdir:
    :return:
    """
    obj_len = len(obj_name)

    if not 5 <= obj_len <= 39:
        raise Exception(f"Not a valid object name {obj_name}")

    objects_path = gitdir / "objects"
    folder_name = obj_name[:2]

    base_path = objects_path / folder_name
    files = []

    for file in base_path.glob("*"):
        dummy_filename = file.parent.name + file.name

        if obj_name == dummy_filename[:obj_len]:
            files.append(dummy_filename)

    if not files:
        raise Exception(f"Not a valid object name {obj_name}")
    return files


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    pass


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    """
    Зеркальная функция к has_object - декодирует хэшированный файл

    Возвращает формат (blob, commit, e.t.c) и раздекодированное сообщение

    :version: 0.3.0

    :param sha:
    :param gitdir:
    :return:
    """
    symbol, space = b"\00", b" "
    folder_name, filename = sha[:2], sha[2:]
    full_path = gitdir / "objects" / folder_name / filename

    with open(full_path, "rb") as f:
        obj_data = zlib.decompress(f.read())

    finish = obj_data.find(symbol)
    header = obj_data[:finish]
    start = header[:header.find(space)]
    fmt = start.decode("ascii")
    data = obj_data[finish+1:]
    return fmt, data


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    pass


def cat_file(obj_name: str, pretty: bool = True) -> None:
    """
    :version: 0.3.0

    :param obj_name:
    :param pretty:
    :return:
    """
    gitdir = repo_find()
    fmt, data = read_object(obj_name, gitdir)
    print(data.decode() if pretty else data)


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    ...

import os
import copy
import pathlib
import stat
import time
import typing as tp
from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(
        gitdir: pathlib.Path,
        index: tp.List[GitIndexEntry],
        dirname: str = "") -> str:
    """
    :version: 0.5.0

    """
    tree = []
    sub_folder = {}
    directory_mode = 0o40000
    for entry in index:
        names = [x for x in entry.name.lstrip(dirname).split("/") if x != ""]
        folder = names[0]
        if len(names) == 1:
            tree.append((
                entry.mode,
                str(gitdir.parent / folder),
                entry.sha1
            ))
        else:
            if folder not in sub_folder:
                sub_folder[folder] = []
            sub_folder[folder].append(entry)
    for name in sub_folder:
        data = write_tree(
            gitdir=gitdir,
            index=sub_folder[name],
            dirname=dirname + "/" + name if dirname != "" else name
        )
        tree.append(
            (
                directory_mode,
                str(gitdir.parent / dirname / name),
                bytes.fromhex(data),
            )
        )
    tree = sorted(tree, key=lambda x: x[1])
    data = b"".join(
        f"{elem[0]:o} {elem[1].split('/')[-1]}".encode() + b"\00" + elem[2] for
        elem in tree
    )
    return hash_object(data, "tree", write=True)


def commit_tree(
        gitdir: pathlib.Path,
        tree: str,
        message: str,
        parent: tp.Optional[str] = None,
        author: tp.Optional[str] = "Dementiy <Dementiy@yandex.ru>",
) -> str:
    """
    :version: 0.6.0

    """
    if (
            author is None
            and "GIT_AUTHOR_NAME" in os.environ
            and "GIT_AUTHOR_EMAIL" in os.environ
    ):
        get_name = os.getenv("GIT_AUTHOR_NAME")
        get_email = os.getenv("GIT_AUTHOR_EMAIL")
        author = f"""{get_name} <{get_email}>"""

    absolute = abs(time.timezone) // 60
    localtime = int(time.mktime(time.localtime()))
    sign = '-' if time.timezone > 0 else '+'
    times = f"{absolute // 60:02}{absolute % 60:02}"
    timezone = sign + times
    data = [
        f"tree {tree}",
        f"parent {parent}" if parent is not None else "",
        f"author {author} {localtime} {timezone}",
        f"committer {author} {localtime} {timezone}",
        f"\n{message}\n"
    ]
    data = '\n'.join([x for x in data if x != ""])

    return hash_object(data.encode(), "commit", write=True)

import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    """
    mtime - время последнего изменения файлов
    ctime - время либо последнего изменения файла,
                  либо последнего изменения атрибутов (права доступа, владельца)
    atime - время последнего доступа к файлу (чтение, запись, выполнение)
    """
    ctime_s: int  # (4 байта) время последнего изменения в секундах>
    ctime_n: int  # (4 байта) время последнего изменения в наносекундах> (0)
    mtime_s: int  # (4 байта) время последней модификации в секундах>
    mtime_n: int  # (4 байта) время последней модификации в наносекундах> (0)
    dev: int  # (4 байта) ID устройства с файлом>
    ino: int  # (4 байта) номер inode>
    mode: int  # (4 байта) права доступа>
    uid: int  # (4 байта) ID пользователя-владельца>
    gid: int  # (4 байта) ID группы-владельца>
    size: int  # (4 байта) полный размер в байтах>
    sha1: bytes  # (20 байт)
    flags: int  # (2 байта)
    name: str  # <name путь к файлу>

    def pack(self) -> bytes:
        """
        I - unsigned int
        :version: 0.4.0

        :return:
        """
        n = len(self.name)
        # прочитав это можно сформировать format
        # https://docs.python.org/3/library/struct.html#format-characters
        formatter = (
                ">"  # big-endian
                + "10I"  # 10 Unsigned INT
                + "20s"  # 20 Bytes
                + "h"  # short (2 bytes)
                + f"{str(n)}s"  # len(str) # variable length
                + f"{str(8 - (62 + n) % 8)}x"  # 1-8 nul bytes as necessary to pad the entry to a multiple of eight bytes
                                               # while keeping the name NUL-terminated.
        )
        args = [
            self.ctime_s, self.ctime_n, self.mtime_s, self.mtime_n,
            self.dev, self.ino, self.mode, self.uid, self.gid, self.size,
            self.sha1, self.flags, self.name.encode()
        ]
        return struct.pack(formatter, *args)

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        """
        :version: 0.4.0

        :param data:
        :return:
        """
        n = len(data)
        formatter = (
            ">"  # big-endian
            + "10I"  # 10 Unsigned INT
            + "20s"  # 20 Bytes
            + "h"  # short (2 bytes)
            + f"{str(n - 62)}s"
        )
        unpack = list(struct.unpack(formatter, data))
        unpack[-1] = unpack[-1].split(b"\00")[0].decode()
        return GitIndexEntry(*unpack)


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    """
    :version: 0.4.0

    :param gitdir:
    :return:
    """
    index = gitdir / "index"
    if not index.exists():
        return []

    with open(index, "rb") as file:
        data = file.read()

    result, header, main_content = [], data[8:12], data[12:]
    n = len(main_content)
    unpacked = struct.unpack(">I", header)[0]

    for _ in range(unpacked):
        end_of_entry = n - 1

        for elem in range(63, n, 8):
            if not main_content[elem]:
                end_of_entry = elem
                break

        pos = end_of_entry + 1
        result += [GitIndexEntry.unpack(main_content[:pos])]
        if len(main_content) > end_of_entry:
            main_content = main_content[pos:]

    return result


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    """
    :version: 0.4.0

    :param gitdir:
    :param entries:
    :return:
    """
    index = gitdir / "index"
    with open(index, "wb") as f:
        data = (
                b"DIRC\00\00\00\02"  # dircache + version 2 (как в тестах)
                + struct.pack(">I", len(entries))  # количество файлов
                + b''.join([i.pack() for i in entries])
        )
        sha = hashlib.sha1(data)
        full_data = data + sha.digest()
        f.write(full_data)


def ls_files(gitdir: pathlib.Path,
             details: bool = False) -> None:
    """
    :version: 0.4.0

    :param gitdir:
    :param details:
    :return:
    """
    for entry in read_index(gitdir):
        print(f"{entry.mode:o} {entry.sha1.hex()} 0\t{entry.name}"
              if details else entry.name)


def update_index(gitdir: pathlib.Path,
                 paths: tp.List[pathlib.Path],
                 write: bool = True) -> None:
    """
    :version: 0.4.0

    :param gitdir:
    :param paths:
    :param write:
    :return:
    """
    entries = read_index(gitdir)

    for path in paths:
        with open(path, "rb") as f:
            data = f.read()

        stat = os.stat(path)
        hsh = hash_object(data, "blob", write=True)
        entries.append(
            GitIndexEntry(
                ctime_s=int(stat.st_ctime),
                ctime_n=0, # по условию
                mtime_s=int(stat.st_mtime),
                mtime_n=0, # по условию
                dev=stat.st_dev,
                ino=stat.st_ino,
                mode=stat.st_mode,
                uid=stat.st_uid,
                gid=stat.st_gid,
                size=stat.st_size,
                sha1=bytes.fromhex(hsh),
                flags=1,
                name=str(path).replace('\\', '/'),  # windows
            )
        )
    if write:
        write_index(gitdir, sorted(entries, key=lambda x: x.name))

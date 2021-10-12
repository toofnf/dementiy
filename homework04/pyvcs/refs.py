import pathlib
import typing as tp


def update_ref(
        gitdir: pathlib.Path,
        ref: tp.Union[str, pathlib.Path],
        new_value: str
) -> None:
    """
    :version: 0.7.0

    Просто записываем в файл с названием ветки <ref>
    ссылку на последний коммит <new_value>

    пример:

    pyvcs update-ref refs/heads/master <new_value>
    """
    with open(gitdir / ref, 'w') as rf:
        rf.write(new_value)


def symbolic_ref(gitdir: pathlib.Path,
                 name: str,
                 ref: str) -> None:
    """
    :version: 0.7.0

    изменяем текущую ветку в файле .pyvcs/HEAD

    pyvcs symbolic-ref HEAD refs/heads/dev

    cat .pyvcs/HEAD
    ref: refs/heads/dev
    """
    with open(gitdir / name, 'w') as head:
        head.write(f'ref: {ref}')


def ref_resolve(
        gitdir: pathlib.Path,
        refname: str
) -> str:
    """
    :version: 0.7.0

    Команда rev-parse - узнаем на какой коммит ссылаемся
    """
    if refname == "HEAD" and not is_detached(gitdir):
        return resolve_head(gitdir)
    path = gitdir / refname
    if path.exists():
        with open(path) as f:
            return f.read().strip()
    else:
        path = gitdir / "refs" / "heads" / refname
        if path.exists():
            with open(path) as f:
                return f.read().strip()
        else:
            return None


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    """
    :version: 0.7.0

    пытаемся забрать из файла .pyvcs/HEAD
    """
    return ref_resolve(gitdir, get_ref(gitdir))


def is_detached(gitdir: pathlib.Path) -> bool:
    """
    :version: 0.7.0

    Есть ли ветки вообще проверяем
    """
    return True if get_ref(gitdir) == "" else False


def get_ref(gitdir: pathlib.Path) -> str:
    """
    :version: 0.7.0

    cat .git/HEAD

    ref: refs/heads/master

    Если есть ссылка на ветку, то берем из сплита второй аргумент
    Иначе возвразаем пустую строку
    """
    with open(gitdir / "HEAD") as head:
        data = head.read().split()
        if len(data) == 2:
            return data[1]  #
        else:
            return ""

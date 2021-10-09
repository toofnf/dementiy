import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".",
              default=".pyvcs",
              windows=True) -> pathlib.Path:
    """
    :version: 0.1.0

    :param windows:
    :param default:
    :param workdir:
    :return:
    """
    root_dir = "\\" if windows else "/"

    # все данные репозитория расположены в каталоге .git
    # имя можно изменить через переменную окружения GIT_DIR

    pyvcs_dir = os.getenv("GIT_DIR", default)

    curr_dir = pathlib.Path(workdir)

    while str(curr_dir.absolute()) != root_dir:
        dummy_dir = curr_dir / pyvcs_dir

        if dummy_dir.exists():
            return dummy_dir

        curr_dir = curr_dir.parent

    final_dir = curr_dir / pyvcs_dir
    if final_dir.exists():
        return final_dir

    raise Exception("Not a git repository")


def repo_create(workdir: tp.Union[str, pathlib.Path],
                default=".pyvcs") -> pathlib.Path:
    """
    :version: 0.1.0

    :param default:
    :param workdir:
    :return:
    """

    # все данные репозитория расположены в каталоге .git
    # имя можно изменить через переменную окружения GIT_DIR

    pyvcs_dir = os.getenv("GIT_DIR", default)

    # проверяем корректность директории

    if not pathlib.Path(workdir).is_dir():
        raise Exception(f"{workdir} is not a directory")
    else:
        curr_path = pathlib.Path(workdir)

    # создаем директории согласно командам

    base_path = curr_path / pyvcs_dir

    # mkdir -p .git/refs/heads
    refs_heads_path = base_path / 'refs' / 'heads'

    # mkdir -p .git/refs/tags
    refs_tags_path = base_path / 'refs' / 'tags'

    # mkdir -p .git/objects
    objects_path = base_path / 'objects'

    for path in [refs_heads_path, refs_tags_path, objects_path]:
        path.mkdir(parents=True, exist_ok=True)

    # echo "ref: refs/heads/master\n" > .git/HEAD
    head_path = base_path / 'HEAD'
    with open(head_path, 'w') as f:
        f.write("ref: refs/heads/master\n")

    # echo "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare
    # = false\n\tlogallrefupdates = false\n" >> .git/config
    config_path = base_path / 'config'
    # .git/config - хранит настройки конкректного репозитория
    with open(config_path, 'w') as f:
        f.write("[core]\n\trepositoryformatversion = 0\n\tfilemode = "
                "true\n\tbare = false\n\tlogallrefupdates = false\n")

    # echo "Unnamed pyvcs repository" >> .git/description
    # .git/description - описание конкректного репозитория
    description_path = base_path / 'description'
    with open(description_path, 'w') as file:
        file.write("Unnamed pyvcs repository.\n")

    return base_path
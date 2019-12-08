#! /usr/bin/env python
from pathlib import Path


class FilePaths:
    _this_file = Path(__file__)

    package_dir = _this_file.parent.parent
    assert package_dir.name == "storygen"

    src_dir = package_dir.parent
    assert src_dir.name == "src"

    project_dir = src_dir.parent
    assert project_dir.name == "storygen"

    data_dir = project_dir / "data"
    assert data_dir.exists()


def project_path(*parts):
    return FilePaths.project_dir / Path(*parts)


print(FilePaths.data_dir)

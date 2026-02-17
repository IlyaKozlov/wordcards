from pathlib import Path
from typing import List
import os

from flake8.api import legacy as flake8


def get_files() -> List[str]:
    all_files = []
    project_root = Path(__file__).parent.parent
    for root in (project_root / "src", project_root / "tests"):
        for base_dir, _, files in os.walk(root):
            for file in files:
                if file.endswith(".py"):
                    all_files.append(str(Path(base_dir) / file))
    return all_files


def test_style() -> None:
    """Test that we conform to flake."""
    print()
    style_guide = flake8.get_style_guide(
        ignore=[
            "E501",
            "W503",
            "ANN101",
            "TYP101",
            "TYP102",
            "E231",
            "W604",
            "E241",
        ],
        max_line_length=140,
    )

    files = get_files()
    for file in files:
        assert os.path.isfile(file), "{} is not file".format(file)

    errors = style_guide.check_files(files)
    assert 0 == errors.total_errors

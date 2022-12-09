import argparse
import enum
import typing
from typing import Any

import requests


_URL_tags = "https://api.github.com/repos/{}/git/refs/tags"


class Type(str, enum.Enum):
    """An enum class of types of Git tags

    Git tags can have one of three types:
        - patch (0.0.x)
        - minor (0.x.0)
        - major (x.0.0)

    where x is the number affected by the type
    """

    patch = "patch"
    minor = "minor"
    major = "major"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def all(cls) -> typing.List[str]:
        return [str(type_) for type_ in cls]


def get_last_tag(repository: str) -> str:
    response = requests.get(_URL_tags.format(repository))

    tags = response.json()
    refs = [tag["ref"] for tag in tags]

    return max(refs).split("/")[-1]


def get_next_tag(last_tag: str, type_: Type) -> str:
    major, minor, patch = tuple(int(x) for x in last_tag.split("."))

    if type_ == Type.major:
        next_tag = f"{major + 1}.0.0"
    elif type_ == Type.minor:
        next_tag = f"{major}.{minor + 1}.0"
    elif type_ == Type.patch:
        next_tag = f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(
            f"Invalid type of Git tag. Expected one of {Type.all()}, got {type_}"
        )

    return next_tag


def parse_args() -> typing.Dict[str, Any]:
    parser = argparse.ArgumentParser()

    parser.add_argument("repository")
    parser.add_argument("release_branch")

    namespace = parser.parse_args()
    return vars(namespace)


def parse_type(release_branch: str) -> Type:
    for type_ in Type:
        pattern = f"/{type_}/"

        if pattern in release_branch:
            return type_

    raise ValueError(
        f"Invalid type of Git tag. Expected one of {Type.all()} in {release_branch}"
    )


def main(repository: str, release_branch: str) -> None:
    type_ = parse_type(release_branch)

    last_tag = get_last_tag(repository)
    next_tag = get_next_tag(last_tag, type_)

    print(next_tag)


if __name__ == "__main__":
    args = parse_args()
    main(**args)

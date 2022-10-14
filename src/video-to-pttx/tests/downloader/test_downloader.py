import pytest
import typing

from video2pttx import ROOT
from video2pttx.downloader.downloader import download


_ROOT_stubs = ROOT.parents[1] / "tests" / "stubs"


def videos_generator():
    """A generator of YouTube video Ids and extensions"""
    samples = [("HoKDTa5jHvg", "mp4")]

    for vid, extension in samples:
        yield vid, extension


@pytest.mark.parametrize("raw", videos_generator())
def test_download(raw):
    samples_dirpath = _ROOT_stubs / "samples"
    samples_dirpath.mkdir(parents=True, exist_ok=True)

    vid, extension = raw

    video_metadata = download(
        vid, samples_dirpath, file_extension=extension
    )

    title = video_metadata.title

    filename = f"{title}.{extension}"
    filepath = samples_dirpath / filename

    assert filepath.exists()

import pathlib
import typing

import pytest
from slugify import slugify

from video2pptx.youtube.models.downloader import YouTubeDownloader


@pytest.fixture(name="downloader")
def fixture_downloader() -> YouTubeDownloader:
    return YouTubeDownloader()


def videos_generator() -> typing.Iterator[str]:
    """A generator of YouTube video Ids and extensions"""
    samples = ["HoKDTa5jHvg"]

    yield from samples


@pytest.mark.unit
@pytest.mark.parametrize("sample", videos_generator())
def test_download(
    ROOT_tests: pathlib.Path, downloader: YouTubeDownloader, sample: str
) -> None:
    """It tests that YouTube videos (and captions, if available) are downloaded correctly

    Notes
    -----
    - All downloaded samples are cleaned up after the execution
    """
    samples_dirpath = ROOT_tests / "stubs" / "samples"
    samples_dirpath.mkdir(parents=True, exist_ok=True)

    video_metadata = downloader.download(sample, samples_dirpath)

    title = video_metadata.title
    extension = downloader.file_extension

    filename = f"{slugify(title)}{extension}"
    filepath = samples_dirpath / filename

    assert video_metadata.filepath == filepath
    assert filepath.exists()

    filepath.unlink()

    assert not filepath.exists()

    caption_filename = f"{slugify(title)}.srt"
    caption_filepath = samples_dirpath / caption_filename

    if video_metadata.caption_filepath is not None:
        assert video_metadata.caption_filepath == caption_filepath
        assert caption_filepath.exists()

        caption_filepath.unlink()

        assert not caption_filepath.exists()
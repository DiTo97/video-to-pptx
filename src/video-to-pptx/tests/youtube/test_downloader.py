import pathlib
import typing

import pytest
from slugify import slugify

from video2pptx.youtube.downloader import YouTubeDownloader


@pytest.fixture
def downloader() -> YouTubeDownloader:
    return YouTubeDownloader()


def videos_generator() -> typing.Iterator[typing.Tuple[str, str]]:
    """A generator of YouTube video Ids and extensions"""
    samples = [("HoKDTa5jHvg", ".mp4")]

    yield from samples


@pytest.mark.parametrize("sample", videos_generator())
def test_download(
    ROOT_tests: pathlib.Path,
    downloader: YouTubeDownloader, 
    sample: typing.Tuple[str, str]
) -> None:
    """It tests that YouTube videos (and captions, if available) are downloaded correctly
    
    Notes
    -----
    - All downloaded samples are cleaned up after the execution
    """
    samples_dirpath = ROOT_tests / "stubs" / "samples"
    samples_dirpath.mkdir(parents=True, exist_ok=True)

    src, extension = sample

    video_metadata = downloader.download(
        src, samples_dirpath, file_extension=extension
    )

    title = video_metadata.title

    filename = f"{slugify(title)}{extension}"
    filepath = samples_dirpath / filename

    assert video_metadata.filepath == str(filepath)
    assert filepath.exists()

    filepath.unlink()

    assert not filepath.exists()

    caption_filename = f"{slugify(title)}.srt"
    caption_filepath = samples_dirpath / caption_filename

    if video_metadata.caption_filepath is not None:
        assert video_metadata.caption_filepath == str(caption_filepath)
        assert caption_filepath.exists()

        caption_filepath.unlink()

        assert not caption_filepath.exists()

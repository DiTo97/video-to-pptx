import pytest
import typing

from slugify import slugify

from video2pptx import ROOT
from video2pptx.youtube.downloader import YouTubeDownloader


_ROOT_stubs = ROOT.parents[2] / "tests" / "stubs"


@pytest.fixture
def downloader():
    return YouTubeDownloader()


def videos_generator():
    """A generator of YouTube video Ids and extensions"""
    samples = [("HoKDTa5jHvg", ".mp4")]

    for src, extension in samples:
        yield src, extension


@pytest.mark.parametrize("raw", videos_generator())
def test_download(
    downloader: YouTubeDownloader, 
    raw: typing.Tuple[str, str]
):
    samples_dirpath = _ROOT_stubs / "samples"
    samples_dirpath.mkdir(parents=True, exist_ok=True)

    src, extension = raw

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

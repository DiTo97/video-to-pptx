import random
import typing
from functools import lru_cache

from pytube import Stream, StreamQuery, YouTube

from video2pttx.video.caption import CaptionType
from video2pttx.video.video import VideoResolution, VideoMetadata


_URL_youtube = "http://youtube.com/watch?v={}"


def _choose_stream(streams: StreamQuery, resolution: VideoResolution) -> Stream:
    """It choose a stream among many given the desired resolution"""
    if resolution == VideoResolution.lowest:
        return streams.get_lowest_resolution()

    if resolution == VideoResolution.highest:
        return streams.get_highest_resolution()

    n_streams = streams.count
    idx = random.randint(0, n_streams - 1)

    return streams.all()[idx]


@lru_cache(maxsize=5)
def download(
    vid_or_url: str,
    output_dirpath: str, 
    proxies: typing.Dict[str, str] = None, 
    use_oauth: bool = False, 
    allow_oauth_cache: bool = True,
    file_extension: str = "mp4",
    lang_code: str = "en",
    video_resolution: VideoResolution = VideoResolution.highest
) -> VideoMetadata:
    """It downloads the YouTube video at the given URL to the given dirpath
    
    The filename defaults to the YouTube video's title.
    """
    if proxies is None:
        proxies = {}

    url = vid_or_url

    # TODO: It may install the validators package
    if not url.startswith("http"):
        url = _URL_youtube.format(url)

    youtube = YouTube(
        url,
        proxies=proxies,
        use_oauth=use_oauth,
        allow_oauth_cache=allow_oauth_cache
    )

    youtube.check_availability()

    streams = youtube.streams.filter(file_extension=file_extension)
    stream  = _choose_stream(streams, video_resolution)

    filename = f"{stream.title}.{file_extension}"
    filepath = stream.download(output_dirpath, filename)

    caption_str  = None
    caption_type = None

    # The captions that have automatically generated by YouTube 
    # are prepended by an 'a.' prefix in the lang code
    for code in [lang_code, f"a.{lang_code}"]:
        caption = youtube.captions.get(code)

        if caption is not None:
            try:
                caption_str  = caption.generate_srt_captions()
                caption_type = CaptionType.srt
            except KeyError:
                caption_str  = caption.xml_captions
                caption_type = CaptionType.xml

            break

    return VideoMetadata(
        youtube.author,
        caption_str,
        caption_type,
        youtube.description,
        filepath,
        youtube.keywords,
        youtube.publish_date,
        youtube.rating,
        youtube.title,
        youtube.views
    )


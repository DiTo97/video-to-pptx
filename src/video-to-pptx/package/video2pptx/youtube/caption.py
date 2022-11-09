from html import unescape
from xml.etree import ElementTree

from pytube import Caption


def xml_caption_to_srt(xml_caption: str) -> str:
    """It converts YouTube .xml caption tracks to SubRip subtitles (.srt)
    
    Notes
    -----
    [#1386](https://github.com/pytube/pytube/pull/1386)

    This function is a fix for Pytube's `xml_caption_to_srt` function, which has stopped
    working since YouTube changed the format of .xml caption tracks at the end of Q2 2022.
    It should be fixed with the release of Pytube v12.2.0.
    """
    root = ElementTree.fromstring(xml_caption)

    segments = []

    for idx, child in enumerate(list(root.findall("body/p"))):
        text = child.text or ""

        if not text:
            text = "".join(child.itertext()).strip()

        if not text:
            continue

        text = text.replace("\n", " ")
        text = text.replace("  ", " ")

        caption = unescape(text)

        try:
            duration = float(child.attrib["d"])
        except KeyError:
            duration = 0.0

        t_start = float(child.attrib["t"])  # millisecs

        try:
            t_end = float(root.findall("body/p")[idx + 2].attrib["t"])
        except Exception:
            t_end = float(root.findall("body/p")[idx].attrib["t"])
            t_end = t_end + duration        # millisecs

        t_start_secs = t_start / 1000
        t_end_secs   = t_end   / 1000

        start = Caption.float_to_srt_time_format(t_start_secs)
        end   = Caption.float_to_srt_time_format(t_end_secs)

        line = f"{idx + 1}\n{start} --> {end}\n{caption}\n"

        segments.append(line)

    return "\n".join(segments).strip()

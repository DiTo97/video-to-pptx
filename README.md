# video-to-pptx

[![Generic badge](https://img.shields.io/badge/status-alpha-green.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/python-3.8%20|%203.9%20|%203.10-blue.svg)](https://shields.io/)

A video-to-PPTX-slides converter whose main goal is to convert scientific presentations to PPTX slides.

**N.B.:** The converter only supports videos hosted on YouTube for now.

The conversion process is roughly nine-fold:

- [x] The video is downloaded in memory or to file storage with the [Pytube](https://pytube.io/en/latest/index.html) package;
- [x] A sequence of frames is extracted from the video;
- [x] A sequence of subtitles is extracted from the video caption;
- [x] Too similar adjacent frames are filtered out, as they likely coincide with longer explanations by the author;
- [ ] The sequences might have to be temporally aligned by joining relevant subtitles;
- [ ] The frames in the reduced sequence are [converted to SVG](https://github.com/IngJavierR/PngToSvg) to infer their structure;
- [ ] The SVG frames are converted to unpolished PPTX slides with an [SVG-to-PPTX converter](https://github.com/udp/svg-to-pptx);
- [ ] The unpolished PPTX slides are better formalized with the [Python-PPTX](https://python-pptx.readthedocs.io/en/latest/index.html) package*;
- [ ] The captions are attached as speaker notes ([NotesSlide](https://python-pptx.readthedocs.io/en/latest/api/slides.html#notesslide-objects) objects) to their corresponding PPTX slide.


*An example of [creating a PPTX presentation with Python-PPTX](https://towardsdatascience.com/creating-presentations-with-python-3f5737824f61).  

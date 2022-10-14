# video-to-pptx

A video-to-PPTX-slides converter whose main goal is to convert scientific presentation to PPTX slides.

The conversion process is roughly nine-fold:

1. The video is downloaded in memory or to file storage with the [Pytube](https://pytube.io/en/latest/index.html) package;
2. A sequence of frames is extracted from the video;
3. A sequence of captions is extracted from the video;
4. Adjacent frames that are too similar are filtered out, as they likely coincide with longer explanations of the author;
5. If any frames have been filtered out, we might have to join some of the captions to align the sequences;
6. The frames in the reduced sequence are [converted to SVG](https://github.com/IngJavierR/PngToSvg) to infer their structure;
7. The SVG frames are converted to unpolished PPTX slides with an [SVG-to-PPTX converter](https://github.com/udp/svg-to-pptx);
8. The unpolished PPTX slides are better formalized with the [Python-PPTX](https://python-pptx.readthedocs.io/en/latest/index.html) package*;
9. The captions are attached as speaker notes ([NotesSlide](https://python-pptx.readthedocs.io/en/latest/api/slides.html#notesslide-objects) objects) to their corresponding PPTX slide.


*An example of [creating a PPTX presentation with Python-PPTX](https://towardsdatascience.com/creating-presentations-with-python-3f5737824f61).  
**N.B.:** The converter only supports videos hosted on YouTube for now.

import dataclasses
import cv2

from typing import Optional
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip
from PIL import Image
from numpy import asarray


@dataclasses.dataclass
class TextForVideo:
    """
    Represents text object for video generation
    """
    txt: str
    animation_duration: Optional[float] = None
    size: Optional[tuple] = None
    color: str = 'AntiqueWhite1'
    fontsize: int = 30
    method: str = "caption"
    font: int = 'Helvetica'
    font_scale: int = 1

    def __post_init__(self) -> None:
        """
        calculates text size and duration of future text clip
        :return: None
        """
        self.set_text_size()
        self.set_anim_duration()

    def set_anim_duration(self) -> None:
        """
        Calculates duration of text clip based on its length in pixels
        :return: None
        """
        self.animation_duration = self.size[0] / 30

    def set_text_size(self) -> None:
        """
        Calculates size of future text object in pixels
        :return: None
        """
        self.size, _ = cv2.getTextSize(self.txt, cv2.FONT_HERSHEY_SIMPLEX, self.font_scale, 2)

    def as_kwargs(self) -> dict:
        to_exclude = ['animation_duration', 'font_scale']
        return {k: v for (k, v) in self.__dict__.items() if k not in to_exclude}


class ScrollingTextMaker:
    """
    Constructor of animations with scrolling text
    """

    def __init__(self, text, image):
        self.text: str = text
        self.image: str = image
        self.width = 100
        self.height = 100
        self.duration = 10
        self.text_object: Optional[TextForVideo] = None

    def create_background(self) -> ImageClip:
        """
        Generates background for clip from image
        :return: ImageClip object
        """
        image = Image.open(self.image)
        image = image.resize((self.width, self.height))

        return ImageClip(asarray(image), duration=self.duration)

    def create_text_parameters(self) -> None:
        """
        Wraps passed and preset data  into object
        :return: TextForVideo object
        """
        self.text_object = TextForVideo(self.text)

    def generate_text_clip(self) -> TextClip:
        """
        Generates text animation based on given text and preset data
        :return: TextClip object
        """
        self.create_text_parameters()
        text_clip = TextClip(**self.text_object.as_kwargs())
        text_clip = text_clip.set_pos(lambda t: (-int(300 * t) + self.width, 'center'))
        return text_clip

    def generate_composite_clip(self) -> CompositeVideoClip:
        """
        Creates CompositeVideoClip based on given text and image (if provided)
        If no image given - uses 'neon-pink' as background
        :return: CompositeVideoClip with text, scrolling right to left
        """
        text_clip = self.generate_text_clip()
        if not self.image:
            return CompositeVideoClip([text_clip], size=(100, 100), bg_color=(254, 1, 154))
        else:
            background_clip = self.create_background()
            return CompositeVideoClip([background_clip, text_clip], size=(100, 100), use_bgclip=True)

    def create_video_from_text(self, destination: str) -> None:
        final_clip = self.generate_composite_clip()
        final_clip = final_clip.set_duration(self.duration)
        final_clip.write_videofile(destination, codec='libvpx', fps=24)
        final_clip.close()

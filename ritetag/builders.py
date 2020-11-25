from .enums import *


class ImageBuilder:

    def __init__(self, text, author=''):
        # type: (str, str) -> ImageBuilder
        # default values
        self.__data = {
            'textFont': FontList.Lora,
            'textColor': '#4f4f4f',
            'textFontWeight': FontWeightType.normal,
            'authorFont': FontList.Lato,
            'authorColor': '#e5e5e5',
            'authorFontWeight': FontWeightType.normal,
            'highlightColor': 'transparent',
            'backgroundColor1': '#000000',
            'backgroundColor2': '#000000',
            'logoUrl': 'https://cdn.ritekit.com/assets/img/common/made-with-ritekit-white.png',
            'width': 400,
            'height': 400
        }
        self.text(text).author(author)

    def text(self, text):
        # type: (str) -> ImageBuilder
        self.__data['text'] = text
        return self

    def author(self, text):
        # type: (str) -> ImageBuilder
        self.__data['author'] = text
        return self

    def text_font(self, font):
        # type: (FontList) -> ImageBuilder
        self.__data['quoteFont'] = font
        return self

    def text_font_color(self, color):
        # type: (int) -> ImageBuilder
        self.__data['quoteFontColor'] = color
        return self

    def text_font_weight(self, weight):
        # type: (int) -> ImageBuilder
        self.__data['textFontWeight'] = weight
        return self

    def author_font(self, font):
        # type: (FontList) -> ImageBuilder
        self.__data['authorFont'] = font
        return self

    def author_color(self, color):
        # type: (FontList) -> ImageBuilder
        self.__data['authorColor'] = color
        return self

    def background_color1(self, color):
        # type: (str) -> ImageBuilder
        self.__data['backgroundColor1'] = color
        return self

    def background_color2(self, color):
        # type: (str) -> ImageBuilder
        self.__data['backgroundColor2'] = color
        return self

    def brand_logo(self, url):
        # type: (str) -> ImageBuilder
        self.__data['brandLogo'] = url
        return self

    def width(self, width):
        # type: (int) -> ImageBuilder
        self.__data['width'] = width
        return self

    def height(self, height):
        # type: (int) -> ImageBuilder
        self.__data['height'] = height
        return self

    def build(self):
        return self.__data

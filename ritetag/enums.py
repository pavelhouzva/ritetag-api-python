from enum import Enum


class HashtagPosition(Enum):
    auto = 'auto'
    end = 'end'

    def __str__(self):
        return '{0}'.format(self.value)


class AnimationType(Enum):
    none = 'none'
    rays = 'rays'
    glint = 'glint'
    circle = 'circle'

    def __str__(self):
        return '{0}'.format(self.value)


class FontList(Enum):
    AlegreyaSC = 'AlegreyaSC'
    ABeeZee = 'ABeeZee'
    AmaticSC = 'AmaticSC'
    Bangers = 'Bangers'
    BungeeShade = 'BungeeShade'
    ChelseaMarket = 'ChelseaMarket'
    Courgette = 'Courgette'
    DancingScript = 'DancingScript'
    Lato_Black = 'Lato Black'
    LifeSavers = 'LifeSavers'
    Lora = 'Lora'
    Montserrat = 'Montserrat'
    PassionOne = 'PassionOne'
    PlayfairDisplay = 'PlayfairDisplay'
    SourceSansPro = 'SourceSansPro'

    def __str__(self):
        return '{0}'.format(self.value)


class BackgroundType(Enum):
    solid = 'solid',
    gradient = 'gradient'

    def __str__(self):
        return '{0}'.format(self.value)


class GradientType(Enum):
    linear = 'linear',
    radial = 'radial'

    def __str__(self):
        return '{0}'.format(self.value)

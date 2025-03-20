from anvil import app

""" Taking advantage of CSS color functions 
ref: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_colors/Relative_colors
"""


DEFAULT_COLOR = "lime"


def _clip(value: float, min_value: float, max_value: float) -> float:
    """Keep the value with in the min and max range"""
    return min(max_value, max(min_value, value))


def get_color(color: str, _path=None) -> str:
    """Get the referenced theme color as necessary
    This is recursive, so it allows theme colors to reference each other which
    allows for more descriptive theme color names.  Downside is the color does not resolve
    in the Color Scheme view.

    Args:
        color: either a color value ie. hex, rgb, etc. or a referenced theme color in the form 'theme:Color'

    Returns the first resolved color value that is not a theme color reference.
    """

    if color.startswith("theme:"):
        if _path is None:
            _path = set()

        # Handle circular references
        if color in _path:
            print(f"Warning: Circular Reference in theme colors {_path}. Using default color '{DEFAULT_COLOR}'")
            return DEFAULT_COLOR
        else:
            _path.add(color)

        # Get the referenced theme color
        next_color = app.theme_colors.get(color.lstrip("theme:"), None)

        # Handle if the requested color is not found in the theme
        if next_color is None:
            print(
                f"Warning: Theme color '{color}' not found. Using default color '{DEFAULT_COLOR}'"
            )
            return DEFAULT_COLOR

        # Dive to the next level
        return get_color(next_color, _path=_path)
    else:
        # Color is resolved, well done everyone.
        return color


def set_alpha(color: str, alpha: float) -> str:
    """Set the alpha channel for the color"""
    color = get_color(color)
    return f"rgb(from {color} r g b / {_clip(alpha, 0, 1)})"


def hue_rotate(color: str, angle: float) -> str:
    """Rotate the HSL hue by the given angle"""
    color = get_color(color)
    return f"hsl(from {color} calc(h + {angle % 360}) s l)"


def set_lightness(color: str, lightness: float) -> str:
    """Set the HSL lightness channel"""
    color = get_color(color)
    return f"hsl(from {color} h s {_clip(lightness, 0, 100)})"


def shift_lightness(color: str, lightness_shift: float) -> str:
    """Shift the HSL lightness channel"""
    color = get_color(color)
    return f"hsl(from {color} h s calc(l + {_clip(lightness_shift, -100, 100)}))"


def set_saturation(color: str, saturation: float) -> str:
    """Set the saturation of the HSL color"""
    return f"hsl(from {color} h {_clip(saturation, 0, 100)} l)"


def shift_saturation(color: str, saturation: float) -> str:
    """Shift the saturation of the HSL color"""
    return f"hsl(from {color} h calc(s + {_clip(saturation, -100, 100)}) l)"


class Color:
    def __init__(self, color: str, _info=None):
        if isinstance(color, self.__class__):
            self.__dict__.update(color.__dict__)
        else:
            self._color = get_color(color)

            self._info = _info
            if self._info is None:
                self._info = [color]

    @property
    def info(self) -> str:
        """Provide a nice representation of the color"""
        return f"Color: {', '.join(self._info)}"

    def __str__(self) -> str:
        """Get the color string on demand"""
        return str(self._color)

    def __repr__(self) -> str:
        """Provide a nice representation of the color"""
        return self.info

    @property
    def color(self) -> str:
        """ Get the CSS representation of the color
        Useful in cases where the string representation is not requested automatically
        """
        return self.__str__()
    
    def __call__(self) -> str:
        """ Force the CSS representation of the color, alias of .color """
        return self.color

    def _extend_info(self, attribute):
        return self._info + [attribute]
    
    def set_alpha(self, alpha: float):
        """Set the opacity of the color using the alpha channel
        Args: 
            alpha: alpha value between 0 and 1
        """
        _info = self._extend_info(f"alpha={alpha:.2f}")
        return Color(set_alpha(self._color, alpha), _info=_info)

    def set_lightness(self, lightness: float):
        """Override the lightness of the color in HSL space
        Args:
            lightness: lightness value between 0 (black) and 100 (white)
        """
        _info = self._extend_info(f"lightness={lightness:.0f}")
        return Color(set_lightness(self._color, lightness), _info=_info)

    def shift_lightness(self, lightness_shift: float):
        """Adjust the lightness of the color
        Args:
            lightness_shift: adjustment from current lightness value +/- 100
        """
        _info = self._extend_info(f"lightness: {lightness_shift:+.0f}")
        return Color(shift_lightness(self._color, lightness_shift), _info=_info)

    def hue_rotate(self, angle: float):
        """Rotate the hue of the color in HSL space
        Args:
            angle: Rotation angle from current hue, 0-360
        """
        angle = angle%360
        _info = self._extend_info(f"hue rotate: {angle:+.0f}")
        return Color(hue_rotate(self._color, angle), _info=_info)

    def set_saturation(self, saturation: float):
        """ Set a the saturation value of the color
        Args:
            saturation: HSL Saturation value 0-100
        """
        _info = self._extend_info(f"saturation={saturation:.0f}")
        return Color(set_saturation(self._color, saturation), _info=_info)

    def shift_saturation(self, saturation_shift: float):
        """ Shift the saturation value in the HSL space
        Args:
            saturation_shift: amount to shif the saturation +/- 100
        """
        _info = self._extend_info(f"saturation: {saturation_shift:+.0f}")
        return Color(shift_saturation(self._color, saturation_shift), _info=_info)

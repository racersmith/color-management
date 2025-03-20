from ._anvil_designer import _color_testTemplate

from .. import cm


class _color_test(_color_testTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        self.button_10.background = cm.DEFAULT_COLOR

        self.button_1.background = cm.get_color("theme:Green")

        self.button_2.background = cm.get_color("theme:MyColor")

        self.button_3.background = cm.get_color("theme:missing")

        self.button_4.background = cm.set_alpha("theme:Orange", 0.25)
        self.button_4.foreground = cm.Color("black")

        color = "mediumaquamarine"
        self.button_5.background = cm.get_color(color)
        rotate = 180 - 30
        self.button_5.text = f"hue rotate {rotate:+}"
        self.button_5.foreground = cm.hue_rotate(color, rotate)

        self.button_6.background = cm.Color("lightblue").set_lightness(20)
        self.button_6.foreground = cm.set_lightness("lightblue", 80)

        self.button_7.background = cm.Color("lightblue").shift_lightness(5)
        self.button_7.foreground = cm.shift_lightness("lightblue", -50)

        color = "darkcyan"
        self.button_8.background = (
            cm.Color(color).shift_lightness(-10).set_alpha(55).hue_rotate(30)
        )
        self.button_8.foreground = cm.Color(color)

        self.button_9.background = cm.Color("theme:Circular_A")

    def canvas_1_reset(self, **event_args):
        """This method is called when the canvas is reset and cleared, such as when the window resizes, or the canvas is added to a form."""
        c = self.canvas_1
        c.begin_path()
        c.move_to(100, 100)
        c.line_to(100, 200)
        c.line_to(200, 200)
        c.close_path()

        triangle_color = cm.Color("theme:Green")
        c.stroke_style = triangle_color.shift_lightness(-20).shift_saturation(10)
        c.line_width = 3
        c.fill_style = triangle_color.set_lightness(80).shift_saturation(-30)

        c.fill()
        c.stroke()

        c.begin_path()
        c.move_to(80, 120)
        c.line_to(80, 220)
        c.line_to(180, 220)
        c.close_path()

        triangle_color_2 = triangle_color.hue_rotate(120)
        c.stroke_style = triangle_color_2
        c.line_width = 3
        c.fill_style = triangle_color_2.set_alpha(0.5)

        c.fill()
        c.stroke()

        # Set the stroke and fill styles
        color = cm.Color("theme:Orange")
        c.stroke_style = color.set_lightness(20)
        c.line_width = 3
        c.fill_style = color.set_lightness(80)

        # Draw a filled rectangle
        c.fill_rect(300, 100, 50, 75)

        c.fill_style = cm.Color("theme:MyColor").set_alpha(0.5)
        # Draw a filled rectangle
        c.fill_rect(275, 50, 150, 75)

        # Draw a rectangle outline 25 pixels right of it
        c.stroke_rect(325, 100, 50, 75)

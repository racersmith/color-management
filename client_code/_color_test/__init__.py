from ._anvil_designer import _color_testTemplate

from .. import cm

from anvil import Button
from anvil import app


class _color_test(_color_testTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        for color_name, color_value in app.theme_colors.items():
            theme_color = f"theme:{color_name}"
            self.add_button(
                button_color=cm.Color(theme_color), 
                text_color=cm.Color("black")
            )

        self.add_button(
            button_color=cm.DEFAULT_COLOR, 
            text_color="black", 
            text="DEFAULT_COLOR"
        )
        
        self.add_button(
            button_color=cm.Color("theme:missing"), 
            text_color=cm.Color("black")
        )
        
        self.add_button(
            button_color=cm.Color("theme:Orange").set_alpha(0.5),
            text_color=cm.Color("black"),
        )

        color = cm.Color("mediumaquamarine")
        self.add_button(
            button_color=color.hue_rotate(180), 
            text_color=color.shift_lightness(+25)
        )

        color = cm.Color("lightblue")
        self.add_button(
            button_color=color, 
            text_color=color.set_lightness(10)
        )

        color = cm.Color("lightblue")
        self.add_button(
            button_color=color.set_lightness(20), 
            text_color=color.set_lightness(80)
        )

        color = cm.Color("lightblue")
        self.add_button(
            button_color=color.shift_lightness(-30),
            text_color=color.shift_lightness(30),
        )

        color = cm.Color("darkcyan")
        self.add_button(
            button_color=color.shift_lightness(-10).set_alpha(60).hue_rotate(30),
            text_color=color,
        )

    def add_button(self, button_color, text_color, text=None):
        if text is None:
            text = button_color.info
        button = Button(text=text, background=button_color, foreground=text_color)
        self.flow_panel_1.add_component(button)

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

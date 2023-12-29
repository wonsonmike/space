import arcade
import game_one


SPRITE_SCALING = .0006 # .5 at minimum
MOVEMENT_SPEED = 7
BULLET_SPEED = 25
MAX_PISTOL_BULLETS = 5
ROUND_TIME = 15

class FullWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)
        self.set_minimum_size(800,600)
        # Set movement variables
        self.movement_speed = (MOVEMENT_SPEED/800) * width
        self.bullet_speed = (BULLET_SPEED/600) * height

        # Set sprite scaling
        self.sprite_scaling = SPRITE_SCALING * width

        # Set initial score to zero
        self.total_score = 0

    def on_resize(self, width, height):
        # Adjust movement speed
        self.movement_speed = (MOVEMENT_SPEED/800) * width

        # Adjust bullet speed
        self.bullet_speed = (BULLET_SPEED/600) * height

        # Adjust sprite scaling
        self.sprite_scaling = SPRITE_SCALING * width
        super().on_resize(width, height)

class Player(arcade.Sprite):

    def update(self):
        # Move player.
        self.center_x += self.change_x
        self.center_y += self.change_y

class MenuView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        # Draw the welcome screen
        self.clear()
        # Each draw_text is based on the window's width and height, so the text will dynamically change size if the window size is changed
        arcade.draw_text("Welcome to Space Invaders", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=(self.window.width/20), anchor_x="center")
        arcade.draw_text("Press any key to advance", self.window.width / 2, self.window.height / 2 - (self.window.width/5),
                         arcade.color.GRAY, font_size=(self.window.width/40), anchor_x="center")

    def on_key_press(self, key, modifiers):
        # Move to Instructions
        instructions_view = game_one.InstructionOneView()
        self.window.show_view(instructions_view)


def main():
    # Make a new window
    window = FullWindow(800, 600, "Space Invaders")

    # Start at the main menu
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()

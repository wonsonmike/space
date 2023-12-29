import arcade
#from main import MenuView, Player,  MOVEMENT_SPEED, BULLET_SPEED, MAX_PISTOL_BULLETS, ROUND_TIME, SPRITE_SCALING

class InstructionTwoView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.GRAY)

    def on_draw(self):
        # Draw instructions
        self.clear()
        arcade.draw_text("Instructions", self.window.width / 2, self.window.height / 1.2,
                         arcade.color.BLACK, font_size=(self.window.width/13), anchor_x="center")
        arcade.draw_text("Use the arrow keys or WASD to move your spaceship, and the space bar to shoot lasers.", self.window.width / 2, self.window.height / 2 + (self.window.height/15),
                         arcade.color.WHITE, font_size=(self.window.width/55), anchor_x="center")
        arcade.draw_text("Shoot all alien robots with lasers to win. Each round, there are more and more robots.", self.window.width / 2, self.window.height / 2 + (self.window.height/40),
                         arcade.color.WHITE, font_size=(self.window.width/55), anchor_x="center")
        arcade.draw_text("If your spaceship hits an alien robot, you lose a life. If you lose all lives, it's game over.", self.window.width / 2, self.window.height / 2 - (self.window.height/40),
                         arcade.color.WHITE, font_size=(self.window.width/55), anchor_x="center")
        arcade.draw_text("You have 15 seconds each round. If you don't shoot all robots in that time, it's game over.", self.window.width / 2, self.window.height / 2 - (self.window.height/15),
                         arcade.color.WHITE, font_size=(self.window.width/55), anchor_x="center")
        arcade.draw_text("Press the space bar to start playing", self.window.width / 2, self.window.height / 5,
                         arcade.color.BLACK, font_size=(self.window.width/40), anchor_x="center")

    def on_key_press(self, key, modifiers):
        # Set the total score and lives for the starting round 
        self.window.total_score = 0
        self.window.lives = 3
        # On the space bar press, start the game
        if key == arcade.key.SPACE:
            game_view = GameTwoView()
            self.window.show_view(game_view)

class GameTwoView(arcade.View):
    pass
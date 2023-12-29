import arcade
import random
from main import MenuView, Player,  MOVEMENT_SPEED, BULLET_SPEED, MAX_PISTOL_BULLETS, ROUND_TIME, SPRITE_SCALING

class InstructionOneView(arcade.View):
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
            game_view = GameOneView()
            self.window.show_view(game_view)

class GameOneView(arcade.View):
    def __init__(self):
        super().__init__()

        # Load resources
        self.background = arcade.load_texture(":resources:images/backgrounds/stars.png")
        self.gun_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hit5.wav")
        self.dead_sound = arcade.load_sound(":resources:sounds/explosion2.wav")


        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        # Set up the player
        self.score = 0
        self.timer = ROUND_TIME # Number of seconds to finish the round
        self.player_sprite = Player(":resources:images/space_shooter/playerShip3_orange.png", self.window.sprite_scaling)
        self.player_sprite.center_x = self.window.width / 2
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # If the player lost lives in a previous round, give them one more life
        if (self.window.lives < 3):
            self.window.lives += 1
    
        # Create 3 enemies, plus a random amount based on the total score. So, it gets harder each round
        for i in range(random.randrange(self.window.total_score + 1) + 3):
            # Create the enemy instance
            enemy = arcade.Sprite(":resources:images/animated_characters/robot/robot_idle.png", self.window.sprite_scaling)

            # Position the enemy based on the window size
            enemy.x_percent = (random.randrange(self.window.width - 40) + 20)/self.window.width
            enemy.center_x = enemy.x_percent * self.window.width
            enemy.y_percent = (random.randrange(self.window.height - 200) + 180)/self.window.height
            enemy.center_y = enemy.y_percent * self.window.height

            # Add the enemy to the lists
            self.enemy_list.append(enemy)

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.w_pressed = False
        self.a_pressed = False
        self.s_pressed = False
        self.d_pressed = False

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

        # Don't show the mouse cursor
        self.window.set_mouse_visible(False)

    def on_draw(self):
        self.clear()
        
        # Set the background
        arcade.draw_lrwh_rectangle_textured(0, 0, self.window.width, self.window.height, self.background)

        # Draw all the sprites.
        self.player_list.draw()
        self.enemy_list.draw()
        self.bullet_list.draw()

        # Draw the lives in the bottom corner
        for i in range(self.window.lives):
            self.live = arcade.Sprite(":resources:images/space_shooter/playerShip3_orange.png", (0.000333*self.window.height))
            self.live.center_x = (i * 30) + 30
            self.live.center_y = 30
            self.live.draw()

        # Put the score and time remaining on the screen
        arcade.draw_text(f"Time left: {int(self.timer)}", 10, (40/600*self.window.height) + 50, arcade.color.WHITE, (14/800*self.window.width))
        arcade.draw_text(f"Score: {self.score}", 10, (20/600*self.window.height) + 50, arcade.color.WHITE, (14/800*self.window.width))
        arcade.draw_text(f"Total Score: {self.window.total_score}", 10, 50, arcade.color.WHITE, (14/800*self.window.width))

    def on_resize(self, width: int, height: int):
        # Adjust movement speed
        self.window.movement_speed = (MOVEMENT_SPEED/800) * width

        # Adjust bullet speed
        self.window.bullet_speed = (BULLET_SPEED/600) * height

        # Adjust sprite size
        self.window.sprite_scaling = SPRITE_SCALING * width
        self.player_sprite.scale = self.window.sprite_scaling
        for enemy in self.enemy_list:
            enemy.scale = self.window.sprite_scaling

        # Adjust enemy location
        for enemy in self.enemy_list:
            enemy.center_x = enemy.x_percent * width
            enemy.center_y = enemy.y_percent * height

        return super().on_resize(width, height)

    def update_player_speed(self):
        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        # Go up
        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y += self.window.movement_speed
        elif self.w_pressed and not self.s_pressed:
            self.player_sprite.change_y += self.window.movement_speed

        # Go down
        if self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y -= self.window.movement_speed
        elif self.s_pressed and not self.w_pressed:
            self.player_sprite.change_y -= self.window.movement_speed

        # Go left
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x -= self.window.movement_speed
        elif self.a_pressed and not self.d_pressed:
            self.player_sprite.change_x -= self.window.movement_speed

        # Go right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x += self.window.movement_speed
        elif self.d_pressed and not self.a_pressed:
            self.player_sprite.change_x += self.window.movement_speed

    def update_bullets(self):
        # Only allow the user so many bullets on screen at a time to prevent them from spamming bullets.
        if len(self.bullet_list) < MAX_PISTOL_BULLETS:
            # Gunshot sound
            arcade.play_sound(self.gun_sound)

            # Create a bullet
            bullet = arcade.Sprite(":resources:images/space_shooter/laserRed01.png", self.window.sprite_scaling * 2)

            # Give the bullet a speed
            bullet.change_y = self.window.bullet_speed

            # Position the bullet
            bullet.center_x = self.player_sprite.center_x
            bullet.bottom = self.player_sprite.top

            # Add the bullet to the appropriate list
            self.bullet_list.append(bullet)

    def handle_collisions(self):
        # Check for bullet hits
        for bullet in self.bullet_list:
            # Check this bullet to see if it hit an enemy
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

            # For every enemy we hit, add to the score and remove the enemy
            for enemy in hit_list:
                enemy.remove_from_sprite_lists()
                self.score += 1
                self.window.total_score += 1

                # Hit Sound
                arcade.play_sound(self.hit_sound)

            # If the bullet flies off-screen, remove it.
            if bullet.bottom > self.window.height:
                bullet.remove_from_sprite_lists()

        # Check if the player hit an enemy
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)

        if len(hit_list) > 0:
            arcade.play_sound(self.dead_sound)
            self.player_sprite.center_x = self.window.width / 2
            self.player_sprite.center_y = 50
        # Any hit enemies are killed, and a life is removed
        for enemy in hit_list:
            enemy.remove_from_sprite_lists()
            self.window.lives -= 1

    def on_update(self, delta_time):

        # Call update on all sprites
        self.enemy_list.update()
        self.player_list.update()
        self.bullet_list.update()

        # Check for out-of-bounds of the player
        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        elif self.player_sprite.right > self.window.width - 1:
            self.player_sprite.right = self.window.width - 1

        if self.player_sprite.bottom < 0:
            self.player_sprite.bottom = 0
        elif self.player_sprite.top > self.window.height - 1:
            self.player_sprite.top = self.window.height - 1

        # Generate a list of all sprites that collided with the player.
        self.handle_collisions()

        # Update timer
        self.timer -= delta_time
        
        # If the player used their last life, the game is over
        if self.window.lives <= 0:
            game_over_view = GameOneOverView()
            self.window.show_view(game_over_view)

        # If the timer is up, the game is over
        if self.timer < 0:
            self.timer = 0
            game_over_view = GameOneOverView()
            self.window.show_view(game_over_view)

        # If we've shot all enemies, they won that round
        if (len(self.enemy_list) == 0) & (self.window.lives > 0):
            game_win_view = GameOneWinView()
            self.window.show_view(game_win_view)

    def on_key_press(self, key, modifiers):

        # Update the player movement keys
        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.W:
            self.w_pressed = True
        elif key == arcade.key.A:
            self.a_pressed = True
        elif key == arcade.key.S:
            self.s_pressed = True
        elif key == arcade.key.D:
            self.d_pressed = True

        # Update the player bullets
        elif key == arcade.key.SPACE:
            self.update_bullets()

        # Update the player's speed
        self.update_player_speed()

    def on_key_release(self, key, modifiers):

        # Update the player movement keys
        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
        elif key == arcade.key.W:
            self.w_pressed = False
        elif key == arcade.key.A:
            self.a_pressed = False
        elif key == arcade.key.S:
            self.s_pressed = False
        elif key == arcade.key.D:
            self.d_pressed = False

        # Update the player's speed
        self.update_player_speed()

class GameOneWinView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

        # Play the sound
        self.gamewin_sound = arcade.load_sound(":resources:sounds/upgrade1.wav")
        arcade.play_sound(self.gamewin_sound)

        # Show the mouse cursor
        self.window.set_mouse_visible(True)

    def on_draw(self):
        self.clear()

        # Draw the text that they beat that round
        arcade.draw_text("You won! ", self.window.width / 2, self.window.height / 1.5, arcade.color.WHITE, font_size=(.0625 * self.window.width), anchor_x="center")
        arcade.draw_text("Press the E key to play the next round", self.window.width / 2, self.window.height / 2, arcade.color.WHITE, font_size=(.025 * self.window.width), anchor_x="center")

        # Show them the current score
        arcade.draw_text(f"Total Score: {self.window.total_score}", self.window.width / 2, self.window.height / 3, arcade.color.WHITE, font_size=(.025 * self.window.width), anchor_x="center")

    def on_key_press(self, key, modifiers):
        # Wait for the E key, then start the next round
        if key == arcade.key.E:
            game_view = GameOneView()
            self.window.show_view(game_view)

class GameOneOverView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

        # Play the sound
        self.gameover_sound = arcade.load_sound(":resources:sounds/gameover3.wav")
        arcade.play_sound(self.gameover_sound)

        # Show the mouse cursor
        self.window.set_mouse_visible(True)

    def on_draw(self):
        self.clear()
        
        # Draw the text that their game is over
        arcade.draw_text("Game Over", self.window.width / 2, self.window.height / 1.5, arcade.color.WHITE, font_size=(.0625 * self.window.width), anchor_x="center")
        arcade.draw_text("Press the E key to go back home", self.window.width / 2, self.window.height / 2, arcade.color.WHITE, font_size=(.025 * self.window.width), anchor_x="center")

        # Show their final score
        arcade.draw_text(f"Final Score: {self.window.total_score}", self.window.width / 2, self.window.height / 3, arcade.color.WHITE, font_size=(.025 * self.window.width), anchor_x="center")

    def on_key_press(self, key, modifiers):
        # Wait for the E key, then go back to the home menu
        if key == arcade.key.E:
            game_view = MenuView()
            self.window.show_view(game_view)

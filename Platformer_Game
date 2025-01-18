import pygame
import random
import sys
import os
import json

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game settings
PLATFORM_SINK_SPEED = 1
PLAYER_SPEED = 8
JUMP_STRENGTH = 10
GRAVITY = 0.4
PLATFORM_HEIGHT = 20
PLATFORM_WIDTH = 100
VERTICAL_PLATFORM_SPACING = 100
INSERTABLE_PLATFORM_WIDTH = 80
INSERTABLE_PLATFORM_HEIGHT = 15

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """
        Initialize a new player sprite.

        This method initializes a new player sprite by loading in the necessary images, setting the initial position and velocity, and setting the number of lives and insertable platforms.

        Args:
            x: The x-coordinate of the player
            y: The y-coordinate of the player
        """
        super().__init__()
        self.image_locations = [
            os.path.join("assets", "player_side1.png"),
            os.path.join("assets", "player_side2.png"),
            os.path.join("assets", "player_side3.png")
        ]
        self.images = [pygame.image.load(location).convert_alpha() for location in self.image_locations]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.lives = 5
        self.insertable_platforms = 15  # New attribute for insertable platforms
        
        self.walk_timer = 0
        self.walk_frame = 0

    def update(self, platforms):
        """
        Update the player's position and state based on user input and platform collisions.

        This function handles the following:
        - Captures keyboard input for horizontal movement and jumping.
        - Updates the player's velocity and position.
        - Checks for platform insertion input.
        - Applies gravity to the player.
        - Updates the player's walking animation.
        - Prevents the player from moving outside the screen boundaries.
        - Handles collisions with platforms, allowing the player to land or be blocked by platforms.

        Args:
            platforms: A list of platform objects that the player can collide with.
        
        Returns:
            A string "INSERT_PLATFORM" if the player requests to insert a platform, otherwise None.
        """
        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        self.velocity_x = 0
        if keys[pygame.K_LEFT]:
            self.velocity_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.velocity_x = PLAYER_SPEED

        # Jumping
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -JUMP_STRENGTH
            self.on_ground = False

        # Platform insertion
        if keys[pygame.K_DOWN] and self.insertable_platforms > 0:
            return "INSERT_PLATFORM"

        # Apply gravity
        self.velocity_y += GRAVITY
        
        # Horizontal movement
        new_x = self.rect.x + self.velocity_x
        # Prevent player from exiting screen
        new_x = max(0, min(new_x, SCREEN_WIDTH - self.rect.width))
        self.rect.x = new_x

        # Vertical movement
        old_rect = self.rect.copy()
        self.rect.y += self.velocity_y
        self.on_ground = False
        
        # Update walk animation
        self.walk_timer += 1
        if self.walk_timer >= 10:
            self.walk_timer = 0
            self.walk_frame = (self.walk_frame + 1) % len(self.images)

        # Set image based on direction and walk frame
        if self.velocity_x > 0:
            self.image = self.images[self.walk_frame]
        elif self.velocity_x < 0:
            self.image = pygame.transform.flip(self.images[self.walk_frame], True, False)

        # Platform collision
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Colliding from top (landing on platform)
                if old_rect.bottom <= platform.rect.top and self.rect.bottom > platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                
                # Colliding from bottom (hitting platform from underneath)
                elif old_rect.top >= platform.rect.bottom and self.rect.top < platform.rect.bottom:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0

class Enemy(pygame.sprite.Sprite):
    """
    A class representing an enemy sprite in the game.

    The enemy moves horizontally across the screen and reverses direction
    when it hits the screen edges. It also sinks downward over time with
    the platform sink speed.

    Attributes:
        image (pygame.Surface): The image of the enemy sprite.
        rect (pygame.Rect): The rectangle defining the enemy's position.
        direction (int): The horizontal direction of movement (-1 for left, 1 for right).
        speed (int): The speed at which the enemy moves horizontally.
    """

    def __init__(self, x, y):
        """
        Initialize an enemy sprite.

        Args:
            x (int): The x-coordinate of the enemy.
            y (int): The y-coordinate of the enemy.
        """
        super().__init__()
        self.image = pygame.image.load(os.path.join("assets", "enemy.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = random.choice([-1, 1])
        self.speed = 2

    def update(self):
        """
        Update the enemy's position.

        Moves the enemy horizontally and vertically according to its speed
        and direction. Reverses direction when hitting screen edges and
        occasionally changes direction randomly.
        """
        self.rect.x += self.speed * self.direction
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.direction *= -1
        if pygame.time.get_ticks() % 50 == 0:
            self.direction = random.choice([-1, 1])
        self.rect.y += PLATFORM_SINK_SPEED

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width=None):
        """
        Create a new platform.
        
        Args:
            x: The x-coordinate of the platform
            y: The y-coordinate of the platform
            width: The width of the platform (optional). If not specified, a random width between 100 and 180 will be used.
        """
        super().__init__()
        self.tile_image = pygame.image.load(os.path.join("assets", "platform_tile.png")).convert_alpha()
        self.tile_image = pygame.transform.scale(self.tile_image, (self.tile_image.get_width(), 20))  # scale image to 20px tall
        self.tile_width = self.tile_image.get_width()
        if width is None:
            width = random.randint(100, 180)
        self.image = pygame.Surface((width, self.tile_image.get_height()))
        self.image.set_colorkey((0, 0, 0))  # set black as transparent color
        for i in range(width // self.tile_width + 1):
            self.image.blit(self.tile_image, (i * self.tile_width, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        self.is_insertable = width != PLATFORM_WIDTH

    def update(self):
        # Sink downward
        self.rect.y += PLATFORM_SINK_SPEED

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join("assets", "coin.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()

class Game:
    def __init__(self):
        """
        Initialize a new game.

        This method initializes a new game by setting up the pygame display, clock, and sprite groups.
        It also creates a new player and adds it to the sprite groups.
        Finally, it sets the score and loads the background, lava, and heart images.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Platformer Game")
        self.clock = pygame.time.Clock()
        
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        
        self.player = Player(SCREEN_WIDTH // 2, 100)
        self.all_sprites.add(self.player)
        
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.PLATFORM_SINK_SPEED = PLATFORM_SINK_SPEED
        
        # Initial platform generation
        self.generate_initial_platforms()
        
        self.PLATFORM_SINK_SPEED = 1
        self.last_platform_insertion = 0
        self.last_platform_insertion_time = 0
        
        self.background_image = pygame.image.load(os.path.join("assets", "stage.png")).convert_alpha()
        self.background_rect = self.background_image.get_rect()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background_rect.x = 0
        self.background_rect.y = 0
        
        self.lava_image = pygame.image.load(os.path.join("assets", "lava.png")).convert_alpha()
        self.lava_rects = []
        self.lava_spawn_timer = 0
        self.lava_spawn_interval = 400  # Initial spawn interval
        
        self.heart_image = pygame.image.load(os.path.join("assets", "heart.tiff")).convert_alpha()
        self.heart_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "heart.tiff")).convert_alpha(), (30, 30))
        self.heart_rects = []
        self.heart_spawn_timer = 0
        self.heart_spawn_interval = random.randint(200, 1000)  # Initial spawn interval
        
        self.platform_heart_image = pygame.image.load(os.path.join("assets", "blueheart.tiff")).convert_alpha()
        self.platform_heart_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "blueheart.tiff")).convert_alpha(), (30, 30))
        self.platform_heart_rects = []
        self.platform_heart_spawn_timer = 0
        self.platform_heart_spawn_interval = random.randint(200, 1000)  # Initial spawn interval
        
        self.enemies = []
        self.enemy_spawn_timer = 0
        self.enemy_spawn_interval = 1000  # Initial spawn interval
        self.enemy_image = pygame.image.load(os.path.join("assets", "enemy.png")).convert_alpha()
        
        self.highscore = self.load_highscore()
        
        self.coin_spawn_timer = 0
        self.coin_spawn_interval = 7000  # initial spawn interval (10 seconds)
        self.coins = pygame.sprite.Group()

    def generate_initial_platforms(self):
        # Generate platforms from top to bottom with consistent vertical spacing
        """
        Generates initial platforms from top to bottom with consistent vertical spacing.
        At least one platform is generated per vertical level, with a random horizontal position.
        A platform is also generated directly below the player's starting position.
        """
        for y in range(0, SCREEN_HEIGHT, VERTICAL_PLATFORM_SPACING):
            # Ensure at least one platform per vertical level
            x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
            platform = Platform(x, y)
            self.platforms.add(platform)
            self.all_sprites.add(platform)

        player_x = self.player.rect.x
        player_y = self.player.rect.y
        platform = Platform(player_x - (PLATFORM_WIDTH / 2) + (self.player.rect.width / 2), player_y + self.player.rect.height)
        self.platforms.add(platform)
        self.all_sprites.add(platform)

    def generate_new_platform(self):
        # Generate a new platform at the top of the screen
        """
        Generates a new platform at a random horizontal position at the top of the screen.
        The platform is added to the platforms and all_sprites groups.
        """
        x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
        platform = Platform(x, 0)
        self.platforms.add(platform)
        self.all_sprites.add(platform)

    def insert_platform(self):
        # Insert a platform just below the player
        """
        Inserts a platform directly below the player's current position if there are
        insertable platforms available. This function checks the player's available
        insertable platforms, calculates the position for the new platform, creates
        it, and adds it to the platforms and all_sprites groups. It also decrements
        the player's count of insertable platforms by one.
        """
        if self.player.insertable_platforms > 0:
            x = self.player.rect.x + (self.player.rect.width - INSERTABLE_PLATFORM_WIDTH) // 2
            y = self.player.rect.bottom
            platform = Platform(x, y, INSERTABLE_PLATFORM_WIDTH)
            self.platforms.add(platform)
            self.all_sprites.add(platform)
            self.player.insertable_platforms -= 1

    def reset_game(self):
        """
        Resets the game state if the player has lives remaining. This function:
        * Decrements the player's lives by 1
        * Resets the player's y position to 100
        * Resets the player's insertable platforms to 50
        * Clears all existing platforms and hearts
        * Regenerates new platforms with generate_initial_platforms()
        * Returns True if the player still has lives remaining, False otherwise.
        """
        if self.player.lives > 0:
            self.player.lives -= 1
            self.player.rect.y = 100  # Reset insertable platforms
            # Clear existing platforms and hearts
            for sprite in list(self.platforms):
                sprite.kill()
            
            # Regenerate platforms
            self.generate_initial_platforms()
            return True
        return False
    
    def add_lava_block(self):
        """
        Spawns a lava block at a random x position at the top of the screen.
        The block is added to the list of lava rects.
        """
        rect = self.lava_image.get_rect()
        rect.x = random.randint(0, SCREEN_WIDTH - rect.width)
        rect.y = -rect.height
        self.lava_rects.append(rect)
        
    def add_heart(self):
        """
        Spawns a heart at a random x position at the top of the screen.
        The heart is added to the list of hearts.
        """
        rect = self.heart_image.get_rect()
        rect.x = random.randint(0, SCREEN_WIDTH - rect.width)
        rect.y = -rect.height
        self.heart_rects.append(rect)

    def add_enemy(self):
        """
        Spawns an enemy at a random x position on the highest platform.
        The enemy is added to the list of enemies.
        """
        platforms = self.platforms.sprites()
        highest_platform = min(platforms, key=lambda platform: platform.rect.y)
        enemy = Enemy(highest_platform.rect.x + random.randint(0, highest_platform.rect.width - self.enemy_image.get_width()), highest_platform.rect.y - self.enemy_image.get_height())
        self.enemies.append(enemy)

    def add_platform_heart(self):
        """
        Spawns a platform heart at a random x position at the top of the screen.
        The platform heart is added to the list of platform hearts.
        """
        rect = self.platform_heart_image.get_rect()
        rect.x = random.randint(0, SCREEN_WIDTH - rect.width)
        rect.y = -rect.height
        self.platform_heart_rects.append(rect)

    def load_highscore(self):
        """
        Loads the current highscore from a file named highscore.json in the current directory.
        If the file does not exist, returns 0.

        Returns:
            int: The current highscore.
        """
        try:
            with open('highscore.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return 0

    def save_highscore(self):
        """
        Saves the current highscore to a file named highscore.json in the current directory.

        This method takes the current highscore and saves it to a file, overwriting any existing value.
        """
        with open('highscore.json', 'w') as f:
            json.dump(self.highscore, f)

    def update_highscore(self, score):
        """
        Updates the highscore if the given score is greater than the current highscore.

        This method compares the provided score with the stored highscore and updates
        the highscore if the provided score is higher. It then saves the updated highscore
        to a file.

        Args:
            score (int): The score to compare against the current highscore.
        """
        if score > self.highscore:
            self.highscore = score
            self.save_highscore()
   
    def spawn_coin(self):
        """
        Spawns a new coin object and adds it to the necessary sprite groups.
        
        This method creates a new coin object and adds it to the coins and all_sprites
        sprite groups. The coin is given a random x-coordinate and placed at the top
        of the screen.
        """
        coin = Coin()
        self.coins.add(coin)
        self.all_sprites.add(coin)

    def handle_coin_collision(self, coin):
        """
        Handles a collision between the player and a coin.

        When a coin is collected, this method increases the player's lives and
        insertable platforms by 20, and kills the coin. It also decreases the
        interval between coin spawns by 10%.

        Args:
            coin: The coin that was collected.
        """
        self.player.insertable_platforms += 20
        self.player.lives += 20
        coin.kill()
        self.coin_spawn_interval *= 0.9  # decrease spawn interval by 10%

    def run(self):
        """
        Runs the game loop until the game is over.
        
        This method is responsible for updating all game objects, checking for collisions,
        and drawing the game state to the screen. It also handles the game over screen
        and saves the highscore if necessary.
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if pygame.time.get_ticks() % 1000 == 0:
                self.PLATFORM_SINK_SPEED += 1
            # Update game objects
            player_update_result = self.player.update(self.platforms)
            
            # Update platforms and move down
            for platform in self.platforms:
                platform.update()
                
            self.coin_spawn_timer += 1
            if self.coin_spawn_timer >= self.coin_spawn_interval:
                self.coin_spawn_timer = 0
                self.coin_spawn_interval *= 0.9
                self.spawn_coin()

            self.coins.update()

            self.enemy_spawn_timer += 1
            if self.enemy_spawn_timer >= self.enemy_spawn_interval:
                self.enemy_spawn_timer = 0
                self.enemy_spawn_interval *= 0.97  # Decrease spawn interval over time
                self.add_enemy()

            # Update enemies
            for enemy in self.enemies[:]:
                enemy.update()
                if self.player.rect.colliderect(enemy.rect):
                    self.player.lives -= 1
                    self.enemies.remove(enemy)

            self.heart_spawn_timer += 1
            if self.heart_spawn_timer >= self.heart_spawn_interval:
                self.heart_spawn_timer = 0
                self.heart_spawn_interval = random.randint(200, 1500)  # Decrease spawn interval over time
                self.add_heart()

            # Update hearts
            for rect in self.heart_rects[:]:
                rect.y += 2  # Move hearts down
                if rect.y > SCREEN_HEIGHT:
                    self.heart_rects.remove(rect)
                if self.player.rect.colliderect(rect):
                    self.heart_rects.remove(rect)
                    self.player.lives += 1
                    
            self.platform_heart_spawn_timer += 1
            if self.platform_heart_spawn_timer >= self.platform_heart_spawn_interval:
                self.platform_heart_spawn_timer = 0
                self.platform_heart_spawn_interval = random.randint(200, 1500)  # Decrease spawn interval over time
                self.add_platform_heart()

            # Update platform hearts
            for rect in self.platform_heart_rects[:]:
                rect.y += 2  # Move platform hearts down
                if rect.y > SCREEN_HEIGHT:
                    self.platform_heart_rects.remove(rect)
                if self.player.rect.colliderect(rect):
                    self.platform_heart_rects.remove(rect)
                    self.player.insertable_platforms += 1
                    
            self.lava_spawn_timer += 1
            if self.lava_spawn_timer >= self.lava_spawn_interval:
                self.lava_spawn_timer = 0
                self.lava_spawn_interval *= 0.98  # Decrease spawn interval over time
                self.add_lava_block()

            # Update lava blocks
            for rect in self.lava_rects:
                if pygame.time.get_ticks() % 2000 == 0:
                    rect.y += 10
                else:
                    rect.y += 2  # Move lava blocks down
                if rect.y > SCREEN_HEIGHT:
                    self.lava_rects.remove(rect)
                if self.player.rect.colliderect(rect):
                    self.lava_rects.remove(rect)
                    self.player.lives -= 1

            # Check for collisions with lava blocks
            for rect in self.lava_rects:
                if self.player.rect.colliderect(rect):
                    # Handle collision with lava block
                    self.player.lives -= 1

            # Check if player touches ground or bottom of screen
            if (self.player.rect.bottom >= SCREEN_HEIGHT or all(platform.rect.top >= SCREEN_HEIGHT for platform in self.platforms)):
                if not self.reset_game():
                    running = False

            if player_update_result == "INSERT_PLATFORM":
                current_time = pygame.time.get_ticks()
                if current_time - self.last_platform_insertion >= 500:  # Check if 1 second has passed since the last platform insertion
                    self.insert_platform()
                    self.last_platform_insertion = current_time

            # Remove off-screen platforms and hearts
            for platform in list(self.platforms):
                if platform.rect.top >= SCREEN_HEIGHT:
                    platform.kill()
            
            if self.player.lives <= 0:
                running = False

            # Generate new platforms to maintain consistent coverage
            while pygame.time.get_ticks() - self.last_platform_insertion_time >= random.randint(800, 2100):
                self.last_platform_insertion_time = pygame.time.get_ticks()
                self.generate_new_platform()

            # Increase score
            self.score += 0.01

            # Draw
            self.screen.blit(self.background_image, self.background_rect)
            self.screen.blit(self.background_image, self.background_rect)
            for rect in self.lava_rects:
                self.screen.blit(self.lava_image, rect)
            for rect in self.heart_rects:
                self.screen.blit(self.heart_image, rect)
            for rect in self.platform_heart_rects:
                self.screen.blit(self.platform_heart_image, rect)
            for enemy in self.enemies:
                self.screen.blit(enemy.image, enemy.rect)
            hits = pygame.sprite.spritecollide(self.player, self.coins, True)
            for coin in hits:
                self.handle_coin_collision(coin)
            self.all_sprites.draw(self.screen)

            # Draw score, lives, and insertable platforms
            score_text = self.font.render(f'Score: {round(self.score)}', True, BLACK)
            lives_text = self.font.render(f'Lives: {self.player.lives}', True, BLACK)
            platforms_text = self.font.render(f'Platforms: {self.player.insertable_platforms}', True, BLACK)
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(lives_text, (10, 50))
            self.screen.blit(platforms_text, (10, 90))
            
            pygame.display.flip()
            self.clock.tick(60)

        # Game over screen
        self.screen.fill(WHITE)
        game_over_text = self.font.render(f'Game Over!       Score: {round(self.score)}        Highscore: {round(self.highscore)}', True, BLACK)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(game_over_text, text_rect)
        pygame.display.flip()
        self.update_highscore(round(self.score))
        print(f"\n\nGame Over!   Your score: {round(self.score)}     Highscore: {round(self.highscore)}\n")
        
        pygame.time.wait(1500)
        pygame.quit()
        sys.exit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()

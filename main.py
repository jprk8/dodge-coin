import pygame
from random import randint

class DodgeCoin:
    def __init__(self):
        pygame.init()

        self.width, self.height = 640, 480
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Dodge Coin")

        self.robot = pygame.image.load("robot.png")
        self.robot_x = self.width / 2 - self.robot.get_width() / 2
        self.robot_y = self.height - self.robot.get_height()
        self.to_left = False
        self.to_right = False
        self.robot_speed = 5

        self.monster = pygame.image.load("monster.png")
        self.monsters = []

        self.coin = pygame.image.load("coin.png")
        self.coins = []

        self.points = 0
        self.game_font = pygame.font.SysFont("Arial", 24)

        self.clock = pygame.time.Clock()
        self.running = True

        self.main_loop()
    
    def spawn_monster(self):
        x = randint(0, self.width - self.monster.get_width())
        y = randint(-self.height, 0)
        self.monsters.append([x, y])
    
    def spawn_coins(self):
        x = randint(0, self.width - self.monster.get_width())
        y = randint(-self.height, 0)
        self.coins.append([x, y])

    def update_monsters(self):
        if randint(1, 30) == 1:
            self.spawn_monster()
        
        new_monsters = []
        for pos in self.monsters:
            x, y = pos
            if self.check_collision(x, y):
                self.points = 0
                return
            y += 5
            if y < self.height - self.monster.get_height():
                new_monsters.append([x, y])
        
        self.monsters = new_monsters

    def update_coins(self):
        if randint(1, 200) == 1:
            self.spawn_coins()
        
        new_coins = []
        for pos in self.coins:
            x, y = pos
            if self.check_collision(x, y):
                self.points += 1
                y += self.height
            y += 5
            if y < self.height - self.coin.get_height():
                new_coins.append([x, y])
        
        self.coins = new_coins

    def check_collision(self, x, y):
        return (
            x <= self.robot_x + self.robot.get_width() and
            x + self.monster.get_width() >= self.robot_x and
            y + self.monster.get_height() >= self.robot_y
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.to_left = True
                if event.key == pygame.K_RIGHT:
                    self.to_right = True
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.to_left = False
                if event.key == pygame.K_RIGHT:
                    self.to_right = False

            if event.type == pygame.QUIT:
                self.running = False
        
    def move_robot(self):
        if self.to_left:
            self.robot_x -= self.robot_speed
        if self.to_right:
            self.robot_x += self.robot_speed
        self.robot_x = max(self.robot_x, 0)
        self.robot_x = min(self.robot_x, self.width - self.robot.get_width())

    def update(self):
        self.move_robot()
        self.update_monsters()
        self.update_coins()

    def draw(self):
        self.window.fill((30, 30, 30))
        self.window.blit(self.robot, (self.robot_x, self.robot_y))
        for x, y in self.monsters:
            self.window.blit(self.monster, (x, y))
        for x, y in self.coins:
            self.window.blit(self.coin, (x, y))
        score = self.game_font.render(f"Coins: {self.points}", True, (255, 0, 0))
        self.window.blit(score, (500, 0))
        pygame.display.flip()

    def main_loop(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    DodgeCoin()
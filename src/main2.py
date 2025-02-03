import pygame
import random

class Player:
    def __init__(self, x, y, size, speed, life):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.life = life

    def move(self, direction):
        if direction == "LEFT":
            self.x -= self.speed
        elif direction == "RIGHT":
            self.x += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, (self.x, self.y), self.size)


class Enemy:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed

    def shoot(self):
        return Bullet(self.x, self.y, 10, "DOWN")

    def move(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.polygon(screen, RED, [
            (self.x - self.size / 2, self.y - self.size / 2),  # Vértice izquierdo
            (self.x + self.size / 2, self.y - self.size / 2),  # Vértice derecho
            (self.x, self.y + self.size / 2)                  # Vértice de la punta
        ])

class Bullet:
    def __init__(self, x, y, speed, direction):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = 5
        self.height = 10
        self.direction = direction  # "UP" para el jugador, "DOWN" para el enemigo


    def move(self):
        if self.direction == "UP":
            self.y -= self.speed
        elif self.direction == "DOWN":
            self.y += self.speed

    def draw(self, screen):
        if self.direction == "DOWN":  # Balas enemigas
            color = YELLOW
        else:  # Balas del jugador
            color = GREEN
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

# Figuras y posiciones aleatorias // se debe mejorar en OOP
cuadros = []
for i in range(80):
    x = random.randint(1,1200)
    y =random.randint(1,600)
    c = [x,y]
    cuadros.append(c)

circulos = []
for i in range(200):
    x = random.randint(5,1195)
    y =random.randint(2,599)
    d = [x,y]
    circulos.append(d)

lineas = []
for i in range(20):
    x = random.randint(10,1190)
    y =random.randint(5,550)
    ee = [x,y]
    lineas.append(ee)


# Game initialization
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arcade Shooter")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255,255,0)

# Clase Game
class Game:
    def __init__(self):
        self.player = Player(WIDTH // 2, HEIGHT - 40, 20, 10, 3)
        self.enemies = []
        self.bullets = []
        self.score = 0
        self.level = 1
        self.max_enemies = 5
        self.enemy_bullets = []  # Lista para almacenar las balas de los enemigos
        self.game_over = False

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            screen.fill(BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Salir del Juego presionando las teclas "Q" y "ESC"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        running = False

            keys = pygame.key.get_pressed()
            if not self.game_over:
                if keys[pygame.K_LEFT] and self.player.x > self.player.speed and self.player.life > 0:
                    self.player.move("LEFT")
                if keys[pygame.K_RIGHT] and self.player.x < WIDTH - self.player.speed and self.player.life > 0:
                    self.player.move("RIGHT")
                if keys[pygame.K_SPACE] and self.player.life > 0:
                    self.bullets.append(Bullet(self.player.x, self.player.y, 20, "UP"))

            self.update_game_state()
            self.draw_game_elements(screen)

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()

    def update_game_state(self):
        if self.player.life <= 0:
            self.game_over = True

        if not self.game_over:
            # Mover y eliminar balas
            for bullet in self.bullets[:]:
                bullet.move()
                if bullet.y < 0:
                    self.bullets.remove(bullet)

            # Generar enemigos aleatoriamente
            if len(self.enemies) < self.max_enemies:
                self.enemies.append(Enemy(random.randint(0, WIDTH-30), 0, 30, 5))

            # Mover enemigos y comprobar colisiones
            for enemy in self.enemies[:]:
                enemy.move()
                if enemy.y > HEIGHT:
                    self.enemies.remove(enemy)
                for bullet in self.bullets[:]:
                    if self.check_collision(bullet, enemy):
                        self.bullets.remove(bullet)
                        self.enemies.remove(enemy)
                        self.score += 10
                        break
                if self.check_attack(enemy, self.player):
                    self.enemies.remove(enemy)
                    self.player.life -= 1

            # Hacer que los enemigos disparen
            for enemy in self.enemies:
                if random.randint(0, 100) < 5:  # Probabilidad del 5% de disparo en cada frame
                    self.enemy_bullets.append(enemy.shoot())

            # Mover y eliminar balas enemigas
            for bullet in self.enemy_bullets[:]:
                bullet.move()
                if bullet.y > HEIGHT:
                    self.enemy_bullets.remove(bullet)

            # Comprobar colisiones entre balas enemigas y jugador
            for bullet in self.enemy_bullets[:]:
                if self.check_collision(bullet, self.player):
                    self.enemy_bullets.remove(bullet)
                    self.player.life -= 1

            # Comprobar colisiones entre balas enemigas y balas del jugador
            for e_bullet in self.enemy_bullets[:]:
                for p_bullet in self.bullets[:]:
                    if self.check_collision(e_bullet, p_bullet):
                        self.enemy_bullets.remove(e_bullet)
                        self.bullets.remove(p_bullet)
                        break

            # Subir de nivel
            if self.score >= self.level * 100:
                self.level += 1
                self.max_enemies += 2
                self.score = 0
                self.player.life += 1

            # Para estrellas: Actualiza las posiciones de cuadros, círculos y líneas
            for c in cuadros:
                c[0] += 1
                c[1] += 2
                if c[0] > 1200:
                    c[0] = 0
                if c[1] > 600:
                    c[1] = 0

            for d in circulos:
                d[0] += 1
                d[1] += 2
                if d[0] > 1200:
                    d[0] = 0
                if d[1] > 600:
                    d[1] = 0

            for f in lineas:
                f[0] += 1
                f[1] += 2
                if f[0] > 1200:
                    f[0] = 0
                if f[1] > 600:
                    f[1] = 0

    def draw_game_elements(self, screen):
        # Dibujar jugador, enemigos y balas
        self.player.draw(screen)
        for bullet in self.bullets:
            bullet.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)
        
        # Dibujar balas enemigas
        for bullet in self.enemy_bullets:
            bullet.draw(screen)

        # Dibujar puntuación y nivel
        self.draw_text(screen, f'Score: {self.score}', (5, 5), 16)
        self.draw_text(screen, f'Level: {self.level}', (5, 25), 16)
        self.draw_text(screen, f'Lifes: {self.player.life}', (5, 45), 16)
        if self.game_over:
            self.draw_text(screen, f'GAME OVER', (300, 250), 48)

        # Dibujar cuadros, círculos y líneas
        for c in cuadros:
            pygame.draw.rect(screen, BLUE, (c[0], c[1], 2, 1))

        for d in circulos:
            pygame.draw.circle(screen, WHITE, (d[0], d[1]), 1)

        for f in lineas:
            pygame.draw.rect(screen, YELLOW, (f[0], f[1], 2, 2))

    def check_collision(self, bullet, enemy):
        return bullet.x in range((enemy.x-enemy.size//2), (enemy.x + enemy.size//2)) and bullet.y in range(enemy.y, enemy.y + enemy.size)
    
    def check_attack(self, enemy, player):
        return player.x in range((enemy.x-enemy.size//2-player.size), (enemy.x + enemy.size//2+player.size)) and player.y-player.size in range(enemy.y-enemy.size//2, enemy.y + enemy.size)
    
    def draw_text(self, screen, text, position, size):
        font = pygame.font.SysFont("monospace", size)
        label = font.render(text, 1, WHITE)
        screen.blit(label, position)


# Inicialización del juego
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arcade Shooter")

# Iniciar y ejecutar el juego 
game = Game()
game.run()

"""
  Concept du jeu :

    Space Invaders est un jeu d'arcade classique dans lequel le joueur contrôle un vaisseau spatial qui doit défendre
    la Terre contre une invasion extraterrestre de vaisseaux ennemis. Le joueur peut se déplacer horizontalement et verticalement pour éviter les tirs ennemis et tirer sur les vaisseaux aliens pour les détruire.

Fonctionnalités du jeu :

    Affichage d'un vaisseau spatial contrôlé par le joueur à la base de l'écran.
    Affichage d'une formation d'aliens à l'écran qui se déplacent horizontalement et descendent progressivement vers le bas.
    Le joueur peut se déplacer horizontalement pour éviter les tirs ennemis et tirer des projectiles pour détruire les aliens.
    Les aliens tirent également des projectiles vers le joueur.
    Le jeu se termine si les aliens atteignent la base du vaisseau du joueur ou si le joueur est touché par un projectile ennemi.
    Le joueur accumule des points en détruisant les aliens.
    Les niveaux deviennent de plus en plus difficiles à mesure que le joueur progresse, avec des aliens se déplaçant plus rapidement et/ou tirant plus fréquemment.

Technologies et bibliothèques :

    Utilisation de Python avec la bibliothèque Pygame pour le développement du jeu.
    Pygame fournit des fonctionnalités pour la gestion des graphismes, des événements, du son, etc., ce qui le rend adapté au développement de jeux 2D comme Space Invaders.

Architecture du code :

    Le code sera structuré en plusieurs modules pour séparer les différentes fonctionnalités du jeu, telles que le vaisseau du joueur, les aliens, les projectiles, la gestion des collisions, etc.
    Utilisation de classes et d'objets pour représenter les différents éléments du jeu et pour faciliter la gestion des interactions entre eux.
    Mise en place d'une boucle principale de jeu qui met à jour l'état du jeu à chaque frame, gère les entrées du joueur et les événements du jeu, et dessine le jeu à l'écran.

Interface utilisateur :

    Affichage d'un écran de menu principal permettant au joueur de commencer une nouvelle partie ou de quitter le jeu.
    Affichage de l'état actuel du jeu, y compris le score du joueur et le nombre de vies restantes.
    Affichage d'un écran de game over lorsque le joueur perd, avec la possibilité de recommencer ou de revenir au menu principal.
"""

import pygame
import time
import sys
import random

class Player:
    def __init__(self):
        self.vie = 3
        self.rect = pygame.Rect(500, 650, 40, 40)
        self.speed = 30
        self.projectiles = []

    def creer_player(self):
        pygame.draw.rect(screen, pygame.Color("red"), self.rect)

    def deplacer(self, touches):
        if touches[pygame.K_RIGHT]:
            self.rect.x += self.speed
            if self.rect.right > largeur:
                self.rect.right = largeur
        if touches[pygame.K_LEFT]:
            self.rect.x -= self.speed
            if self.rect.left < 0:
                self.rect.left = 0

    def shoot(self):
        projectile = pygame.Rect(self.rect.centerx - 2, self.rect.top - 10, 4, 20)  # Créer un projectile au centre du joueur
        self.projectiles.append(projectile)

    def affiche_vie(self):
        draw_text("vies :", font, pygame.Color("white"), 550, 25)
        if self.vie == 3:
            draw_text("3", font, pygame.Color("white"), 550, 60)
        pygame.display.update()
        if self.vie == 2:
            draw_text("2", font, pygame.Color("white"), 550, 60)
        pygame.display.update()
        if self.vie == 1:
            draw_text("1", font, pygame.Color("white"), 550, 60)
        pygame.display.update()

class Alien:
    def __init__(self, row_count, col_count):
        self.row_count = row_count
        self.col_count = col_count
        self.aliens = []
        self.tirs = []
        self.vie = 1
        self.rect = pygame.Rect(0, 0, 30, 30)
        self.vitesse = 10
        self.init_aliens()
        self.init_fire_info()

    def init_aliens(self): # méthode pour faire mon tableau d'aliens
        alien_width = 30
        alien_height = 30
        padding = 10
        for row in range(self.row_count):
            for col in range(self.col_count):
                alien_x = col * (alien_width + padding)
                alien_y = row * (alien_height + padding)
                self.aliens.append(pygame.Rect(alien_x, alien_y, alien_width, alien_height))

    def init_fire_info(self):
        self.fire_info = [(time.time(), random.uniform(0.5, 3)) for _ in range(len(self.aliens))]

    def creer_alien(self):
        for alien in (self.aliens):
            pygame.draw.rect(screen, pygame.Color("black"), alien)

    def shoot(self):
        current_time = time.time()
        for i, (last_fire_time, fire_delay) in enumerate(self.fire_info):
            if i < len(self.aliens):  # Vérifier si i est dans la plage valide
                if current_time - last_fire_time > fire_delay:
                    tir = pygame.Rect(self.aliens[i].centerx - 2, self.aliens[i].bottom + 10, 4, 20)
                    self.tirs.append(tir)
                    self.fire_info[i] = (current_time, random.uniform(0.5, 2))

    def deplacer(self):
        time.sleep(0.2)
        reached_edge = False  # Variable pour suivre si un alien a atteint le bord de l'écran
        for alien in self.aliens:
            alien.x += self.vitesse
            if alien.right > largeur or alien.left < 0:
                reached_edge = True

        if reached_edge:
            self.vitesse = -self.vitesse
            for alien in self.aliens:
                alien.y += 30


pygame.font.init()
ma_police = "/home/cytech/fonts/game-battles-font/GameBattlesRegular-RjXo.ttf"
titre = "/home/cytech/fonts/game-battles-font/GameBattlesRegular-RjXo.ttf"
font = pygame.font.Font(ma_police, 25)
font_2 = pygame.font.Font(ma_police, 30)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def text_title(text, font_2, color, x, y):
    text_surface = font_2.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

#def records():

obstacles_list = []  # liste pour stocker les rectangles obstacles

def obstacles():
    global obstacles_list
    obstacles_list = []  # Réinitialiser la liste des obstacles
    rect = pygame.Rect(50, 550, 50, 50)
    obstacles_list.append(rect)
    pygame.draw.rect(screen, pygame.Color("green"), rect)
    rect_1 = pygame.Rect(280, 550, 50, 50)
    obstacles_list.append(rect_1)
    pygame.draw.rect(screen, pygame.Color("green"), rect_1)
    rect_2 = pygame.Rect(500, 550, 50, 50)
    obstacles_list.append(rect_2)
    pygame.draw.rect(screen, pygame.Color("green"), rect_2)

def detect_collision(tir_rect):
    global obstacles_list
    for obstacle in obstacles_list:
        if tir_rect.colliderect(obstacle):
            obstacles_list.remove(obstacle)
            return True
    return False



def main_menu():
    while True:
        screen.fill(pygame.Color("dark blue"))
        text_title("SPACE INVADERS", font_2, pygame.Color("green"), largeur//2, hauteur//6)
        draw_text("S for START", font, pygame.Color("white"), largeur//2, hauteur//2.5)
        draw_text("Q for EXIT", font, pygame.Color("white"), largeur//2, hauteur//2)
        draw_text("R for records", font, pygame.Color("white"), largeur//2, hauteur//1.4)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    start_game()
                if event.key == pygame.K_q:
                    pygame.quit()

def game_over():
    game_over = True
    while game_over:
        screen.fill(pygame.Color("red"))
        text_title("you loose", font_2, pygame.Color("white"), largeur // 2, hauteur // 4)
        draw_text("m for menu", font, pygame.Color("white"), largeur // 2, hauteur // 2)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    game_over = False
                    main_menu()
            if event.type == pygame.QUIT:
                game_over = False
                main_menu()


clock = pygame.time.Clock()
pygame.init()

pygame.display.set_caption("Space Invader")
largeur = 600
hauteur = 800
screen = pygame.display.set_mode((largeur, hauteur))


def start_game():
    player = Player()
    alien_group = Alien(row_count=5, col_count=12)

    game_on = True

    while game_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
                if event.key == pygame.K_p:
                    main_menu()

        touches = pygame.key.get_pressed()
        player.deplacer(touches)
        player.affiche_vie()

        screen.fill(pygame.Color("dark blue"))

        player.creer_player()

        alien_group.deplacer()
        alien_group.creer_alien()
        obstacles()

        for alien in alien_group.aliens:
            if random.random() < 0.001:  # La fréquence de tir des aliens
                alien_group.shoot()

        for projectile in player.projectiles:
            pygame.draw.rect(screen, pygame.Color("red"), projectile)
            projectile.y -= 40  # Déplacer les projectiles vers le haut
            for alien in alien_group.aliens:
                if projectile.colliderect(alien):
                    player.projectiles.remove(projectile)
                    alien_group.vie -= 1
                    if alien_group.vie <= 0:
                        alien_group.aliens.remove(alien)

        # Créez une nouvelle liste pour stocker les tirs qui ne sont pas entrés en collision avec les obstacles
        new_tirs = []

        # Parcourez les tirs de manière sécurisée avec une copie de la liste
        for tir in alien_group.tirs[:]:
            pygame.draw.rect(screen, pygame.Color("white"), tir)
            tir.y += 40  # Déplacer les tirs vers le bas

            # Vérifiez la collision avec le joueur
            if tir.colliderect(player.rect):
                player.vie -= 1
                if player.vie <= 0:
                    game_over()
            else:
                # Vérifiez la collision avec les obstacles
                if not detect_collision(tir):
                    # Si pas de collision, ajoutez le tir à la nouvelle liste
                    new_tirs.append(tir)

        # Remplacez la liste originale par la nouvelle liste
        alien_group.tirs = new_tirs

        # Redessinez les obstacles après la détection de collision
        obstacles()

        pygame.display.flip()
        clock.tick(60)

main_menu()
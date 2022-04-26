# Richard Cruz
# CPSC 386-01
# 2021-12-01
# rcruz99@csu.fullerton.edu
# @rcrz10
#
# Lab 05-01
#
# Space Invader game implemented in python with pygame
#
"""Holds alien object functionality for the Space Invader game"""

from random import randrange
import os
import pygame


class Alien:
    """
    Class that runs all the functionality of the Aliens
    """

    main_dir = os.path.split(os.path.abspath(__file__))[0]
    data_dir = os.path.join(main_dir, 'data')
    image = os.path.join(main_dir, "data", 'invader.jpeg')
    impact_sound = os.path.join(data_dir, 'impact.wav')
    collide_sound = os.path.join(data_dir, 'collide.wav')

    def __init__(self, color):
        self._color = color
        try:
            alien = pygame.image.load(Alien.image).convert_alpha()
        except pygame.error:
            raise SystemExit(
                'Could not load image "%s" %s'
                % (Alien.image, pygame.get_error())
            )
        self._alien = pygame.transform.scale(alien, (60, 50))
        self._rows = [
            [
                pygame.Rect(110 + (i * 75), 50 + (j * 80), 60, 50)
                for j in range(0, 5)
            ]
            for i in range(0, 8)
        ]
        self._direction = 'RIGHT'
        self._down = False
        self._attack = []
        self._last_attack = 0
        try:
            self._impact_sound = pygame.mixer.Sound(Alien.impact_sound)
        except pygame.error:
            print('Cannot Open {}'.format(Alien.impact_sound))
            raise SystemExit(1)
        try:
            self._collide_sound = pygame.mixer.Sound(Alien.collide_sound)
        except pygame.error:
            print('Cannot Open {}'.format(Alien.collide_sound))
            raise SystemExit(1)

    def get_army(self):
        """Getter to get the list of aliens"""
        return self._rows

    def reset(self):
        """
        Function that resets the values of the
        alien object when wanting to play again
        """
        self._rows = [
            [
                pygame.Rect(110 + (i * 75), 50 + (j * 80), 60, 50)
                for j in range(0, 5)
            ]
            for i in range(0, 8)
        ]
        self._attack.clear()
        self._direction = 'RIGHT'
        self._last_attack = 0

    def draw(self, screen):
        """Draws the aliens on the screen"""
        for i in range(len(self._rows)):
            for j in range(len(self._rows[i])):
                pygame.draw.rect(screen, self._color, self._rows[i][j])
                screen.blit(self._alien, self._rows[i][j])

        for attack in self._attack:
            pygame.draw.rect(screen, (106, 255, 13), attack)

    def attack(self):
        """
        Function that creates the attacks the aliens use agains the player,
        the attacks having a random cooldown and comes from a random alien
        from the bottom row
        """
        if len(self._rows) != 0:
            j = randrange(0, len(self._rows))
            cool_down = pygame.time.get_ticks()
            if cool_down - self._last_attack >= randrange(1000, 2000):
                self._attack.append(
                    pygame.Rect(
                        self._rows[j][len(self._rows[j]) - 1].centerx - 2,
                        self._rows[j][len(self._rows[j]) - 1].centery + 15,
                        5,
                        15,
                    )
                )
                self._last_attack = pygame.time.get_ticks()

    def move_aliens(self):
        """
        Function that moves the aliens to the left right, and down
        """
        if not self._down:
            if self._direction == 'RIGHT':
                for i in range(len(self._rows)):
                    for j in range(len(self._rows[i])):
                        self._rows[i][j] = pygame.Rect.move(
                            self._rows[i][j], 1, 0
                        )
                        if self._rows[i][j].right >= 800:
                            self._direction = 'LEFT'
                            self._down = True
            elif self._direction == 'LEFT':
                for i in range(len(self._rows)):
                    for j in range(len(self._rows[i])):
                        self._rows[i][j] = pygame.Rect.move(
                            self._rows[i][j], -1, 0
                        )
                        if self._rows[i][j].left <= 0:
                            self._direction = 'RIGHT'
                            self._down = True
        else:
            for i in range(len(self._rows)):
                for j in range(len(self._rows[i])):
                    self._rows[i][j] = pygame.Rect.move(self._rows[i][j], 0, 10)
            self._down = False

    def move_attack(self, player, obstacle):
        """
        Moves the attacks of the aliens downwards towards the alien
        """
        for idx, attack in enumerate(self._attack):
            attack = pygame.Rect.move(attack, 0, 5)
            if attack.bottom <= 740:
                self._attack[idx] = attack
            else:
                self._attack.pop(idx)

            if pygame.Rect.collidelist(attack, obstacle) > -1:
                self._attack.pop(idx)

            if pygame.Rect.colliderect(attack, player.get_player()):
                self._collide_sound.play()
                self._attack.pop(idx)
                player.lives()
                self._attack.clear()
                pygame.time.delay(500)
                player.respawn()

    def update_aliens(self, player, obstacle):
        """
        Function that calls other function that are all meant
        to update the alien in some way
        """
        self.move_aliens()
        self.attack()
        self.move_attack(player, obstacle)

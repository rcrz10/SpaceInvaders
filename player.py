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
"""Player object that controls the player functionality"""

from datetime import date
import os
import pickle
import pygame


class Player:
    """
    Class that runs all the functionality of the Player
    """

    main_dir = os.path.split(os.path.abspath(__file__))[0]
    data_dir = os.path.join(main_dir, 'data')
    laser_sound = os.path.join(data_dir, 'laser.wav')
    impact_sound = os.path.join(data_dir, 'impact.wav')
    collide_sound = os.path.join(data_dir, 'collide.wav')

    def __init__(self, color):
        self._color = color
        self._xpos = 50
        self._player = pygame.Rect(self._xpos, 680, 50, 35)
        self._laser = pygame.Rect(1000, 1000, 5, 15)
        self._shot_exists = False
        self._lives = 3
        self._points = 0
        self._all_players = []
        self._player_name = ''
        self._time = 0
        self._total_time = ''
        try:
            self._laser_sound = pygame.mixer.Sound(Player.laser_sound)
        except pygame.error:
            print('Cannot Open {}'.format(Player.laser_sound))
            raise SystemExit(1)
        try:
            self._impact_sound = pygame.mixer.Sound(Player.impact_sound)
        except pygame.error:
            print('Cannot Open {}'.format(Player.impact_sound))
            raise SystemExit(1)
        try:
            self._collide_sound = pygame.mixer.Sound(Player.collide_sound)
        except pygame.error:
            print('Cannot Open {}'.format(Player.collide_sound))
            raise SystemExit(1)

    def get_player(self):
        """Getter for the player"""
        return self._player

    def get_lives(self):
        """Getter for the player lives"""
        return self._lives

    def set_name(self, name):
        """Setter for the player name"""
        self._player_name = name

    def set_time(self, time):
        """Setter for player time played"""
        self._time += time

    def get_playerscores(self):
        """Getter for the list of all player scores"""
        return self._all_players

    def convert(self):
        """Converts snake players time alive from milliseconds to seconds"""
        seconds = self._time / 1000
        self._total_time = f"{int(seconds)} s."

    def draw(self, screen):
        """Draw function to display the player and what it shoots"""
        pygame.draw.rect(screen, self._color, self._player)
        self._player = pygame.Rect(self._xpos, 680, 65, 50)
        if self._shot_exists:
            pygame.draw.rect(screen, self._color, self._laser)

    def get_points(self):
        """Getter for the player points"""
        return self._points

    def respawn(self):
        """Resets the position of the player when they lose a life"""
        self._xpos = 50
        self._shot_exists = False

    def move(self):
        """Moves the player left and right"""
        arrow = pygame.key.get_pressed()

        if arrow[pygame.K_LEFT]:
            if self._player.left >= 0:
                self._xpos = self._xpos - 4
        elif arrow[pygame.K_RIGHT]:
            if self._player.right <= 800:
                self._xpos = self._xpos + 4

    def player_collision(self, aliens):
        """Checks if the player collide with any of the aliens"""
        for idx, alien in enumerate(aliens):
            if pygame.Rect.collidelist(self._player, aliens[idx]) > -1:
                self._collide_sound.play()
                self.lives()
                pygame.time.delay(500)
                self.respawn()

    def shoot(self):
        """
        Creates the object that is used to shoot the aliens
        Unable to create another until it hits an alien or the top of the screen
        """
        if not self._shot_exists:
            self._laser_sound.play()
            pygame.time.delay(50)
            self._laser = pygame.Rect(
                self._player.centerx - 2, self._player.centery - 15, 5, 15
            )
            self._shot_exists = True

    def lives(self):
        """Reduces the amount lives by one"""
        self._lives -= 1

    def update_laser(self, aliens, obstacle):
        """
        Moves the object the player shoots, upwards towards the aliens
        Destroying the alien if hits one
        """
        self._laser = pygame.Rect.move(self._laser, 0, -5)
        if self._laser.top < -15:
            self._shot_exists = False

        for idx, alien in enumerate(aliens):
            collision = pygame.Rect.collidelist(self._laser, aliens[idx])
            if collision > -1:
                self._impact_sound.play()
                self._shot_exists = False
                aliens[idx].pop(collision)
                self._points += 10
                if len(aliens[idx]) == 0:
                    aliens.pop(idx)

        if pygame.Rect.collidelist(self._laser, obstacle) > -1:
            self._shot_exists = False

    def update_player(self, aliens, obstacle):
        """
        Function that calls other functions that are used
        to update the player in some way
        """
        self.move()
        self.player_collision(aliens)
        if self._shot_exists:
            self.update_laser(aliens, obstacle)

    def scoreboard(self):
        """
        This where the information(date, name, score and time_played) of the snake player
        is stored and appended to the all players list that will be used on
        leaderboard at the game over screen
        """
        self.convert()
        day = date.today()
        today = day.strftime("%m/%d/%Y")
        # checks if pickle file exits if not writes to it first to create
        try:
            with open('invaders_players.pickle', 'rb') as fh:
                self._all_players = pickle.load(fh)
        except (OSError, IOError) as e:
            with open('invaders_players.pickle', 'wb') as fh:
                pickle.dump(self._all_players, fh, pickle.HIGHEST_PROTOCOL)
        # appends player score to list
        self._all_players.append(
            (self._player_name, self._points, self._total_time, today)
        )
        # dumps the player scores to the pickle file
        with open('invaders_players.pickle', 'wb') as fh:
            pickle.dump(self._all_players, fh, pickle.HIGHEST_PROTOCOL)

    def reset(self):
        """Resets the player variable if the player wants to play again"""
        self._lives = 3
        self._points = 0
        self.respawn()
        self._time = 0
        self._shot_exists = False

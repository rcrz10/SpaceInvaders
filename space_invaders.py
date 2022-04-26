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
"""This is where the game loop is run for  the Space Invader Game"""

import pygame
from scene import SpaceScene
from scene import TitleScene
from scene import GameOver
from scene import WinScene
from player import Player
from alien import Alien


class InvaderGame:
    """
    Class that runs all the functionality of our Space Invader game,
    being the scenes, player, and alien objects
    """

    def __init__(self):
        self._time = 0

    def run(self):
        """Game loop for that runs the Space Invader game"""
        print('Starting Space Invaders...')
        pygame.init()
        window_size = (800, 800)
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode(window_size)
        title = 'CPSC 386-Space Invaders'
        pygame.display.set_caption(title)

        # Left the soundtrack out of the data folder since
        # I did not know how to play it without passing the name directly
        scene_list = [
            TitleScene(screen, (0, 0, 0), "SPACE INVADERS", (50, 168, 50), 50),
            SpaceScene(screen, (0, 0, 0), 'game_music.wav'),
            GameOver(screen, (0, 0, 0), "GAME OVER", (50, 168, 50), 36),
            WinScene(screen, (0, 0, 0), "YOU WIN", (50, 168, 50), 36),
        ]

        i = 0
        current_scene = scene_list[i]

        player = Player((255, 255, 255))
        alien = Alien((0, 0, 0))
        run = True
        while run:
            current_scene.draw()
            if type(current_scene) == TitleScene:
                for event in pygame.event.get():
                    current_scene.process_event(event)
                    run = current_scene.is_valid()

                current_scene.draw_text_box()
                if current_scene.get_next():
                    i += 1
                    player.set_name(current_scene.get_player_text())
                    current_scene.set_nextF()
                    current_scene = scene_list[i]

            elif type(current_scene) == SpaceScene:
                if not current_scene.get_playing():
                    current_scene.start()

                for event in pygame.event.get():
                    current_scene.process_event(event, player)
                    run = current_scene.is_valid()

                player.draw(current_scene.get_screen())
                alien.draw(current_scene.get_screen())
                current_scene.draw_obstacles()
                current_scene.display_points(player)
                current_scene.display_lives(player)

                player.update_player(
                    alien.get_army(), current_scene.get_obstacles()
                )
                alien.update_aliens(player, current_scene.get_obstacles())

                self._time = clock.get_time()
                player.set_time(self._time)

                if player.get_lives() == 0:
                    i += 1
                    current_scene.end()
                    player.scoreboard()
                    current_scene = scene_list[i]

                if (len(alien.get_army())) == 0:
                    i = len(scene_list) - 1
                    current_scene.end()
                    current_scene = scene_list[i]

            elif type(current_scene) == GameOver:
                for event in pygame.event.get():
                    current_scene.process_event(event)
                    run = current_scene.is_valid()

                current_scene.player_score(player)

                current_scene.leaderboard(player)

                if current_scene.get_play_again():
                    i -= 1
                    current_scene.reset_game(player, alien)
                    current_scene = scene_list[i]

            else:
                for event in pygame.event.get():
                    current_scene.process_event(event)
                    run = current_scene.is_valid()

                current_scene.cutscene()

                if current_scene.get_play_again():
                    i -= 2
                    current_scene.reset_game(player, alien)
                    current_scene = scene_list[i]
                elif current_scene.get_quit():
                    i -= 1
                    player.scoreboard()
                    current_scene = scene_list[i]

            pygame.display.update()
            clock.tick(current_scene.frame_rate())

        pygame.quit()
        print('Exiting')
        return 0

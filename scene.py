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
"""Holds the Scene classes that are used for the Space Invader Game"""

import pygame


class Scene:
    """Base scene class, sets up the scene of the space invaders game"""

    def __init__(self, screen, background_color, soundtrack=None):
        self._screen = screen
        self._background = pygame.Surface(self._screen.get_size())
        self._background.fill(background_color)
        self._frame_rate = 60
        self._is_valid = True
        self._soundtrack = soundtrack
        self._playing = False

    def draw(self):
        """Base draw function for scenes"""
        self._screen.blit(self._background, (0, 0))

    def process_event(self, event):
        """Base function to process game events"""
        if event.type == pygame.QUIT:
            self._is_valid = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._is_valid = False

    def is_valid(self):
        """Getter to check is scene screen is valid"""
        return self._is_valid

    def get_screen(self):
        """Getter for scene screen"""
        return self._screen

    def get_playing(self):
        """Getter to check if music is playing"""
        return self._playing

    def start(self):
        """Starts game soundtrack"""
        if self._soundtrack:
            try:
                pygame.mixer.music.load(self._soundtrack)
            except pygame.error:
                print('Cannot open the mixer?')
                raise SystemExit('broken!!')
            pygame.mixer.music.play(-1)
            self._playing = True

    def end(self):
        """Stops game soundtrack"""
        if self._soundtrack:
            pygame.mixer.music.stop()
            self._playing = False

    def frame_rate(self):
        """Returns game frame rate"""
        return self._frame_rate


class TitleScene(Scene):
    """Title Screen scene that inherits from scene class"""

    def __init__(
        self, screen, background_color, title, title_color, title_size
    ):
        super().__init__(screen, background_color)
        self._title_size = title_size
        title_font = pygame.font.Font(
            pygame.font.get_default_font(), title_size
        )
        self._title = title_font.render(title, True, title_color)
        (w, h) = self._screen.get_size()
        self._title_pos = self._title.get_rect(center=(w / 2, 360))
        self._input_name = pygame.Rect(455, 460, 67, 30)
        self._player_text = ''
        self._next = False

    def get_player_text(self):
        """Getter for title scene input text"""
        return self._player_text

    def set_player_text(self, text):
        """Setter for title scene input text"""
        self._player_text = text

    def set_nextF(self):
        """Setter for the next variable"""
        self._next = False

    def get_next(self):
        """Getter for next variable"""
        return self._next

    def draw(self):
        """Draws title scene on screen"""
        super().draw()
        self._screen.blit(self._title, self._title_pos)

        text = pygame.font.Font(pygame.font.get_default_font(), 30)
        name = text.render("Enter Name:", True, (50, 168, 50))
        name_pos = name.get_rect(topleft=(265, 460))
        self._screen.blit(name, name_pos)

        text = pygame.font.Font(pygame.font.get_default_font(), 20)
        name = text.render(
            "Press the enter key to play. Must enter a 3 letter name to play",
            True,
            (50, 168, 50),
        )
        name_pos = name.get_rect(center=(400, 550))
        self._screen.blit(name, name_pos)

        name = text.render(
            "Move player with the left and rigth arrow keys. Shoot with spacebar",
            True,
            (50, 168, 50),
        )
        name_pos = name.get_rect(center=(400, 520))
        self._screen.blit(name, name_pos)

        name = text.render(
            "Press any alphabet key to enter name", True, (50, 168, 50)
        )
        name_pos = name.get_rect(center=(400, 580))
        self._screen.blit(name, name_pos)

        name = text.render(
            "Press backspace to delete a character in your name",
            True,
            (50, 168, 50),
        )
        name_pos = name.get_rect(center=(400, 600))
        self._screen.blit(name, name_pos)

        name = text.render(
            "Press Esc to quit game at any point", True, (50, 168, 50)
        )
        name_pos = name.get_rect(center=(400, 680))
        self._screen.blit(name, name_pos)

    def process_event(self, event):
        """Process events during title scene screen"""
        super().process_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self._player_text = self._player_text[:-1]
            else:
                if len(self._player_text) < 3 and event.unicode.isalpha():
                    self._player_text += event.unicode.upper()

            if event.key == pygame.K_RETURN:
                if len(self._player_text) == 3:
                    self._next = True

    def draw_text_box(self):
        """draws text box for player name to be inputted"""
        pygame.draw.rect(self._screen, (50, 168, 50), self._input_name, 2)
        text = pygame.font.Font(pygame.font.get_default_font(), 32)
        input_surface = text.render(self._player_text, True, (50, 168, 50))
        self._screen.blit(
            input_surface, (self._input_name.x + 5, self._input_name.y + 2)
        )

        self._input_name.w = input_surface.get_width() + 10


class SpaceScene(Scene):
    """Spaces scene that will display the invader game"""

    def __init__(self, screen, background_color, soundtrack):
        super().__init__(screen, background_color, soundtrack)
        self._obstacles = []
        for i in range(2):
            self._obstacles.append(pygame.Rect(210 + (i * 300), 550, 100, 75))

    def get_obstacles(self):
        return self._obstacles

    def draw(self):
        """Draws game over scene on the screen"""
        super().draw()
        pygame.draw.line(
            self._background, (50, 168, 50), (0, 740), (1000, 740), 3
        )

    def draw_obstacles(self):
        """Draws game obtacles onto the screen"""
        for blocks in self._obstacles:
            pygame.draw.rect(self._screen, (58, 66, 69), blocks)

    def display_points(self, player):
        """Displays players points on the bottom right of the space scene"""
        font = pygame.font.SysFont(pygame.font.get_default_font(), 50)
        points = font.render(
            f"Score: {player.get_points()}", True, (50, 168, 50)
        )
        points_pos = points.get_rect(topleft=(580, 750))
        self._screen.blit(points, points_pos)

    def display_lives(self, player):
        """Displays players lives on the bottom left of the space scene"""
        font = pygame.font.SysFont(pygame.font.get_default_font(), 50)
        lives = font.render(
            f"Lives left: {player.get_lives()}", True, (50, 168, 50)
        )
        life_pos = lives.get_rect(topleft=(100, 750))
        self._screen.blit(lives, life_pos)

    def process_event(self, event, player):
        """Process events of the space scene, such as when to shoot"""
        super().process_event(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.shoot()


class GameOver(Scene):
    """Game over class that displays game over screen, inhertis from scene class"""

    def __init__(
        self, screen, background_color, loss_text, text_color, text_size
    ):
        super().__init__(screen, background_color)
        self._text_size = text_size
        game_over_font = pygame.font.Font(
            pygame.font.get_default_font(), text_size
        )
        self._game_over = game_over_font.render(loss_text, True, text_color)
        self._game_over_pos = self._game_over.get_rect(center=(400, 20))

        self._play_again = False

    def get_play_again(self):
        """Getter to check play_again"""
        return self._play_again

    def draw(self):
        """Draws game over scene on the screen"""
        super().draw()
        self._screen.blit(self._game_over, self._game_over_pos)
        text = pygame.font.Font(pygame.font.get_default_font(), 20)
        name = text.render(
            "Press Enter to play again or Esc to quit", True, (50, 168, 50)
        )
        name_pos = name.get_rect(center=(400, 720))
        self._screen.blit(name, name_pos)

    def process_event(self, event):
        """Process events of the game over scene, such as checking to play again"""
        super().process_event(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self._play_again = True

    def player_score(self, player):
        """Displays player score on the gameover screen"""
        score = pygame.font.Font(pygame.font.get_default_font(), 36)
        player_score = score.render(
            f"Your Score: {player.get_points()}", True, (50, 168, 50)
        )
        score_pos = player_score.get_rect(center=(400, 60))
        self._screen.blit(player_score, score_pos)

    def leaderboard(self, player):
        """Displays space invader game leaderboard on the gameoverscene"""
        board = pygame.font.Font(pygame.font.get_default_font(), 36)
        leaderboard = board.render("High Scores", True, (50, 168, 50))
        board_pos = leaderboard.get_rect(center=(400, 120))
        self._screen.blit(leaderboard, board_pos)

        for i in range(170, 670, 50):
            pygame.draw.line(self._screen, (50, 168, 50), (100, i), (700, i), 3)

        board = pygame.font.Font(pygame.font.get_default_font(), 25)
        leaderboard = board.render("Name", True, (50, 168, 50))
        board_pos = leaderboard.get_rect(center=(180, 157))
        self._screen.blit(leaderboard, board_pos)

        leaderboard = board.render("Score", True, (50, 168, 50))
        board_pos = leaderboard.get_rect(center=(325, 157))
        self._screen.blit(leaderboard, board_pos)

        leaderboard = board.render("Time Played", True, (50, 168, 50))
        board_pos = leaderboard.get_rect(center=(500, 157))
        self._screen.blit(leaderboard, board_pos)

        leaderboard = board.render("Date", True, (50, 168, 50))
        board_pos = leaderboard.get_rect(center=(630, 157))
        self._screen.blit(leaderboard, board_pos)

        for i in range(1, 11):
            leaderboard = board.render(f"{i}.", True, (50, 168, 50))
            board_pos = leaderboard.get_rect(center=(125, 157 + (i * 50)))
            self._screen.blit(leaderboard, board_pos)

        highscores = player.get_playerscores()

        size = len(highscores)
        if size > 1:
            highscores.sort(key=lambda tup: tup[1], reverse=True)
            if size > 10:
                for k in range(size, 10, -1):
                    highscores.pop()

        j = 1
        for tup in highscores:
            leaderboard = board.render(f"{tup[0]}", True, (50, 168, 50))
            board_pos = leaderboard.get_rect(center=(180, 157 + (j * 50)))
            self._screen.blit(leaderboard, board_pos)

            leaderboard = board.render(f"{tup[1]}", True, (50, 168, 50))
            board_pos = leaderboard.get_rect(center=(325, 157 + (j * 50)))
            self._screen.blit(leaderboard, board_pos)

            leaderboard = board.render(f"{tup[2]}", True, (50, 168, 50))
            board_pos = leaderboard.get_rect(center=(500, 157 + (j * 50)))
            self._screen.blit(leaderboard, board_pos)

            leaderboard = board.render(f"{tup[3]}", True, (50, 168, 50))
            board_pos = leaderboard.get_rect(center=(630, 157 + (j * 50)))
            self._screen.blit(leaderboard, board_pos)
            j += 1

    def reset_game(self, player, alien):
        """Start a new game after the player has lost"""
        player.reset()
        alien.reset()
        self._play_again = False


class WinScene(Scene):
    """Scene that is displayed when the player takes out all the aliens"""

    def __init__(
        self, screen, background_color, loss_text, text_color, text_size
    ):
        super().__init__(screen, background_color)
        self._text_size = text_size
        game_over_font = pygame.font.Font(
            pygame.font.get_default_font(), text_size
        )
        self._win = game_over_font.render(loss_text, True, text_color)
        self._winner_pos = self._win.get_rect(center=(400, 800))

        self._congrats = game_over_font.render('CONGRATS', True, text_color)
        self._congrats_pos = self._win.get_rect(center=(378, -20))

        self._play_again = False
        self._quit = False

    def get_play_again(self):
        """Getter to check if player wants to play again"""
        return self._play_again

    def get_quit(self):
        """Getter to check if player wants to quit"""
        return self._quit

    def draw(self):
        """Draws the win screen scene on the screen"""
        super().draw()
        self._screen.blit(self._congrats, self._congrats_pos)
        self._screen.blit(self._win, self._winner_pos)
        if self._congrats_pos.top > 395:
            text = pygame.font.Font(pygame.font.get_default_font(), 20)
            name = text.render(
                "Press Enter to play next level or Q to end",
                True,
                (50, 168, 50),
            )
            name_pos = name.get_rect(center=(400, 500))
            self._screen.blit(name, name_pos)

    def cutscene(self):
        """Function to move text across screen"""
        if self._congrats_pos.top < 395:
            self._congrats_pos = pygame.Rect.move(self._congrats_pos, 0, 7)
        if self._winner_pos.top > 440:
            self._winner_pos = pygame.Rect.move(self._winner_pos, 0, -5)

    def reset_game(self, player, alien):
        """Start a new game after the player has won"""
        alien.reset()
        player.respawn()
        self._play_again = False
        self._quit = False

    def process_event(self, event):
        """Process events of the win scene, such as play again or quitting"""
        super().process_event(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self._play_again = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            self._quit = True

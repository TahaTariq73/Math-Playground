import pygame
from pygame import mixer

pygame.init()
mixer.init()

class GameEngine():

    def __init__(self):
        self.font = pygame.font.SysFont("comicsansms", 30)
        self.clock = pygame.time.Clock()
        self.fps = 30

        self.white = (245, 245, 245)
        self.black = (0, 0, 0)

        self.exit_game = False
        self.game_over = False

    def game_window(self):
        """ Creating window with title """
        self.window = pygame.display.set_mode((740, 460))
        icon = pygame.image.load("Images/icon.ico")
        pygame.display.set_caption("Catch Catch Game")
        pygame.display.set_icon(icon)
        pygame.display.update()

    def game_txt(self, txt, color, x, y):
        """ Adding text where needed """
        text = self.font.render(txt, True, color)
        self.window.blit(text, [x, y])

    def machine_breaker(self, machinePositionY, no):
        """ Machine will automatically break when it collabs with the border """
        if machinePositionY < 10 or machinePositionY > 330:
            if no == 1 :
                self.machine1_velocity_y = 0
            else:
                self.machine2_velocity_y = 0

    def machine_reflector(self, machine_position_x, ball_position_x, machine_position_y, ball_position_y, value):
        """ Reflecting ball when it touches the machine """
        if abs(machine_position_x - ball_position_x) < 15 and abs((machine_position_y + 60) - ball_position_y) < 60:
            self.ball_velocity_x = value
            self.ball_velocity_y = ((machine_position_y + 60) - ball_position_y) / 5
            mixer.music.load("Audios/lichess_move.mp3")
            mixer.music.play()

    def border_reflector(self, ball_position_y):
        """ Reflecting ball when it collab with the roof or ground """
        if ball_position_y < 10:
            self.ball_velocity_y = 10
        elif ball_position_y > 450:
            self.ball_velocity_y = -10

    def placeImg(self, path):
        img = pygame.image.load(path)
        return pygame.transform.scale(img, (740, 460)).convert_alpha()

    def welcomeScreen(self):
        """ Welcoming the user """
        self.game_over = False
        self.exit_game = False

        while not self.exit_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_engine.gameloop()

            self.window.blit(self.placeImg("Images/homepage.jpg"), (0, 0))
            pygame.display.update()

    def gameloop(self):
        # MACHINE VARIABLES - All values are checked and they are perfect for this default window size
        # Machine 1! means player 1
        machine1_position_x = 20
        machine1_position_y = (430 / 2) - 60
        self.machine1_velocity_y = 0

        # Machine 2! means player 1
        machine2_position_x = 700
        machine2_position_y = (430 / 2) - 60
        self.machine2_velocity_y = 0

        machine_size_y = 120
        machine_size_x = 20
        machine_borders = [8, 8, 8, 8]

        # BALL VARIABLES - All values are checked and they are perfect for this default window size
        ball_position_x = 740 / 2
        ball_position_y = 430 / 2
        ball_size = 20
        self.ball_velocity_x = 10
        self.ball_velocity_y = 0

        self.winner = None
        while not self.exit_game:
            if self.game_over:
                self.game_txt(f"{self.winner} win's! Press enter to play again", self.white, (740 / 3) - 120, (460 / 2) - 30)
                pygame.display.update() # Showing the gameOver text

                # Handling events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.exit_game = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.welcomeScreen()
            else:
                # Handling events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.exit_game = True

                    if event.type == pygame.KEYDOWN:
                        # Player 1 controls
                        if event.key == pygame.K_w:
                            self.machine1_velocity_y = -10

                        elif event.key == pygame.K_s:
                            self.machine1_velocity_y = 10

                        elif event.key == pygame.K_a:
                            self.machine1_velocity_y = 0

                        # Player 2 controls
                        if event.key == pygame.K_UP:
                            self.machine2_velocity_y = -10

                        elif event.key == pygame.K_DOWN:
                            self.machine2_velocity_y = 10

                        elif event.key == pygame.K_LEFT:
                            self.machine2_velocity_y = 0

                machine1_position_y += self.machine1_velocity_y
                machine2_position_y += self.machine2_velocity_y
                ball_position_x += self.ball_velocity_x
                ball_position_y += self.ball_velocity_y

                # Calling game functions
                self.machine_breaker(machine1_position_y, 1)
                self.machine_breaker(machine2_position_y, 2)
                self.machine_reflector(machine1_position_x, ball_position_x, machine1_position_y, ball_position_y, 10)
                self.machine_reflector(machine2_position_x, ball_position_x, machine2_position_y, ball_position_y, -10)
                self.border_reflector(ball_position_y)

                # Updating screen
                self.window.fill(self.black)
                self.window.blit(self.placeImg("Images/playing_background.jpg"), (0, 0))
                pygame.draw.circle(self.window, self.white, [ball_position_x, ball_position_y], 10)
                pygame.draw.rect(self.window, self.white, [machine1_position_x, machine1_position_y, machine_size_x, machine_size_y], 10, *machine_borders)
                pygame.draw.rect(self.window, self.white, [machine2_position_x, machine2_position_y, machine_size_x, machine_size_y], 10, *machine_borders)

                # GameOvering when the ball touch with the left/right border without touching the machine
                if ball_position_x > 720:
                    self.ball_velocity_x = 0
                    self.winner = "Left"
                    mixer.music.load("Audios/duck2.mp3")
                    mixer.music.play()
                    self.game_over = True

                elif ball_position_x < 20:
                    self.ball_velocity_x = 0
                    self.winner = "Right"
                    mixer.music.load("Audios/duck2.mp3")
                    mixer.music.play()
                    self.game_over = True

                pygame.display.update()
                self.clock.tick(self.fps)

if __name__ == '__main__':
    game_engine = GameEngine()
    game_engine.game_window()
    game_engine.welcomeScreen()
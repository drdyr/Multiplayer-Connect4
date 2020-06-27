import pygame
from network import Network
from connect4game import Game, Disk, Slot, EntrySlot
import pickle

pygame.init()


white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
blue = (50, 50, 255)
grey = (150, 150, 150)
black = (0, 0, 0)
green = (0, 255, 0)

screen = pygame.display.set_mode((700, 720))
screen.fill(blue)
bottom_text_panel = (0, 620, 700, 100)


def draw_screen(screen, game):
    screen.fill(blue)
    if not game.isReady():
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255, 0, 0), True)
        screen.blit(text, (700 / 2 - text.get_width() / 2, 720 / 2 - text.get_height() / 2))
    else:
        game.draw(screen)

    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        draw_screen(screen, game)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for entry_slot in game.entry_slots:
                    if entry_slot.is_cursor() and Disk(entry_slot.x, 0, red) not in game.disks and not game.won and (game.turn - player) % 2 == 0:
                        n.send(str(entry_slot.x))


main()
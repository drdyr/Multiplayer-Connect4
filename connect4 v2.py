import pygame
import sys

pygame.init()
clock = pygame.time.Clock()


class Board:
    def __init__(self):
        self.slots = []
        self.entry_slots = []
        self.disks = []
        for i in range(7):
            self.entry_slots.append(EntrySlot(i))
            for j in range(6):
                self.slots.append(Slot(i, j))
        self.won = False

    def add_disk(self, disk):
        disk.update()
        self.disks.append(disk)
        if self.check_win(disk):
            self.won = True


    def draw(self):
        for slot in self.slots:
            slot.draw()
        for entry_slot in self.entry_slots:
            entry_slot.draw()
        for disk in self.disks:
            disk.draw()

    def check_win(self, disk):
        colour = disk.colour
        next_disk = disk
        directions = [(0, 1), (1, 1), (1, 0), (1, -1)]
        for direction in directions:
            count = 0
            while next_disk.colour == colour:
                candidate = Disk(next_disk.x + direction[0], next_disk.y + direction[1], next_disk.colour)
                if candidate in self.disks:
                    next_disk = self.disks[self.disks.index(candidate)]
                    if next_disk.colour == colour:
                        count += 1
                else:
                    break
            next_disk = disk
            while next_disk.colour == colour:
                candidate = Disk(next_disk.x + (direction[0] * -1), next_disk.y + (direction[1] * -1), next_disk.colour)
                if candidate in self.disks:
                    next_disk = self.disks[self.disks.index(candidate)]
                    if next_disk.colour == colour:
                        count += 1
                else:
                    break
            if count >= 3:
                return True

        return False


class Slot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.colour = white
        self.rect = (100 * self.x + 15, 100 * self.y + 15, 70, 70)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def draw(self):
        self.rect = (100 * self.x + 15, 100 * self.y + 35, 70, 70)
        pygame.draw.ellipse(screen, self.colour, self.rect)


class EntrySlot:
    def __init__(self, x):
        self.x = x
        self.rect = (100 * self.x, 0, 100, 20)
        self.colour = black

    def draw(self):
        if self.is_cursor():
            self.colour = green
        else:
            self.colour = black
        pygame.draw.rect(screen, self.colour, self.rect)

    def is_cursor(self):
        return self.x * 100 < pygame.mouse.get_pos()[0] < (self.x + 1) * 100 and 0 < pygame.mouse.get_pos()[1] < 20


class Disk:
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.colour = colour
        self.rect = (100 * self.x + 15, 100 * self.y + 15, 70, 70)

    def draw(self):
        self.rect = (100 * self.x + 15, 100 * self.y + 35, 70, 70)
        pygame.draw.ellipse(screen, self.colour, self.rect)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def update(self):
        while self.y < 5 and Disk(self.x, self.y + 1, red) not in board.disks:
            self.y += 1

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

turn = 1

board = Board()
font = pygame.font.SysFont('Comic Sans', 50)
display_red_turn = font.render("It is red's turn.", False, black)
display_yellow_turn = font.render("It is yellow's turn.", False, black)
display_red_won = font.render("Player red won!", False, black)
display_yellow_won = font.render("Player yellow won!", False, black)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for entry_slot in board.entry_slots:
                if entry_slot.is_cursor() and Disk(entry_slot.x, 0, red) not in board.disks and not board.won:
                    if turn % 2 == 1:
                        board.add_disk(Disk(entry_slot.x, 0, red))
                        turn += 1
                    else:
                        board.add_disk(Disk(entry_slot.x, 0, yellow))
                        turn += 1

    board.draw()
    pygame.draw.rect(screen, grey, bottom_text_panel)
    if not board.won:
        if turn % 2 == 1:
            screen.blit(display_red_turn, (50, 650))
        else:
            screen.blit(display_yellow_turn, (50, 650))
    else:
        if turn % 2 == 0:
            screen.blit(display_red_won, (50, 650))
        else:
            screen.blit(display_yellow_won, (50, 650))
    pygame.display.flip()
    clock.tick(60)

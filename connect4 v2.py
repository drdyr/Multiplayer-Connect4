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

    def add_disk(self, disk):
        disk.update()
        self.disks.append(disk)
        # if self.check_win(disk):
        #      pygame.quit()
        #      sys.exit()

    def draw(self):
        for slot in self.slots:
            slot.draw()
        for entry_slot in self.entry_slots:
            entry_slot.draw()
        for disk in self.disks:
            disk.draw()

    # def get_neighbours(self, disk):
    #     neighbours = []
    #     for i in range(-1, 2):
    #         for j in range(-1, 2):
    #             if Disk(disk.x + i, disk.y + j, red) in self.disks and (i != 0 and j != 0):
    #                 neighbour = self.disks[self.disks.index(Disk(disk.x + i, disk.y + j, red))]
    #                 if neighbour.colour == disk.colour:
    #                     neighbours.append(self.disks[self.disks.index(Disk(disk.x + i, disk.y + j, red))])
    #     return neighbours
    #
    # def check_win(self, disk):
    #     for neighbour in self.get_neighbours(disk):
    #         if self.diverge(neighbour, neighbour.x - disk.x, neighbour.y - disk.y, 1):
    #             return True
    #     return False
    #
    # def diverge(self, disk, dir1, dir2, count):
    #     if count > 4:
    #         return True
    #     else:
    #         check_disk = Disk(disk.x + dir1, disk.y + dir2, red)
    #         if check_disk in self.disks and self.disks[self.disks.index(check_disk)].colour == disk.colour:
    #             self.diverge(check_disk, dir1, dir2, count + 1)


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

screen = pygame.display.set_mode((700, 620))
screen.fill(blue)

turn = 1

board = Board()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for entry_slot in board.entry_slots:
                if entry_slot.is_cursor() and Disk(entry_slot.x, 0, red) not in board.disks:
                    if turn % 2 == 1:
                        board.add_disk(Disk(entry_slot.x, 0, red))
                        turn += 1
                    else:
                        board.add_disk(Disk(entry_slot.x, 0, yellow))
                        turn += 1
    board.draw()
    pygame.display.flip()
    clock.tick(60)

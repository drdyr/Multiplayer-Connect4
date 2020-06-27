import pygame

class Game:
    def __init__(self, id):
        self.p1Turn = True
        self.p2Turn = False
        self.ready = False
        self.id = id
        self.slots = []
        self.entry_slots = []
        self.disks = []
        for i in range(7):
            self.entry_slots.append(EntrySlot(i))
            for j in range(6):
                self.slots.append(Slot(i, j))
        self.won = False

    def isReady(self):
        return self.ready

    def add_disk(self, disk):
        disk.update()
        self.disks.append(disk)
        if self.check_win(disk):
            self.won = True

    def draw(self, screen):
        for slot in self.slots:
            slot.draw(screen)
        for entry_slot in self.entry_slots:
            entry_slot.draw(screen)
        for disk in self.disks:
            disk.draw(screen)

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

    def draw(self, screen):
        self.rect = (100 * self.x + 15, 100 * self.y + 35, 70, 70)
        pygame.draw.ellipse(screen, self.colour, self.rect)


class EntrySlot:
    def __init__(self, x):
        self.x = x
        self.rect = (100 * self.x, 0, 100, 20)
        self.colour = black

    def draw(self, screen):
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

    def draw(self, screen):
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
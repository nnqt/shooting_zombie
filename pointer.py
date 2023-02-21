import pygame

class pointer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10,10))
        self.image.fill('blue')
        self.rect = self.image.get_rect(center = (300,300))
        self.mask = pygame.mask.from_surface(self.image)

    def show(self,window):
        r = 0
        l = 10
        color = (255, 0,0)
        pos = pygame.mouse.get_pos()

        self.image.blit(self.image, pos)

        # pygame.draw.ellipse(window, color, (pos[0] - r/2, pos[1] - r/2, r, r), 4)
        pygame.draw.line(window, color, (pos[0], pos[1] - l/2), (pos[0], pos[1] - l), 4)
        pygame.draw.line(window, color, (pos[0] + l/2, pos[1]), (pos[0] + l, pos[1]), 4)
        pygame.draw.line(window, color, (pos[0], pos[1] + l/2), (pos[0], pos[1] + l), 4)
        pygame.draw.line(window, color, (pos[0] - l/2, pos[1]), (pos[0] - l, pos[1]), 4)

    def update(self):
        if pygame.mouse.get_pos():
            self.rect.center = pygame.mouse.get_pos()

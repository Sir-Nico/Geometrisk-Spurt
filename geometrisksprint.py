import math
import pygame
import sys


GAME_SPEED = 5


class Player:
    def __init__(self, texture):
        self.pos = pygame.Vector2((100, 330))
        self.speed = 0
        self.texture = texture
        self.rotated_texture = texture
        self.rect = pygame.Rect((self.pos.x, self.pos.y, 50, 50))
        self.rotated_rect = self.rect
        self.is_jumping = False
        self.is_rotating = False
        self.angle = 0
        self.rotation = 0

    def draw(self, screen):
        if self.texture:
            screen.blit(self.rotated_texture, self.rotated_rect)
        else:
            pygame.draw.rect(screen, "crimson", self.rect)

    def update(self):
        self.pos.y -= self.speed
        self.speed -= 1
        self.rect = pygame.Rect((self.pos.x, self.pos.y, 50, 50))
        if self.is_rotating:
            self.rotate(180/25)
        if catch_platform(self):
            self.speed = 0
            self.is_jumping = False
            self.is_rotating = False
            self.angle = snap_angle(self.angle)
    
    def jump(self):
        if self.is_jumping is False:
            self.speed = 12
            self.is_jumping = True
            self.is_rotating = True
        
    def rotate(self, angle):
        self.angle -= angle
        self.angle %= 360
        self.rotated_texture = pygame.transform.rotate(self.texture, self.angle)
        self.rotated_rect = self.rotated_texture.get_rect(center=self.rect.center)


class Block:
    def __init__(self, y_index, displacement):
        self.pos = pygame.Vector2(1000 - displacement, 330 - 50 * y_index)
        self.tilepos = pygame.Vector2(self.pos.x // 50, y_index)
        self.speed = GAME_SPEED
        self.rect = pygame.Rect(self.pos.x, self.pos.y, 50, 50)

    def update(self):
        self.pos.x -= self.speed
        self.rect = pygame.Rect(self.pos.x, self.pos.y, 50, 50)
        self.tilepos.x -= ((self.tilepos.x * 50) - self.pos.x) // 50 
    
    def draw(self, screen):
        pygame.draw.rect(screen, "red", self.rect)


def catch_platform(player, *rectlist):

    if rectlist:
        if pygame.Rect.collidelist(player.rect, rectlist):
            return True

    if player.pos.y >= 330:
        return True


def snap_angle(angle):
    multiple = angle / 90
    multiple = round(multiple)
    return multiple * 90


def render_platatataform(screen, platatataform, platform_x):
    screen.blit(platatataform, (platform_x, 379))
    screen.blit(platatataform, (platform_x + 986, 379))
    platform_x -= GAME_SPEED
    if platform_x <= -986:
        platform_x = 0
    return platform_x


# Main Function
def main():
    # Pygame Setup
    pygame.init()
    screen_w, screen_h = 640, 480
    screen = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption("Geometrisk Spurt")
    clock = pygame.time.Clock()

    platform_x = 0
    current_grid_displacement = 0

    DIE = pygame.USEREVENT
    RESET = pygame.USEREVENT + 1
    JUMP = pygame.USEREVENT + 2
    SPAWN_BLOCK = pygame.USEREVENT + 3

    stereo_backdrop = pygame.image.load("Assets\\MicrosoftTeams-image.png")
    platatataform = pygame.image.load("Assets\\platatataform.png")
    dawgvo = pygame.transform.smoothscale(pygame.image.load("Assets\\uten navn.png"), (50, 50))

    player = Player(dawgvo)

    blocks = []
    has_spawned_block_this_frame = False

    # Clears board and starts loop
    pygame.event.post(pygame.event.Event(RESET))
    running = True

    while running:
        # Main event loop
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == RESET:
                print("reset")
            if event.type == JUMP:
                player.jump()
            if event.type == SPAWN_BLOCK and has_spawned_block_this_frame is False:
                block = Block(0, current_grid_displacement)
                tilepos_list = [block.tilepos.x for block in blocks]
                if block.tilepos.x not in tilepos_list:
                    blocks.append(block)
                    has_spawned_block_this_frame = True
                    print("block spawned")
                    print([block.tilepos.x for block in blocks])
                else:
                    del block
            
        has_spawned_block_this_frame = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if player.is_jumping is False:
                pygame.event.post(pygame.event.Event(JUMP))
        if keys[pygame.K_b]:
            pygame.event.post(pygame.event.Event(SPAWN_BLOCK))
        
        # Purging block list
        blocks = [block for block in blocks if block.pos.x >= -100]

        current_grid_displacement += 5
        current_grid_displacement %= 50

        rectlist = [block.rect for block in blocks]
        catch_platform(player, rectlist)

        for block in blocks:
            block.update()
        player.update()

        # Rendering Code
        try:
            screen.fill("#282828")
            screen.blit(stereo_backdrop, (0,0))
            platform_x = render_platatataform(screen, platatataform, platform_x)

            for block in blocks:
                block.draw(screen)
            player.draw(screen)

            pygame.display.flip()
        
        except Exception as e:
            print(e)

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
    sys.exit()
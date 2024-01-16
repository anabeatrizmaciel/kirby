import pygame
import sys

pygame.init()

largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Kirby Animation')
branco = (255, 255, 255)

class Kirby(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        spritesheet_original = pygame.image.load('assets/kirby_spritesheet.png')
        self.spritesheet = spritesheet_original
        self.frames_por_acao = {
            'parado': [0],
            'andando': list(range(1, 8)),
            'pulando': list(range(9, 10)),
            'correndo': list(range(11, 15))
        }
        self.acao_atual = 'parado'
        self.frame_atual = 0
        self.frame_rect = pygame.Rect(0, 0, self.spritesheet.get_width() // 17, self.spritesheet.get_height())
        self.rect = self.frame_rect.copy()
        self.iniciar_posicao()
        self.velocidade_base = 5
        self.velocidade = self.velocidade_base
        self.pulo = False
        self.altura_pulo = 10

    def iniciar_posicao(self):
        self.rect.midbottom = (largura // 2, altura)

    def update(self):
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
            self.acao_atual = 'andando'
        elif teclas[pygame.K_RIGHT]:
            if teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT]:
                self.velocidade = min(self.velocidade + 1, self.velocidade_base * 3)
                self.acao_atual = 'correndo'
            else:
                self.velocidade = min(self.velocidade_base * (teclas[pygame.K_RIGHT] + 1), self.velocidade_base * 2)
                self.acao_atual = 'andando'
            self.velocidade = min(self.velocidade, self.velocidade_base * 3)
            self.rect.x += self.velocidade
        else:
            self.velocidade = self.velocidade_base
            self.acao_atual = 'parado'

        if not self.pulo:
            self.rect.y += 5

        if teclas[pygame.K_UP]:
            if not self.pulo:
                self.pulo = True
                self.acao_atual = 'pulando'
                self.altura_pulo = 10

        if self.pulo:
            if self.rect.y > altura // 2:
                self.rect.y -= self.altura_pulo
                self.altura_pulo -= 1
            else:
                self.pulo = False
                self.altura_pulo = 10
                self.acao_atual = 'parado'

        self.atualizar_frame()

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > largura:
            self.rect.right = largura
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > altura:
            self.rect.bottom = altura

    def atualizar_frame(self):
        frames = self.frames_por_acao[self.acao_atual]
        self.frame_atual = (self.frame_atual + 1) % len(frames)
        self.frame_rect.x = frames[self.frame_atual] * self.frame_rect.width

todos_sprites = pygame.sprite.Group()
kirby = Kirby()
todos_sprites.add(kirby)

kirby.iniciar_posicao()

clock = pygame.time.Clock()
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    todos_sprites.update()
    tela.fill(branco)
    tela.blit(kirby.spritesheet, kirby.rect, area=kirby.frame_rect)
    pygame.display.flip()
    clock.tick(10)

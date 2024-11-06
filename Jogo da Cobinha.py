import pygame
import random

# Configurações da janela
pygame.init()
pygame.display.set_caption("Jogo Snake")
largura, altura = 900, 600
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

# Cores RGB
preto = (0, 0, 0)
branco = (248, 248, 255)
amarelo = (255, 215, 0)
verde = (0, 128, 0)
verde_escuro = (0, 255, 0)
vermelho = (255, 0, 0)
cinza = (169, 169, 169)

# Parâmetros da cobra e do jogo
tamanho_quadrado = 10
velocidade_jogo = 10

def gerar_maca():
    return (round(random.randrange(0, largura - tamanho_quadrado) / 10.0) * 10.0,
            round(random.randrange(0, altura - tamanho_quadrado) / 10.0) * 10.0)

def desenhar_maca(tamanho, maca_x, maca_y):
    pygame.draw.circle(tela, vermelho, (maca_x + tamanho // 2, maca_y + tamanho // 2), tamanho // 2)

def desenhar_cobra(tamanho, pixels):
    head_x, head_y = pixels[-1]
    pygame.draw.rect(tela, verde_escuro, [head_x, head_y, tamanho, tamanho])
    for pixel in pixels[:-1]:
        pygame.draw.rect(tela, verde_escuro, [pixel[0], pixel[1], tamanho, tamanho])

def desenhar_obstaculos(obstaculos):
    for obstaculo in obstaculos:
        pygame.draw.rect(tela, cinza, [obstaculo[0], obstaculo[1], tamanho_quadrado, tamanho_quadrado])

def desenhar_pontuacao(pontuacao):
    fonte = pygame.font.SysFont("helvetica", 20, bold=True)
    texto = fonte.render(f"Pontos: {pontuacao}", True, amarelo)
    tela.blit(texto, [10, 5])

def rodar_jogo():
    global velocidade_x, velocidade_y, velocidade_jogo
    fim_jogo = False
    x, y = largura / 2, altura / 2
    velocidade_x, velocidade_y = 0, 0
    tamanho_cobra, contagem_macas = 1, 0
    pixels = []
    maca_x, maca_y = gerar_maca()

    obstaculos = [gerar_maca() for _ in range(10)]

    while not fim_jogo:
        tela.fill(verde)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_jogo = True
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and velocidade_x == 0:
                    velocidade_x, velocidade_y = -tamanho_quadrado, 0
                elif evento.key == pygame.K_RIGHT and velocidade_x == 0:
                    velocidade_x, velocidade_y = tamanho_quadrado, 0
                elif evento.key == pygame.K_UP and velocidade_y == 0:
                    velocidade_x, velocidade_y = 0, -tamanho_quadrado
                elif evento.key == pygame.K_DOWN and velocidade_y == 0:
                    velocidade_x, velocidade_y = 0, tamanho_quadrado

        x += velocidade_x
        y += velocidade_y

        if x >= largura or x < 0 or y >= altura or y < 0:
            fim_jogo = True

        desenhar_maca(tamanho_quadrado, maca_x, maca_y)
        desenhar_obstaculos(obstaculos)

        pixels.append([x, y])
        if len(pixels) > tamanho_cobra:
            del pixels[0]

        if [x, y] in pixels[:-1]:
            fim_jogo = True

        desenhar_cobra(tamanho_quadrado, pixels)
        desenhar_pontuacao(tamanho_cobra - 1)

        for obstaculo in obstaculos:
            if x == obstaculo[0] and y == obstaculo[1]:
                fim_jogo = True

        if x == maca_x and y == maca_y:
            maca_x, maca_y = gerar_maca()
            tamanho_cobra += 1
            contagem_macas += 1
            velocidade_jogo += 0.25
            if contagem_macas % 5 == 0:
                obstaculos.append(gerar_maca())

        pygame.display.update()
        relogio.tick(velocidade_jogo)

# Rodar o jogo
rodar_jogo()

# Fechar o Pygame
pygame.quit()
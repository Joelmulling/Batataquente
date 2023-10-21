import pygame
import random
import math
from pythonds.basic.queue import Queue

def calculate_player_positions(num_players, radius, center):
    player_positions = []
    for i in range(num_players):
        angle = (2 * math.pi * i) / num_players
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        player_positions.append((x, y))
    return player_positions

def hotPotato(namelist, num):
    pygame.init()
    largura = 1024
    altura = 768
    screen = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Batata Quente")

    branco = (255, 255, 255)
    font = pygame.font.Font(None, 25)

    eliminados = []

    clock = pygame.time.Clock()

    raio = 200  # Raio inicial do círculo
    centro_x = largura // 2
    centro_y = altura // 2

    jogador_posicoes = calculate_player_positions(len(namelist), raio, (centro_x, centro_y))

    # Mapeamento entre nomes dos jogadores e círculos correspondentes
    jogador_circulo = {name: (x, y) for name, (x, y) in zip(namelist, jogador_posicoes)}

    simqueue = Queue()
    for name in namelist:
        simqueue.enqueue(name)

    while len(eliminados) < len(namelist) - 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return  # Encerra a função, mas mantém a janela aberta

        screen.fill(branco)

        for i in range(num):
            simqueue.enqueue(simqueue.dequeue())

        eliminado = simqueue.dequeue()
        eliminados.append(eliminado)

        raio -= 20  # Reduz o raio a cada eliminação

        jogador_posicoes = calculate_player_positions(len(namelist) - len(eliminados), raio, (centro_x, centro_y))

        for i, (x, y) in enumerate(jogador_posicoes):
            pygame.draw.circle(screen, (128, 128, 128), (int(x), int(y)), 50)
            text = font.render(namelist[i], True, (0, 0, 0))
            text_rect = text.get_rect(center=(x, y))
            screen.blit(text, text_rect)

        text = font.render(f"Eliminados : {eliminados}", True, (0, 0, 0))
        screen.blit(text, (largura // 2 - 500, altura // 2 - 350))
        text = font.render(f"Jogadores : {namelist}", True, (0, 255, 128))
        screen.blit(text, (largura // 2 - 500, altura // 2 - 370))
        pygame.display.update()

        pygame.time.delay(2000)  # Tempo para mostrar quem foi eliminado

        clock.tick(2)  # Ajuste a taxa de atualização

    vencedor = simqueue.dequeue()
    print(f"Vencedor: {vencedor}")

    while True:  # Loop para manter a janela aberta
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

# Lista de nomes dos jogadores
nomes = ["Joel", "Gui", "Paulo", "Lucas", "Samuel", "Tiago", "Gabriel", "Miguel", "Túlio", "Leonardo"]

# Número de vezes para passar a batata quente
numero = random.randint(5, 15)

hotPotato(nomes, numero)

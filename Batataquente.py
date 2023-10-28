import pygame
import random
import math
import sys

LARGURA = 1024
ALTURA = 768
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)

def get_number_players(screen):
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 48)  # Fonte para o título
    input_box_width = 200
    input_box_height = 50
    input_box_x = (LARGURA - input_box_width) // 2  # Centralizando na largura
    input_box_y = (ALTURA - input_box_height) // 2  # Centralizando na altura
    input_box = pygame.Rect(input_box_x, input_box_y, input_box_width, input_box_height)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    text = ''
    active = False

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        try:
                            num_players = int(text)
                            if 1 < num_players <= 10:
                                return num_players
                            else:
                                text = 'O número precisa ser maior que 1 e menor que 0.'
                        except ValueError:
                            text = 'Você não digitou um número.'
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(BRANCO)
        title_text = title_font.render("Digite a quantidade de jogadores:", True, (0, 0, 0))
        screen.blit(title_text, ((LARGURA - title_text.get_width()) // 2, (ALTURA - title_text.get_height()) // 2 - 50))  # Centralizando o título na tela
        pygame.draw.rect(screen, color, input_box, 2)
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, ((LARGURA - width) // 2 + 5, (ALTURA - input_box_height) // 2 + 5))

        pygame.display.flip()
        clock.tick(30)


def get_player_names(num_players):
    pygame.init()
    screen = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Players - Batata Quente")
    font = pygame.font.Font(None, 36)
    label_font = pygame.font.Font(None, 24)  # Fonte para os rótulos
    title_font = pygame.font.Font(None, 48)  # Fonte para o título
    input_boxes = [pygame.Rect((LARGURA - 200) // 2, 150 + i * 50, 200, 32) for i in range(num_players)]
    labels = [label_font.render(f"Jogador {i+1}:", True, (0, 0, 0)) for i in range(num_players)]
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    texts = [''] * num_players
    active_input_box = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return texts
                if event.key == pygame.K_TAB:
                    active_input_box = (active_input_box + 1) % num_players
                if event.key == pygame.K_BACKSPACE:
                    texts[active_input_box] = texts[active_input_box][:-1]
                else:
                    texts[active_input_box] += event.unicode

        screen.fill(BRANCO)
        title_text = title_font.render("Digite o nome dos jogadores:", True, (0, 0, 0))
        screen.blit(title_text, ((LARGURA - title_text.get_width()) // 2, 50))  # Centralizando o título na tela
        for i, box in enumerate(input_boxes):
            if i == active_input_box:
                color = color_active
            else:
                color = color_inactive
            pygame.draw.rect(screen, color, box, 2)
            txt_surface = font.render(texts[i], True, color)
            width = max(200, txt_surface.get_width()+10)
            box.w = width
            screen.blit(txt_surface, ((LARGURA - width) // 2 + 5, box.y + 5))  # Centralizando o texto na caixa
            # Desenhando rótulo (label) à esquerda da entrada
            screen.blit(labels[i], ((LARGURA - width) // 2 - labels[i].get_width() - 10, box.y))

        pygame.display.flip()



def calculate_player_positions(num_players, radius, center):
    player_positions = []
    for i in range(num_players):
        angle = (2 * math.pi * i) / num_players
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        player_positions.append((x, y))
    return player_positions

def hotPotato(num_players, num):
    pygame.init()
    screen = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Batata Quente")

    font = pygame.font.Font(None, 25)

    eliminados = []

    clock = pygame.time.Clock()

    raio = 200  # Raio inicial do círculo
    centro_x = LARGURA // 2
    centro_y = ALTURA // 2

    namelist = get_player_names(num_players)

    jogador_posicoes = calculate_player_positions(len(namelist), raio, (centro_x, centro_y))

    # Mapeamento entre nomes dos jogadores e círculos correspondentes
    jogador_circulo = {name: (x, y) for name, (x, y) in zip(namelist, jogador_posicoes)}

    simqueue = namelist.copy()

    while len(eliminados) < len(namelist) - 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return  # Encerra a função, mas mantém a janela aberta

        screen.fill(BRANCO)

        for i in range(num):
            simqueue.insert(0, simqueue.pop())

        eliminado = simqueue.pop()
        eliminados.append(eliminado)

        raio -= 10  # Reduz o raio a cada eliminação

        jogador_posicoes = calculate_player_positions(len(namelist) - len(eliminados), raio, (centro_x, centro_y))

        for i, (x, y) in enumerate(jogador_posicoes):
            pygame.draw.circle(screen, (128, 128, 128), (int(x), int(y)), 50)
            text = font.render(simqueue[i], True, (0, 0, 0))
            text_rect = text.get_rect(center=(x, y))
            screen.blit(text, text_rect)

        text = font.render(f"Eliminados : {eliminados}", True, (0, 0, 0))
        screen.blit(text, (LARGURA // 2 - 500, ALTURA // 2 - 350))
        text = font.render(f"Jogadores : {namelist}", True, (0, 255, 128))
        screen.blit(text, (LARGURA // 2 - 500, ALTURA // 2 - 370))
        pygame.display.update()

        pygame.time.delay(2000)  # Tempo para mostrar quem foi eliminado

        clock.tick(2)  # Ajuste a taxa de atualização

    vencedor = simqueue.pop()
    print(f"Vencedor: {vencedor}")

    while True:  # Loop para manter a janela aberta
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return


def menu_batata_quente():
    pygame.init()
    screen = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Menu - Batata Quente")
    title_font = pygame.font.Font(None, 48)  # Fonte para o título
    font = pygame.font.Font(None, 36)

    botao_jogar = pygame.Rect(400, 400, 200, 50)
    botao_sair = pygame.Rect(400, 500, 200, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if botao_jogar.collidepoint(pos):
                    num_players = get_number_players(screen)
                    if num_players is not None:
                        numero = random.randint(5, 15)
                        hotPotato(num_players, numero)
                elif botao_sair.collidepoint(pos):
                    pygame.quit()
                    sys.exit()

        screen.fill(BRANCO)
        title_text = title_font.render("Menu - Batata Quente", True, (0, 0, 0))
        screen.blit(title_text, ((LARGURA - title_text.get_width()) // 2, 100))  # Centralizando o título na tela

        # Centralizando os botões e textos dos botões
        botao_jogar.center = (LARGURA // 2, ALTURA // 2)
        botao_sair.center = (LARGURA // 2, ALTURA // 2 + 100)

        pygame.draw.rect(screen, (0, 255, 0), botao_jogar)
        pygame.draw.rect(screen, (255, 0, 0), botao_sair)

        texto_jogar = font.render("Jogar", True, (0, 0, 0))
        texto_sair = font.render("Sair", True, (0, 0, 0))

        screen.blit(texto_jogar, texto_jogar.get_rect(center=botao_jogar.center))
        screen.blit(texto_sair, texto_sair.get_rect(center=botao_sair.center))

        pygame.display.flip()

menu_batata_quente()



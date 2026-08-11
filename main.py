import pygame
import random


def selecionar_dificuldade(tela, cores):
    fonte = pygame.font.Font(None, 40)

    caixa_facil = pygame.Rect(150, 200, 200, 60)
    caixa_dificil = pygame.Rect(150, 300, 200, 60)

    pygame.draw.rect(tela, cores['branca'], caixa_facil)
    pygame.draw.rect(tela, cores['branca'], caixa_dificil)

    texto_facil = fonte.render("Facil", True, cores['preto'])
    texto_dificil = fonte.render("Dificil", True, cores['preto'])

    tela.blit(texto_facil, texto_facil.get_rect(center=caixa_facil.center))
    tela.blit(texto_dificil, texto_dificil.get_rect(center=caixa_dificil.center))

    return caixa_facil, caixa_dificil


def main():
    # Tela
    pygame.init()
    largura = 500
    altura = 600
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Caça ao tesouro')
    estado = 'menu'

    som_tesouro = pygame.mixer.Sound("pygame_tesouro.wav")
    som_buraco = pygame.mixer.Sound("pygame_buraco.wav")
    som_contagem = pygame.mixer.Sound("pygame_contagem.wav")

    msc_menu = pygame.mixer.Sound("musica_menu.wav")
    msc_vitoria = pygame.mixer.Sound("musica_vitoria.wav")
    msc_jogo = pygame.mixer.Sound("musica_jogo.wav")
    msc_jogo.set_volume(0.2)

    msc_menu.play()

    img_dificuldade = pygame.transform.scale(pygame.image.load('dificuldade.png'), (500, 600))
    img_tesouro = pygame.transform.scale(pygame.image.load("tesouro.png"), (46, 46))
    img_buraco = pygame.transform.scale(pygame.image.load("buraco.png"), (46, 46))
    img_menu = pygame.transform.scale(pygame.image.load('menu.png'), (500, 650))
    img_vitoria = pygame.transform.scale(pygame.image.load('vitoria.png'), (500, 600))
    img_empate = pygame.transform.scale(pygame.image.load('empate.png'), (500, 600))

    cores = {
        'branca': (255, 255, 255),
        'azul': (0, 0, 255),
        'vermelho': (255, 0, 0),
        'preto': (0, 0, 0),
        'marrom': (101, 67, 33),
        'areia': (194, 178, 128),
    }

    fonte1 = pygame.font.Font(None, 40)
    fonte2 = pygame.font.Font(None, 30)
    fonte3 = pygame.font.Font(None, 20)

    lado_quadrado = 50

    config_facil = {'linhas': 4, 'colunas': 4, 'tesouros': 6, 'buracos': 3, 'diagonais': False}
    config_dificil = {'linhas': 8, 'colunas': 8, 'tesouros': 15, 'buracos': 10, 'diagonais': True}

    running = True
    while running:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE and estado == 'menu':
                    running = False
                    print('fechou')

                if evento.key == pygame.K_RETURN and estado == 'menu':
                    estado = 'dificuldade'

                if evento.key == pygame.K_RETURN and estado == 'vitoria':
                    estado = 'menu'
                    msc_vitoria.stop()
                    msc_menu.play(-1)
                    print('menu')
                if evento.key == pygame.K_ESCAPE and estado == 'vitoria':
                    running = False
                    print('fechou')
                if evento.key == pygame.K_ESCAPE and estado == 'jogando':
                    running = False
                    print('fechou')

            if evento.type == pygame.MOUSEBUTTONDOWN and estado == 'dificuldade':
                if caixa_facil.collidepoint(evento.pos):
                    config = config_facil
                elif caixa_dificil.collidepoint(evento.pos):
                    config = config_dificil
                else:
                    continue

                if config ==  config_facil:
                    largura, altura = 200, 250
                    fonte_placar = fonte3
                    espaco_placar = 16
                else:
                    largura, altura = 400, 500
                    fonte_placar = fonte1
                    espaco_placar = 30
                tela = pygame.display.set_mode((largura,altura))

                linhas = config['linhas']
                colunas = config['colunas']
                tesouros = config['tesouros']
                buracos = config['buracos']
                diagonais = config['diagonais']

                pontuacao = [0, 0]
                msc_menu.stop()
                msc_jogo.play()

                tamanho_grade_x = lado_quadrado * colunas
                tamanho_grade_y = lado_quadrado * linhas

                tabuleiro = []
                for i in range(linhas):
                    tabuleiro.append([0] * colunas)

                contador = 0
                while contador < tesouros:
                    linha = random.randint(0, linhas - 1)
                    coluna = random.randint(0, colunas - 1)
                    if tabuleiro[linha][coluna] == 0:
                        tabuleiro[linha][coluna] = -1
                        contador += 1

                contador = 0
                while contador < buracos:
                    linha = random.randint(0, linhas - 1)
                    coluna = random.randint(0, colunas - 1)
                    if tabuleiro[linha][coluna] == 0:
                        tabuleiro[linha][coluna] = -2
                        contador += 1

                revelado = []
                for i in range(linhas):
                    revelado.append([0] * colunas)

                for i in range(linhas):
                    for j in range(colunas):
                        if tabuleiro[i][j] == 0:
                            contar_tesouros = 0
                            if i - 1 >= 0 and tabuleiro[i - 1][j] == -1:
                                contar_tesouros += 1
                            if i + 1 < linhas and tabuleiro[i + 1][j] == -1:
                                contar_tesouros += 1
                            if j - 1 >= 0 and tabuleiro[i][j - 1] == -1:
                                contar_tesouros += 1
                            if j + 1 < colunas and tabuleiro[i][j + 1] == -1:
                                contar_tesouros += 1

                            if diagonais:
                                if i - 1 >= 0 and j - 1 >= 0 and tabuleiro[i - 1][j - 1] == -1:
                                    contar_tesouros += 1
                                if i - 1 >= 0 and j + 1 < colunas and tabuleiro[i - 1][j + 1] == -1:
                                    contar_tesouros += 1
                                if i + 1 < linhas and j - 1 >= 0 and tabuleiro[i + 1][j - 1] == -1:
                                    contar_tesouros += 1
                                if i + 1 < linhas and j + 1 < colunas and tabuleiro[i + 1][j + 1] == -1:
                                    contar_tesouros += 1

                            tabuleiro[i][j] = contar_tesouros

                vez = random.randint(1, 2)
                print(f"Quem começa é o Jogador {vez}")

                estado = 'jogando'

            elif evento.type == pygame.MOUSEBUTTONDOWN and estado == 'jogando':
                x, y = evento.pos
                coluna = x // 50
                linha = y // 50
                if linha < 0 or linha >= linhas or coluna < 0 or coluna >= colunas:
                    continue
                if revelado[linha][coluna] != 0:
                    continue

                if tabuleiro[linha][coluna] == -1:
                    print(f'Jogador {vez} achou um tesouro!')
                    revelado[linha][coluna] = 1
                    som_tesouro.play()
                    if vez == 1:
                        pontuacao[0] += 100
                        vez = 2
                    else:
                        pontuacao[1] += 100
                        vez = 1

                elif tabuleiro[linha][coluna] == -2:
                    print(f'Jogador {vez} caiu em um buraco!')
                    revelado[linha][coluna] = 2
                    som_buraco.play()
                    if vez == 1:
                        pontuacao[0] -= 50
                        if pontuacao[0] < 0:
                            pontuacao[0] = 0
                        vez = 2
                    else:
                        pontuacao[1] -= 50
                        if pontuacao[1] < 0:
                            pontuacao[1] = 0
                        vez = 1
                else:
                    print(f'Jogador {vez} não encontrou nada.')
                    print(f'Tem {tabuleiro[linha][coluna]} ao redor!')
                    revelado[linha][coluna] = 3
                    som_contagem.play()
                    if vez == 1:
                        vez = 2
                    elif vez == 2:
                        vez = 1

        if estado == 'dificuldade':
            tela.blit(img_dificuldade, (0, 0))
            caixa_facil, caixa_dificil = selecionar_dificuldade(tela, cores)

        if estado == 'vitoria':
            if vencedor == 'Jogador 1':
                texto_vitoria1 = fonte1.render('O vencedor da partida foi:', False, cores['branca'])
                texto_vitoria2 = fonte1.render(f'{vencedor}', False, cores['azul'])
                tela.blit(img_vitoria, (0, 0))
                tela.blit(texto_vitoria1, (60, 20))
                tela.blit(texto_vitoria2, (170, 150))

            elif vencedor == 'Jogador 2':
                texto_vitoria1 = fonte1.render('O vencedor da partida foi:', False, cores['branca'])
                texto_vitoria2 = fonte1.render(f'{vencedor}', False, cores['vermelho'])
                tela.blit(img_vitoria, (0, 0))
                tela.blit(texto_vitoria1, (60, 20))
                tela.blit(texto_vitoria2, (170, 150))

            elif vencedor == 'Empate':
                texto_vitoria1 = fonte1.render('Houve um EMPATE', False, cores['branca'])
                tela.blit(img_empate, (0, 0))
                tela.blit(texto_vitoria1, (42, 20))

            texto_retorno = fonte1.render('ENTER para retornar ao menu', False, cores['branca'])
            tela.blit(texto_retorno, (60, 445))
            texto_fecha = fonte1.render('Aperte ESC para sair do jogo', False, cores['branca'])
            tela.blit(texto_fecha, (60, 485))

        if estado == 'menu':
            tela.fill(cores['preto'])
            texto_menu1 = fonte1.render('Aperte ENTER para jogar', False, cores['branca'])
            texto_menu2 = fonte1.render('Aperte ESC para sair', False, cores['branca'])
            tela.blit(img_menu, (0, 0))
            tela.blit(texto_menu1, (70, 325))
            tela.blit(texto_menu2, (95, 375))

        if estado == 'jogando':
            tela.fill(cores['areia'])
            pos_y = 0
            for i in range(linhas + 1):
                pygame.draw.line(tela, cores['marrom'], (0, pos_y), (tamanho_grade_x, pos_y), 3)
                pos_y += lado_quadrado

            pos_x = 0
            for j in range(colunas + 1):
                pygame.draw.line(tela, cores['marrom'], (pos_x, 0), (pos_x, tamanho_grade_y), 3)
                pos_x += lado_quadrado
            
            barra_y = tamanho_grade_y
            texto_jogador_1 = fonte_placar.render(f'Jogador 1 - Pontuação:{pontuacao[0]}', False, cores['azul'])
            texto_jogador_2 = fonte_placar.render(f'Jogador 2 - Pontuação:{pontuacao[1]}', False, cores['vermelho'])
            texto_vez = fonte_placar.render(f'Vez:{vez}', False, cores['preto'])

            tela.blit(texto_vez, (5, barra_y + 2))
            tela.blit(texto_jogador_1, (5, barra_y + 2 + espaco_placar))
            tela.blit(texto_jogador_2, (5, barra_y + 2 + espaco_placar * 2))

            for i in range(linhas):
                for j in range(colunas):
                    if revelado[i][j] == 1:
                        tela.blit(img_tesouro, (j * 50, i * 50))
                    elif revelado[i][j] == 2:
                        tela.blit(img_buraco, (j * 50, i * 50))
                    elif revelado[i][j] == 3:
                        texto_numeros = fonte1.render(str(tabuleiro[i][j]), True, cores['preto'])
                        tela.blit(texto_numeros, (j * 50 + 20, i * 50 + 20))

            acabou = True
            for i in range(linhas):
                for j in range(colunas):
                    if revelado[i][j] == 0:
                        acabou = False

            if acabou:
                if pontuacao[0] > pontuacao[1]:
                    vencedor = 'Jogador 1'
                elif pontuacao[1] > pontuacao[0]:
                    vencedor = 'Jogador 2'
                else:
                    vencedor = 'Empate'
                largura, altura = 500, 600
                tela = pygame.display.set_mode((largura,altura))

                estado = 'vitoria'
                msc_jogo.stop()
                msc_vitoria.play()

        pygame.display.update()


if __name__ == '__main__':
    main()
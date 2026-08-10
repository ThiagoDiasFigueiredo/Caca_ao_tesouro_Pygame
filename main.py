import pygame
import random

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

    img_tesouro = pygame.transform.scale(pygame.image.load("tesouro.png"), (46, 46))
    img_buraco = pygame.transform.scale(pygame.image.load("buraco1.png"), (46, 46))
    img_menu = pygame.transform.scale(pygame.image.load('menu.png'),(500,650))
    img_vitoria = pygame.transform.scale(pygame.image.load('vitoria.png'),(500,600))
    img_empate = pygame.transform.scale(pygame.image.load('empate.png'),(500,600))

    cores = {
        'branca': (255, 255, 255),
        'azul': (0, 0, 255),
        'vermelho': (255, 0, 0),
        'preto': (0, 0, 0),
        'marrom': (101,67,33),
        'areia': (194,178,128),
    }

    fonte1 = pygame.font.Font(None, 40)
    fonte2 = pygame.font.Font(None, 30)
    lado_quadrado = 50
    num_linhas = 11
    tamanho_grade = lado_quadrado * (num_linhas - 1)  # 200

    linhas = 10
    colunas = 10

    # Looping do jogo
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
                    pontuacao = [0,0]

                    tela.fill(cores['areia'])

                    pos_y = 0
                    for i in range(num_linhas):
                        pygame.draw.line(tela, cores['marrom'], (0, pos_y), (tamanho_grade, pos_y),3)
                        pos_y += lado_quadrado

                    pos_x = 0
                    for j in range(num_linhas):
                        pygame.draw.line(tela, cores['marrom'], (pos_x, 0), (pos_x, tamanho_grade), 3)
                        pos_x += lado_quadrado

                    tabuleiro = []
                    for i in range(linhas):
                        linha = []
                        for j in range(colunas):
                            linha.append(0)
                        tabuleiro.append(linha)

                    tesouros = 12
                    buracos = 8
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

                    for linha_tab in tabuleiro:
                        print(linha_tab)
                    
                    revelado = []
                    for i in range(linhas):
                        revelado.append([0] * colunas)

                    for i in range(linhas):
                        for j in range(colunas):
                            if tabuleiro[i][j] == 0:
                                contar_tesouros = 0
                                if i - 1 >= 0:
                                    if tabuleiro[i - 1][j] == -1:
                                        contar_tesouros += 1
                                if i + 1 < linhas:
                                    if tabuleiro[i + 1][j] == -1:
                                        contar_tesouros += 1
                                if j - 1 >= 0:
                                    if tabuleiro[i][j - 1] == -1:
                                        contar_tesouros += 1
                                if j + 1 < colunas:
                                    if tabuleiro[i][j + 1] == -1:
                                        contar_tesouros += 1
                                if i - 1 >= 0 and j - 1 >= 0:
                                    if tabuleiro[i - 1][j - 1] == -1:
                                        contar_tesouros += 1
                                if i - 1 >= 0 and j + 1 < colunas:
                                    if tabuleiro[i - 1][j + 1] == -1:
                                        contar_tesouros += 1
                                if i + 1 < linhas and j - 1 >= 0:
                                    if tabuleiro [i + 1][j - 1] == -1:
                                        contar_tesouros += 1
                                if i + 1 < linhas and j + 1 < colunas:
                                    if tabuleiro [i + 1][j + 1] == -1:
                                        contar_tesouros += 1

                                tabuleiro[i][j] = contar_tesouros

                    vez = random.randint(1,2)
                    print(f"Quem começa é o Jogador {vez}")

                    estado = 'jogando'

                # Controles na tela de vitória
                if evento.key == pygame.K_RETURN and estado == 'vitoria':
                    estado = 'menu'
                    print('menu')
                if evento.key == pygame.K_ESCAPE and estado == 'vitoria':
                    running = False
                    print('fechou')

            if evento.type == pygame.MOUSEBUTTONDOWN and estado == 'jogando':
                x, y = evento.pos
                coluna = x // 50
                linha = y // 50
                if y >= 500:
                    continue
                if revelado[linha][coluna] != 0:
                    continue

                if tabuleiro[linha][coluna] == -1: # Tesouro
                    print(f'Jogador {vez} achou um tesouro!')
                    revelado[linha][coluna] = 1
                    som_tesouro.play()
                    if vez == 1:
                        pontuacao[0] += 100
                        vez = 2
                    else:
                        pontuacao[1] += 100
                        vez = 1

                elif tabuleiro[linha][coluna] == -2: # Buraco
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

        # RENDERIZAÇÃO
        if estado == 'vitoria':
            if vencedor == 'Jogador 1':
                texto_vitoria1 = fonte1.render('O vencedor da partida foi:', False, cores['branca'])
                texto_vitoria2 = fonte1.render(f'{vencedor}', False, cores['azul'])
                tela.blit(img_vitoria,(0,0))
                tela.blit(texto_vitoria1, (60, 20)) 
                tela.blit(texto_vitoria2, (170, 150))
                
            elif vencedor == 'Jogador 2':
                texto_vitoria1 = fonte1.render('O vencedor da partida foi:', False, cores['branca'])
                texto_vitoria2 = fonte1.render(f'{vencedor}', False, cores['vermelho'])
                tela.blit(img_vitoria,(0,0))
                tela.blit(texto_vitoria1, (60, 20)) 
                tela.blit(texto_vitoria2, (170, 150))
                
            elif vencedor == 'Empate':
                texto_vitoria1 = fonte1.render('Houve um EMPATE', False, cores['branca'])
                tela.blit(img_empate,(0,0))
                tela.blit(texto_vitoria1, (42, 20))
                
            texto_retorno = fonte1.render('ENTER para retornar ao menu', False, cores['branca'])
            tela.blit(texto_retorno, (60, 445))
            texto_fecha = fonte1.render('Aperte ESC para sair do jogo', False, cores['branca'])
            tela.blit(texto_fecha, (60, 485))

        if estado == 'menu':
            tela.fill(cores['preto'])
            texto_menu1 = fonte1.render('Aperte ENTER para jogar', False, cores['branca'])
            texto_menu2 = fonte1.render('Aperte ESC para sair', False, cores['branca'])
            tela.blit(img_menu, (0,0))
            tela.blit(texto_menu1,(70,325))
            tela.blit(texto_menu2,(95,375))

        if estado == 'jogando':
            pygame.draw.rect(tela, cores['areia'], (0, 505, largura, altura - 505))
            texto_jogador_1 = fonte2.render(f'Jogador 1 - Pontuação:{pontuacao[0]}', False, cores['azul'])
            texto_jogador_2 = fonte2.render(f'Jogador 2 - Pontuação:{pontuacao[1]}', False, cores['vermelho'])
            texto_vez = fonte2.render(f'Vez:{vez}', False, cores['preto'])
            tela.blit(texto_vez, (20, 510))
            tela.blit(texto_jogador_1, (20, 540))
            tela.blit(texto_jogador_2, (20, 570))

            for i in range(linhas):
                for j in range(colunas):
                    if revelado[i][j] == 1:
                        tela.blit(img_tesouro, (j * 50 + 2, i * 50 + 2))
                    elif revelado[i][j] == 2:
                        tela.blit(img_buraco, (j * 50 + 2, i * 50 + 2))
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
                estado = 'vitoria'

        pygame.display.update()

if __name__ == '__main__':
    main()
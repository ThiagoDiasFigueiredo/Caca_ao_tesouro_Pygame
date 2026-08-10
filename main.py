def main():
    import pygame
    import random
    
    pygame.init()
    pygame.mixer.init()
    largura = 200
    altura = 250
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Caça ao tesouro')
    estado = 'menu'

    som_tesouro = pygame.mixer.Sound("pygame_tesouro.wav")
    som_buraco = pygame.mixer.Sound("pygame_buraco.wav")
    som_contagem = pygame.mixer.Sound("pygame_contagem.wav")
    img_tesouro = pygame.transform.scale(pygame.image.load("tesouro.png"), (49, 49))
    img_buraco = pygame.transform.scale(pygame.image.load("buraco.png"), (49, 49))
    img_menu = pygame.transform.scale(pygame.image.load('menu.png'),(200,250))
    img_vitoria = pygame.transform.scale(pygame.image.load('vitoria.png'),(200,250))
    img_empate = pygame.transform.scale(pygame.image.load('empate.png'),(200,250))
    
    msc_menu = pygame.mixer.Sound("musica_menu.wav")
    msc_vitoria = pygame.mixer.Sound("musica_vitoria.wav")
    msc_jogo = pygame.mixer.Sound("musica_jogo.wav")
    msc_jogo.set_volume(0.2)
    
    msc_menu.play()    
    
    cores = {
        'branca': (255, 255, 255),
        'azul': (0, 0, 255),
        'vermelho': (255, 0, 0),
        'preto': (0, 0, 0),
        'verde': (0, 255, 0),
        'areia': (194,178,128),
        'marrom': (101,67,33),
    }

    fonte = pygame.font.Font(None,20)
    lado_quadrado = 50
    num_linhas = 5
    tamanho_grade = lado_quadrado * (num_linhas -1)

    linhas = 4
    colunas = 4
    
    running = True
    while running:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and estado == 'menu':
                    pontuacao = [0,0]
                    msc_menu.stop()
                    msc_jogo.play()

                    tela.fill(cores['areia'])

                    pos_y = 0
                    for i in range(num_linhas):
                        pygame.draw.line(tela, cores['marrom'], (0, pos_y), (tamanho_grade, pos_y),2)
                        pos_y += lado_quadrado

                    pos_x = 0
                    for j in range(num_linhas):
                        pygame.draw.line(tela, cores['marrom'], (pos_x, 0), (pos_x, tamanho_grade), 2)
                        pos_x += lado_quadrado

                    tabuleiro = []
                    for i in range(linhas):
                        tabuleiro.append([0]*colunas)

                    tesouros = 6
                    buracos = 3
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
                                tabuleiro[i][j] = contar_tesouros

                    vez = random.randint(1,2)
                    print(f"Quem começa é o Jogador {vez}")

                    estado = 'jogando'

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

            if evento.type == pygame.MOUSEBUTTONDOWN and estado == 'jogando':
                x, y = evento.pos
                coluna = x // 50
                linha = y // 50
                if y >= 200:
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

        
        if estado == 'vitoria':
            if vencedor == 'Jogador 1':
                texto_vitoria1 = fonte.render('O vencedor da partida foi:', False, cores['branca'])
                texto_vitoria2 = fonte.render(f'{vencedor}', False, cores['azul'])
                tela.blit(img_vitoria,(0,0))
                tela.blit(texto_vitoria1, (15, 10)) 
                tela.blit(texto_vitoria2, (65, 50))
                
            elif vencedor == 'Jogador 2':
                texto_vitoria1 = fonte.render('O vencedor da partida foi:', False, cores['branca'])
                texto_vitoria2 = fonte.render(f'{vencedor}', False, cores['vermelho'])
                tela.blit(img_vitoria,(0,0) )
                tela.blit(texto_vitoria1, (15, 10)) 
                tela.blit(texto_vitoria2, (65, 50))
                
            elif vencedor == 'Empate':
                texto_vitoria1 = fonte.render('Houve um EMPATE', False, cores['branca'])
                tela.blit(img_empate,(0,0))
                tela.blit(texto_vitoria1, (42, 20))
                
            texto_retorno = fonte.render('ENTER para retornar ao menu', False, cores['branca'])
            
            tela.blit(texto_retorno, (5, 190))
            texto_fecha = fonte.render('Aperte ESC para sair do jogo', False, cores['branca'])
            tela.blit(texto_fecha, (10, 230))

        if estado == 'menu':
            texto_menu = fonte.render('Aperte Enter para jogar', False, cores['branca'])
            tela.blit(img_menu, (0,0))
            tela.blit(texto_menu,(20,170))
        if estado == 'jogando':
            pygame.draw.rect(tela, cores['branca'], (0, 201, 201, 50))
            texto_jogador_1 = fonte.render(f'Jogador 1 - Pontuação:{pontuacao[0]}', False, cores['azul'])
            texto_jogador_2 = fonte.render(f'Jogador 2 - Pontuação:{pontuacao[1]}', False, cores['vermelho'])
            texto_vez = fonte.render(f'Vez:{vez}', False, cores['preto'])
            tela.blit(texto_vez, (20, 201))
            tela.blit(texto_jogador_1, (20, 215))
            tela.blit(texto_jogador_2, (20, 230))

            for i in range(linhas):
                for j in range(colunas):
                    if revelado[i][j] == 1:
                        tela.blit(img_tesouro, (j * 50 , i * 50))
                    elif revelado[i][j] == 2:
                        tela.blit(img_buraco, (j * 50 , i * 50 ))
                    elif revelado[i][j] == 3:
                        texto_numeros = fonte.render(str(tabuleiro[i][j]), True, cores['preto'])
                        tela.blit(texto_numeros, (j * 50 + 20, i * 50 +20 ))

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
                msc_jogo.stop()
                msc_vitoria.play()
                
        pygame.display.update()

if __name__ == '__main__':
    main()
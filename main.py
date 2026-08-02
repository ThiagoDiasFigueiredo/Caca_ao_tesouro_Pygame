import pygame
import random
def main():
    #Tela
    pygame.init()
    largura = 200
    altura = 250
    tela = pygame.display.set_mode((largura,altura))
    pygame.display.set_caption('Caça ao tesouro')
    pontuacao = [0,0] #Pontuaçao[0] == Jogador 1 e pontuação[1] == Jogador 2
    
    som_tesouro = pygame.mixer.Sound("pygame_tesouro.wav")
    som_buraco = pygame.mixer.Sound("pygame_buraco.wav")
    som_contagem = pygame.mixer.Sound("pygame_contagem.wav")
    img_tesouro = pygame.transform.scale(pygame.image.load("tesouro.png"), (49,49))
    img_buraco = pygame.transform.scale(pygame.image.load("buraco.png"), (49, 49))
 #Desenhar as coisas
 
    cores = {
        'branca': (255,255,255),
        'azul': (0,0,255),
        'vermelho': (255,0,0),
        'preto': (0,0,0),
    }
    tela.fill(cores['branca'])
    
    lado_quadrado = 50
    num_linhas = 4
    tamanho_grade = lado_quadrado * num_linhas  # 200

    pos_y = 0
    #Linhas horizontais
    for i in range(num_linhas + 1):  # +1 para fechar a última borda
        pygame.draw.line(tela, cores['preto'], (0, pos_y), (tamanho_grade, pos_y), 1)
        pos_y += lado_quadrado

    
    pos_x = 0
    #Linhas verticais
    for j in range(num_linhas + 1):
        pygame.draw.line(tela, cores['preto'], (pos_x, 0), (pos_x, tamanho_grade), 1)
        pos_x += lado_quadrado

    fonte = pygame.font.Font(None,20)
    texto_jogador_1 = fonte.render(f'Jogador 1 - Pontuação: {pontuacao[0]}',False,cores['azul'])
    texto_jogador_2 = fonte.render(f'Jogador 2 - Pontuação: {pontuacao[1]}',False,cores['vermelho'])

#Tabuleiro
    linhas = 4
    colunas = 4
    tabuleiro = []
    for i in range(linhas):
        linha = []
        for j in range(colunas):
            linha.append(0)
        tabuleiro.append(linha)

#Spawn buraco/tesouro
    tesouros = 6
    buracos = 3
    contador = 0
    while contador < tesouros:
        linha = random.randint(0,linhas-1)
        coluna = random.randint(0,colunas-1)
        if tabuleiro[linha][coluna] == 0:
            tabuleiro[linha][coluna] = -1
            contador += 1
            
    contador = 0
    while contador < buracos:
            linha = random.randint(0,linhas-1)
            coluna = random.randint(0,colunas-1)
            if tabuleiro[linha][coluna] == 0:
                tabuleiro[linha][coluna] = -2
                contador += 1

    #Só para saber as posições 
    for linha in tabuleiro:
        print(linha)
#Revelação
    revelado = []
    for i in range(linhas):
        revelado.append([0]*colunas)
    
#Casas sem nada
    
    for i in range(linhas):
        for j in range(colunas):

            if tabuleiro[i][j] == 0:

                contar_tesouros = 0

                # Cima
                if i - 1 >= 0:
                    if tabuleiro[i - 1][j] == -1:
                        contar_tesouros += 1

                # Baixo
                if i + 1 < linhas:
                    if tabuleiro[i + 1][j] == -1:
                        contar_tesouros += 1

                # Esquerda
                if j - 1 >= 0:
                    if tabuleiro[i][j - 1] == -1:
                        contar_tesouros += 1

                # Direita
                if j + 1 < colunas:
                    if tabuleiro[i][j + 1] == -1:
                        contar_tesouros += 1

                tabuleiro[i][j] = contar_tesouros
#Qual jogador vai começar:
    vez = random.choice([1,2])
    print(f"Quem começa é o Jogador {vez}")
    #Looping do jogo
    running = True
    while running:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False
            if evento.type == pygame.MOUSEBUTTONDOWN:

                x, y = evento.pos
                coluna = x // 50
                linha = y // 50
                if y >= 200:
                    continue
                if revelado[linha][coluna] != 0: # Não pode clicar 2 vezes na mesma casa
                    continue
                    

                if tabuleiro[linha][coluna] == -1: #Tesouro
                    print(f'Jogador {vez} achou um tesouro!')
                    revelado[linha][coluna] = 1
                    som_tesouro.play()
                    if vez == 1:
                        pontuacao[0] += 100
                        vez = 2
                    else:
                        pontuacao[1] += 100
                        vez = 1

                elif tabuleiro[linha][coluna] == -2: #Buraco
                    
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
                    print(evento.pos)
                    som_contagem.play()
                    if vez == 1:
                        vez = 2
                    elif vez == 2:
                        vez = 1
            
        pygame.draw.rect(tela, cores['branca'], (0, 200, 200, 50))
        texto_jogador_1 = fonte.render(f'Jogador 1 - Pontuação:{pontuacao[0]}',False,cores['azul'])
        texto_jogador_2 = fonte.render(f'Jogador 2 - Pontuação:{pontuacao[1]}',False,cores['vermelho'])
        texto_vez = fonte.render(f'Vez:{vez}',False,cores['preto'])
        tela.blit(texto_vez,(20,200))
        tela.blit(texto_jogador_1,(20,210))
        tela.blit(texto_jogador_2,(20,230))

        for i in range(linhas):
            for j in range(colunas):
                if revelado[i][j] == 1:
                    
                    tela.blit(img_tesouro, (j * 50 + 1, i * 50 +1 , 49, 49))

                elif revelado[i][j] == 2:
                    
                    tela.blit(img_buraco, (j * 50 + 1 , i * 50 + 1 , 49, 49))

                elif revelado[i][j] == 3:
                    
                    texto_numeros = fonte.render(str(tabuleiro[i][j]),True,cores['preto'])
                    tela.blit(texto_numeros, (j * 50 + 20, i * 50 + 20))
        #Fechar jogo

        acabou = True
        for i in range(linhas):
            for j in range(colunas):
                    if revelado[i][j] == 0:
                        acabou = False
                
        if acabou:
            running = False
            
        pygame.display.update() 
        
if __name__ == '__main__':
    main()
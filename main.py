import pygame
import random
def main():
    #Tela
    pygame.init()
    largura = 200
    altura = 250
    tela = pygame.display.set_mode((largura,altura))
    pygame.display.set_caption('Caça ao tesouro')
    jogador_1 = 0
    jogador_2 = 0
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
    texto_jogador_1 = fonte.render(f'Jogador 1 - Pontuação: {jogador_1}',False,cores['azul'])
    texto_jogador_2 = fonte.render(f'Jogador 2 - Pontuação: {jogador_2}',False,cores['vermelho'])
#Spawn tesouro

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
    

    

#Casas sem nada
 
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

                if tabuleiro[linha][coluna] == -1:
                    print("Achou tesouro!")
                elif tabuleiro[linha][coluna] == -2:
                    print('Achou buraco!')
                else:
                    print("Nada")
                print(evento.pos)
        tela.blit(texto_jogador_1,(20,210))
        tela.blit(texto_jogador_2,(20,230))
        pygame.display.update()
if __name__ == '__main__':
    main()
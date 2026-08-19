# Caça ao Tesouro

Jogo desenvolvido em **Python + Pygame** como projeto final da disciplina de Introdução à Programação, sob orientação do professor Bruno Jefferson.

O jogo segue o enunciado original do "Caça ao Tesouro" (tabuleiro com tesouros e buracos revelados progressivamente), mas o nosso grupo foi além do escopo pedido, implementando:

- **Menu inicial** com tela de apresentação e música ambiente
- **Seleção de dificuldade**: Fácil (tabuleiro 4x4, sem diagonais) e Difícil (tabuleiro 8x8 ampliado, considerando também casas diagonais)
- **Efeitos sonoros e trilha sonora** para tesouro, buraco, contagem e vitória
- **Tela de vitória** dinâmica, indicando o vencedor ou empate

## Como jogar

1. No menu, pressione **ENTER** para iniciar
2. Escolha a dificuldade clicando em "Fácil" ou "Difícil"
3. Os dois jogadores se revezam clicando nas casas do tabuleiro:
   - **Tesouro**: +100 pontos
   - **Buraco**: -50 pontos (o placar não fica negativo)
   - **Número**: indica quantos tesouros há nas casas vizinhas (o placar não muda)
4. O jogo termina quando todas as casas forem reveladas — vence quem tiver mais pontos
5. Pressione **ESC** a qualquer momento para sair

## Tecnologias

- Python
- Biblioteca do Pygame (renderização, eventos de mouse/teclado, áudio)
- Conceitos aplicados: listas (matrizes do tabuleiro), funções, strings e módulos

## Autores

Projeto desenvolvido em grupo de 3 alunos:
- Raphael Brito
- Thiago Dias
- Matheus Meira

## Como executar

```bash
pip install pygame
python main.py
```


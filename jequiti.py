from random import randint
from re import sub
from base import base_de_dados

jogadores = {'Ana': 0, 'Bárbara': 0, 'Carlos': 0}
jogador_ativo = 'Ana'
valor_roleta = 0
tema = ''
palavras = []
letras_erradas = []
rodada = 0
turno = 0

def main():
    definir_tema()
    definir_palavras()
    passa_vez()
    painel()
    roleta()

def definir_tema(aleatorio = True, i = 0):
    global tema

    if aleatorio:
        tema = pegar_nome_por_numero(base_de_dados, randint(0, 9))
    else:
        tema = pegar_nome_por_numero(base_de_dados, i - 1)


def definir_palavras():
    global palavras

    if len(base_de_dados[tema]) > 3:

        while len(palavras) < 3:
            i = randint(0, len(base_de_dados[tema]) - 1)

            if list.count(palavras, base_de_dados[tema][i]) > 0:
                continue
            list.append(palavras, base_de_dados[tema][i])
    else:
        palavras = base_de_dados[tema]


def roleta():
    valores = []
    funcoes = [passa_vez, perdeu_tudo]
    for i in range(100, 951, 50):
        list.insert(valores, randint(0, len(valores)), i)
    
    for i in range(0, 2):
        for func in funcoes:
            list.insert(valores, randint(0, len(valores)), func)


def passa_vez():
    global jogador_ativo
    posicao = list(jogadores.keys()).index(jogador_ativo) + 1

    if posicao < len(jogadores):
        jogador_ativo = pegar_nome_por_numero(jogadores, posicao)
    else:
        jogador_ativo = jogadores[pegar_nome_por_numero(jogadores, 0)]


def perdeu_tudo():
    jogadores[jogador_ativo] = 0


def painel():
    print('+', '=' * 48, sep='')
    print('RODADA {} - TURNO {}'.format(rodada, turno))
    print('+', '=' * 48, sep='')

    for i in range(len(jogadores.keys())):
        print('|', '{} - {}'.format(pegar_nome_por_numero(jogadores, i), pegar_valor_por_numero(jogadores, i)), end=' ')

    print('')
    print('+', '=' * 48, sep='')
    print('Jogador ativo: {}'.format(jogador_ativo))
    print('Pontuação atual: {}'.format(jogadores[jogador_ativo]))
    print('Roleta: {}'.format(valor_roleta))
    print('Nova pontuação: {}'.format(jogadores[jogador_ativo]))
    print('+', '=' * 48, sep='')
    print('Tema: {}'.format(tema))
    print('+', '=' * 48, sep='')
    print('P1) {}'.format(mascara(palavras[0])))
    print('P2) {}'.format(mascara(palavras[1])))
    print('P3) {}'.format(mascara(palavras[2])))
    print('Letras erradas: {}'.format('Nenhuma' if len(letras_erradas) == 0 else str.join(letras_erradas, ', ')))
    print('+', '=' * 48, sep='')


def pegar_nome_por_numero(dicionario, i):
    return list(dicionario.keys())[i]


def pegar_valor_por_numero(dicionario, i):
    return dicionario[pegar_nome_por_numero(dicionario, i)]


def mascara(palavra):
    return sub('\w', '_', palavra)


main()
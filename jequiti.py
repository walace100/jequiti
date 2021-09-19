from random import randint
from re import sub, search, finditer, IGNORECASE
import unicodedata
from base import base_de_dados


jogadores = {'Ana': 0, 'Bárbara': 0, 'Carlos': 0}
jogador_ativo = 'Ana'
valor_roleta = 0
tema = ''
palavras = []
palavras_mascaradas = []
letras_usadas = []
valor_rodada = 0
valor_turno = 0


def main():
    for i in range(3):
        pre_turno()
        definir_rodada(i + 1)
        turno()
        adicionar_turno(True)


def pre_turno():
    limpar_vars()
    definir_tema()
    definir_palavras()
    definir_mascaras()


def turno():
    while True:
        adicionar_turno()
        rodar_roleta()
        painel()

        if not isinstance(valor_roleta, int):
            valor_roleta()
            continue

        acertou_pergunta = pergunta()

        if not acertou_pergunta:
            passa_vez()
            continue

        definir_pontuacao(valor_roleta)

        if falta_letras(): #
            if not dizer_palavras():
                continue

            painel()
            break

def dizer_palavras():
    while True:
        resposta = input('Deseja dizer todas as palavras? [S/N] ')

        if resposta.upper() not in 'SN':
            continue
        elif resposta.upper() == 'S':
            return True
        else:
            return False


def definir_pontuacao(pontuacao):
    print(pontuacao)
    jogadores[jogador_ativo] += pontuacao


def falta_letras():
    falta_total = 0
    for p in palavras_mascaradas:
        falta_total += str.count(p, '_')

    if falta_total <= 3:
        return True
    return False


def pergunta():
    while True:
        resposta = input('Valendo {} reais, uma letra: '.format(valor_roleta))
        resposta_validada = validar_resposta(resposta)

        if not resposta_validada[0]:
            print(resposta_validada[1])
            continue

        adicionar_letra_usada(resposta)
        return substituir_letras_mascarada(resposta)


def substituir_letras_mascarada(letra):
    palavra = sem_acento(letra).upper()
    acertou_letra = False
    palavras_sem_acento = []

    for p in palavras:
        list.append(palavras_sem_acento, sem_acento(p))

    for i in range(len(palavras_sem_acento)):
        pos = []

        if palavra in palavras_sem_acento[i].upper():
            acertou_letra = True

            for occ in finditer(palavra, palavras_sem_acento[i], flags=IGNORECASE):
                list.append(pos, occ.start())

        for p in pos:
            palavras_mascaradas[i] = palavras_mascaradas[i][:p] + palavra + palavras_mascaradas[i][p + 1:]

    return acertou_letra


def sem_acento(palavra):
    return unicodedata.normalize('NFKD', palavra).encode('ASCII', 'ignore').decode("utf-8") 


def validar_resposta(resposta):
    palavra = resposta.strip().upper()

    if search('[\u00C0-\u017F]', palavra):
        return (False, 'Digite uma letra sem acento. Tente novamente.')
    elif len(palavra) > 1:
        return (False, 'Digite apenas uma letra. Tente novamente.')
    elif palavra in letras_usadas:
        return (False, 'A letra já foi utilizada. Tente novamente.')
    elif len(palavra) < 1:
        return (False, 'É preciso digitar uma letra. Tente novamente.')
    else:
        return (True,)


def definir_rodada(r):
    global valor_rodada
    valor_rodada = r


def limpar_vars():
    global palavras
    global palavras_mascaradas
    global letras_usadas

    palavras_mascaradas = []
    palavras = []
    letras_usadas = []


def adicionar_letra_usada(letra):
    list.append(letras_usadas, letra.upper())


def adicionar_turno(zerar = False):
    global valor_turno
    
    if zerar:
        valor_turno = 0
    else:
        valor_turno += 1


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


def definir_mascaras():
    for p in palavras:
        list.append(palavras_mascaradas, mascara(p))


def roleta():
    valores = []
    funcoes = [passa_vez, perdeu_tudo]
    for i in range(100, 951, 50):
        list.insert(valores, randint(0, len(valores)), i)
    
    for i in range(2):
        for func in funcoes:
            list.insert(valores, randint(0, len(valores)), func)

    return valores


def rodar_roleta():
    global valor_roleta

    roleta_rodada = roleta()
    valor_roleta = roleta_rodada[randint(0, len(roleta_rodada) -1)]


def passa_vez():
    global jogador_ativo
    posicao = list(jogadores.keys()).index(jogador_ativo) + 1

    if posicao < len(jogadores):
        jogador_ativo = pegar_nome_por_numero(jogadores, posicao)
    else:
        jogador_ativo = pegar_nome_por_numero(jogadores, 0)


def perdeu_tudo():
    jogadores[jogador_ativo] = 0
    passa_vez()


def painel():
    print('+', '=' * 48, sep='')
    print('RODADA {} - TURNO {}'.format(valor_rodada, valor_turno))
    print('+', '=' * 48, sep='')

    for i in range(len(jogadores.keys())):
        print('|', '{} - {}'.format(pegar_nome_por_numero(jogadores, i), pegar_valor_por_numero(jogadores, i)), end=' ')

    print('')
    print('+', '=' * 48, sep='')
    print('Jogador ativo: {}'.format(jogador_ativo))
    print('Pontuação atual: {}'.format(jogadores[jogador_ativo]))

    if isinstance(valor_roleta, int):
        print('Roleta: {}'.format(valor_roleta))
    elif valor_roleta.__name__ == 'passa_vez':
        print('Roleta: PASSOU A VEZ!!!')
    else:
        print('Roleta: PERDEU TUDO!!!')

    print('Nova pontuação: {}'.format(jogadores[jogador_ativo]))
    print('+', '=' * 48, sep='')
    print('Tema: {}'.format(tema))
    print('+', '=' * 48, sep='')
    print('P1) {}'.format(palavras_mascaradas[0]))
    print('P2) {}'.format(palavras_mascaradas[1]))
    print('P3) {}'.format(palavras_mascaradas[2]))
    print('Letras já faladas: {}'.format('Nenhuma' if len(letras_usadas) == 0 else str.join(', ', letras_usadas)))
    print('+', '=' * 48, sep='')


def pegar_nome_por_numero(dicionario, i):
    return list(dicionario.keys())[i]


def pegar_valor_por_numero(dicionario, i):
    return dicionario[pegar_nome_por_numero(dicionario, i)]


def mascara(palavra):
    return sub('\w', '_', palavra)


if __name__ == '__main__':
    main()

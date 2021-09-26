from random import randint
from re import sub, search, finditer
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

        if not pergunta():
            passa_vez()
            continue

        definir_pontuacao(valor_roleta)

        if falta_letras():
            painel()

            if not dizer_palavras():
                continue

            break


def dizer_palavras():
    while True:
        resposta = input('Deseja dizer todas as palavras? [S/N] ')

        if resposta.upper() not in 'SN':
            print('Digite um caracter válido.')
            continue
        elif resposta.upper() == 'S':
            quantidade_acertos = 0

            for i in range(3):
                palavra = input('Valendo {}, digite a {}º palavra: '.format(jogadores[jogador_ativo] * 2, i + 1))

                if palavra.upper() in respostas_sem_acento():
                    quantidade_acertos += 1
                else:
                    return False

            if quantidade_acertos >= 3:
                definir_pontuacao(jogadores[jogador_ativo] * 2)

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

    if falta_total <= 3 and falta_total > 0:
        return True
    return False


def pergunta():
    while True:
        resposta = input('Valendo {} reais, uma letra: '.format(valor_roleta))
        resposta_validada = validar_resposta(resposta)

        if not resposta_validada[0]:
            print(f"\033[1;31m{resposta_validada[1]}\033[m")
            continue

        adicionar_letra_usada(resposta)
        return substituir_letras_mascarada(resposta)


def substituir_letras_mascarada(letra):
    palavra = sem_acento(letra).upper()
    acertou_letra = False
    palavras_sem_acento = respostas_sem_acento()

    for i in range(len(palavras_sem_acento)):
        pos = []

        if palavra in palavras_sem_acento[i]:
            acertou_letra = True

            for occ in finditer(palavra, palavras_sem_acento[i]):
                list.append(pos, occ.start())

        for p in pos:
            palavras_mascaradas[i] = palavras_mascaradas[i][:p] + palavra + palavras_mascaradas[i][p + 1:]

    return acertou_letra


def respostas_sem_acento():
    palavras_sem_acento = []

    for p in palavras:
        list.append(palavras_sem_acento, sem_acento(p).upper())
    
    return palavras_sem_acento


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
    valor_roleta = roleta_rodada[randint(0, len(roleta_rodada) - 1)]


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
    print(f"\033[4;31m+{'=' * 48}\033[m", sep='')
    print('\033[1;37;40mRODADA {} - TURNO {}\033[m'.format(valor_rodada, valor_turno))
    print(f"\033[4;31m+{'=' * 48}\033[m", sep='')


    for i in range(len(jogadores.keys())):
        print(f"\033[1;35;40m| {pegar_nome_por_numero(jogadores, i)} - {pegar_valor_por_numero(jogadores, i)}\033[m", end=' ')

    print('')
    print(f"\033[4;31m+{'=' * 48}\033[m", sep='')

    print('\033[1;37;40mJogador ativo:\033[m \033[1;35;40m{}\033[m'.format(jogador_ativo))
    print('\033[1;37;40mPontuação atual: \033[1;33;40m{}\033[m'.format(jogadores[jogador_ativo]))

    if isinstance(valor_roleta, int):
        print('\033[1;37;40mRoleta:\033[m \033[1;32;40m{}\033[m'.format(valor_roleta))
    elif valor_roleta.__name__ == 'passa_vez':
        print('\033[1;37;40mRoleta:\033[m \033[1;31;40mPASSOU A VEZ!!!\033[m')
    else:
        print('\033[1;37;40mRoleta:\033[m \033[1;31;40mPERDEU TUDO!!!\033[m')

    print('\033[1;37;40mNova pontuação:\033[m \033[1;32;40m{}\033[m'.format(jogadores[jogador_ativo]))
    print(f"\033[4;31m+{'=' * 48}\033[m", sep='')

    print(f"\033[1;37;40mTema:\033[m \033[1;{randint(30, 37)};40m{tema}\033[m")
    print(f"\033[4;31m+{'=' * 48}\033[m", sep='')

    print('\033[1;31;40mP1) {}\033[m'.format(palavras_mascaradas[0]))
    print('\033[1;33;40mP2) {}\033[m'.format(palavras_mascaradas[1]))
    print('\033[1;32;40mP3) {}\033[m'.format(palavras_mascaradas[2]))
    print(f"\033[1;37;40mLetras já faladas:\033[m \033[1;{randint(30, 37)};40m{'Nenhuma' if len(letras_usadas) == 0 else str.join(', ', letras_usadas)}\033")
    print(f"\033[4;31m+{'=' * 48}\033[m", sep='')


def pegar_nome_por_numero(dicionario, i):
    return list(dicionario.keys())[i]


def pegar_valor_por_numero(dicionario, i):
    return dicionario[pegar_nome_por_numero(dicionario, i)]


def mascara(palavra):
    return sub('\w', '_', palavra)


if __name__ == '__main__':
    main()

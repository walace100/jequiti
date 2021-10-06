from random import randint, sample
from re import sub, search, findall, IGNORECASE
import unicodedata
from base import base_de_dados, rodada_final


jogadores = {'Ana': 0, 'Bárbara': 0, 'Carlos': 0}
jogador_ativo = 'Ana'
valor_roleta = 0
tema = ''
palavras = []
palavra_final = ''
palavras_mascaradas_final = ''
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
    ganhador()
    ultima_rodada()


def ultima_rodada():
    definir_tema(True)
    definir_palavra_final()
    definir_mascara_final()
    painel_final()
    letras = pedir_letras()
    substituir_letras_mascarada_final(letras)
    painel_final()
    if dizer_palavra_final():
        sucesso(f"Parabéns!!! o jogador {jogador_ativo} ganhou {jogadores[jogador_ativo]} reais!!!")
    else:
        erro(f"Infelizmente você errou, a palavra certa era {palavra_final.upper()}, você saiu com {jogadores[jogador_ativo]} reais")


def dizer_palavra_final():
    palavra = sem_acento(input('Valendo {} reais, digite a palavra: '.format(jogadores[jogador_ativo] * 2)))

    if palavra.upper() == sem_acento(palavra_final).upper():
        definir_pontuacao(jogadores[jogador_ativo] * 2)
        return True
    return False


def substituir_letras_mascarada_final(letras):
    global palavra_final
    global palavras_mascaradas_final

    palavra_final_sem_acento = sem_acento(palavra_final).upper()
    letras_separadas = [letra.upper() for letra in letras]

    for i in range(len(palavra_final_sem_acento)):
        pos = []

        for letra_separada in letras_separadas:
            if palavra_final_sem_acento[i] == letra_separada:
                list.append(pos, i)
        
        for j in pos:
            palavras_mascaradas_final = palavras_mascaradas_final[:j] + palavra_final_sem_acento[i] + palavras_mascaradas_final[j + 1:]


def definir_palavra_final():
    global tema
    global palavra_final

    i = randint(0, len(rodada_final[tema]) - 1)
    palavra_final = rodada_final[tema][i]


def definir_mascara_final():
    global palavras_mascaradas_final
    palavras_mascaradas_final = mascara(palavra_final)


def ganhador():
    maior_valor = sorted(list(jogadores.values()), reverse=True)[0]

    for jogador in jogadores.items():
        if jogador[1] == maior_valor:
            jogador_ganhador = jogador[0]
            break

    sucesso(f"O grande ganhou foi {jogador_ganhador}!!!")
    sucesso(f"Parabéns {jogador_ganhador}, você ganhou {jogadores[jogador_ganhador]} reais!!!")
    sucesso(f"O ganhador {jogador_ganhador} foi selecionado para a RODADA FINAL")


def pedir_letras():
    while True:
        letras = input('Digite 5 consoantes e 1 vogal sem utilizar espaço ou qualquer separação: ')

        if not validar_letras(letras):
            continue
        return letras


def validar_letras(letras):
    if not len(findall('[b-df-hj-np-tv-xz]', letras, flags=IGNORECASE)) == 5:
        erro('Digite 5 consoantes. Tente novamente.')
        return False
    if not len(findall('[aeiou]', letras, flags=IGNORECASE)) == 1:
        erro('Digite 1 vogal. Tente novamente.')
        return False
    if search('[\u00C0-\u017F]', letras):
        erro('Digite uma letra sem acento. Tente novamente.')
        return False
    return True


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

        if not falta_zero_letras() and not pergunta():
            passa_vez()
            continue

        definir_pontuacao(valor_roleta)

        if falta_zero_letras():
            break

        if falta_tres_letras():
            painel()

            if dizer_palavras():
                break
            continue


def dizer_palavras():
    while True:
        resposta = input('Deseja dizer todas as palavras? [S/N] ')

        if resposta.upper() not in 'SN':
            erro('Digite um caracter válido.')
            continue
        elif resposta.upper() == 'S':
            quantidade_acertos = 0

            for i in range(3):
                palavra = sem_acento(input('Valendo {} reais, digite a {}º palavra: '.format(jogadores[jogador_ativo] * 2, i + 1)))

                if palavra.upper() in respostas_sem_acento():
                    quantidade_acertos += 1
                else:
                    return False

            if quantidade_acertos >= 3:
                sucesso(f"O jogador {jogador_ativo}, ganhou {jogadores[jogador_ativo] * 2} reais")
                definir_pontuacao(jogadores[jogador_ativo] * 2)

            return True
        else:
            return False


def definir_pontuacao(pontuacao):
    jogadores[jogador_ativo] += pontuacao


def falta_letras():
    falta_total = 0
    for p in palavras_mascaradas:
        falta_total += str.count(p, '_')

    return falta_total


def falta_tres_letras():
    falta_total = falta_letras()

    if falta_total <= 3 and falta_total > 0:
        return True
    return False


def falta_zero_letras():
    return falta_letras() == 0


def pergunta():
    while True:
        resposta = input('Valendo {} reais, uma letra: '.format(valor_roleta))
        resposta_validada = validar_resposta(resposta)

        if not resposta_validada[0]:
            erro(resposta_validada[1])
            continue

        adicionar_letra_usada(resposta)
        return substituir_letras_mascarada(resposta)


def substituir_letras_mascarada(letra):
    palavra = sem_acento(letra).upper()
    acertou_letra = False
    palavras_sem_acento = respostas_sem_acento()

    for i in range(len(palavras_sem_acento)):
        if palavra in palavras_sem_acento[i]:
            acertou_letra = True

            for j in range(len(palavras[i])):
                if palavra == sem_acento(palavras[i][j]).upper():
                    palavras_mascaradas[i] = palavras_mascaradas[i][:j] + palavras[i][j].upper() + palavras_mascaradas[i][j + 1:]

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


def definir_tema(final=False):
    global tema

    if final:
        tema = pegar_nome_por_numero(rodada_final, randint(0, 9))
    else:
        tema = pegar_nome_por_numero(base_de_dados, randint(0, 9))


def definir_palavras():
    global palavras

    if len(base_de_dados[tema]) > 3:
        palavras = sample(base_de_dados[tema], k=3)
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


def painel_final():
    print(f"\033[4;31m+{'=' * 48}\033[m", sep='')
    print('\033[1;37;40mRODADA FINAL\033[m')
    print(f"\033[4;31m+{'=' * 48}\033[m", sep='')
    print('\033[1;37;40mJogador ativo:\033[m \033[1;35;40m{}\033[m'.format(jogador_ativo))
    print('\033[1;37;40mPontuação atual: \033[1;33;40m{}\033[m'.format(jogadores[jogador_ativo]))
    print('\033[1;37;40mNova pontuação:\033[m \033[1;32;40m{}\033[m'.format(jogadores[jogador_ativo] * 2))
    print(f"\033[4;31m+{'=' * 48}\033[m", sep='')
    print(f"\033[1;37;40mTema:\033[m \033[1;{randint(30, 37)};40m{tema}\033[m")
    print(f"\033[4;31m+{'=' * 48}\033[m", sep='')
    print('\033[1;37;40mPalavra Final: {}\033[m'.format(palavras_mascaradas_final))
    print(f"\033[4;31m+{'=' * 48}\033[m", sep='')


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
        print('\033[1;37;40mNova pontuação:\033[m \033[1;32;40m{}\033[m'.format(jogadores[jogador_ativo] + valor_roleta))
    elif valor_roleta.__name__ == 'passa_vez':
        print('\033[1;37;40mRoleta:\033[m \033[1;31;40mPASSOU A VEZ!!!\033[m')
        print('\033[1;37;40mNova pontuação:\033[m \033[1;37;40m{}\033[m'.format(jogadores[jogador_ativo]))
    else:
        print('\033[1;37;40mRoleta:\033[m \033[1;31;40mPERDEU TUDO!!!\033[m')
        print('\033[1;37;40mNova pontuação:\033[m \033[1;37;40m0\033[m')

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


def sucesso(msg):
    print(f"\033[1;32;40m{msg}\033[m")


def erro(msg):
    print(f"\033[1;31;40m{msg}\033[m")


if __name__ == '__main__':
    main()

# reescrever o código
    # colocar sleeps
    # tirar variaveis globais
    # fazer documentação

import unicodedata

from time import sleep
from random import randint, sample, choice
from re import sub, search, findall, finditer, IGNORECASE


def main() -> None:
    """Função principal que executa outras funções para o funcionamento do roda roda.
    """
    # Bases de dados.

    from base import base_de_dados, rodada_final

    # Vars "globais"

    # Armazena os dados dos jogadores.
    jogadores = {'Ana': 0, 'Bárbara': 0, 'Carlos': 0}
    # Armazena o jogador ativo no momento.
    jogador_ativo = 'Ana'

    # Armazena em qual rodada está.
    valor_rodada = 0

    sucesso("Bem vindo ao Roda Roda jequiti!")
    sleep(1)

    for _ in range(3):
    # Pré turno
        # limpa as variáveis utilizadas na rodada.

        # Armazena as máscaras das palavras escolhidas do tema.
        palavras_mascaradas = []
        # Armazena as palavras escolhidas do tema.
        palavras = []
        # Armazena as letras já ditas durante a rodada.
        letras_usadas = []

        # Define a rodada atual.
        valor_rodada += 1
        # Reseta o valor do turno
        valor_turno = 0

        # Define o tema da rodada.
        tema = choice(list(base_de_dados))

        # Define as palavras do tema.
        palavras = definir_palavras(base_de_dados, tema)

        # Define as máscaras das palavras.
        palavras_mascaradas = definir_mascaras(palavras)

    # Turno
        while True:
            # adiciona mais um ao valor do turno.
            valor_turno = adicionar_turno(valor_turno)

            # roda a roleta.
            valor_roleta = rodar_roleta()

            msg_cor("Rodando a roleta...", 37)
            sleep(2)

            if isinstance(valor_roleta, int):
                sucesso(f"A roleta parou em {valor_roleta} reais!")
            elif not isinstance(valor_roleta, int) and valor_roleta.__name__ == 'passa_vez':
                erro("PASSOU A VEZ!!!")
            else:
                erro("PERDEU TUDO!!!")
            sleep(1)

            painel(valor_rodada, valor_turno, valor_roleta, jogadores, jogador_ativo, tema, palavras_mascaradas, letras_usadas)

            if not isinstance(valor_roleta, int):
                jogador_ativo = valor_roleta(jogadores, jogador_ativo)
                continue

            if falta_letras(palavras_mascaradas) != 0:
                letra = pergunta(valor_roleta, letras_usadas)

                letras_usadas = adicionar_letra_usada(letra, letras_usadas)

                if acertou_letra(letra, palavras):
                    jogador_ativo = passa_vez(jogadores, jogador_ativo)
                    continue

                palavras_mascaradas = substituir_letras_mascarada(letra, palavras_mascaradas, palavras)

            # define uma nova pontuação
            jogadores[jogador_ativo] += valor_roleta

            if falta_letras(palavras_mascaradas) == 0:
                break

            if falta_letras(palavras_mascaradas) <= 3:
                painel(valor_rodada, valor_turno, valor_roleta, jogadores, jogador_ativo, tema, palavras_mascaradas, letras_usadas)

                sleep(.5)
                if perguntar_palavras() and dizer_palavras(jogador_ativo, palavras):
                    jogadores[jogador_ativo] += 1000
                    break
                continue

    # ganhador
    sleep(1)
    ganhador(jogadores)

    # rodada final

    # define o tema da rodada final.
    tema = pedir_tema(rodada_final)

    # Armazena a palavra para a rodada final.
    palavra_final = choice(rodada_final[tema])

    # Armazena a máscara da palavra da rodada final.
    palavra_mascarada_final = mascara(palavra_final)

    painel_final(jogadores, jogador_ativo, palavra_mascarada_final, tema)

    letra_final = pedir_letras()

    palavra_mascarada_final = substituir_letras_mascarada_final(letra_final, palavra_mascarada_final, palavra_final)

    painel_final(jogadores, jogador_ativo, palavra_mascarada_final, tema)

    if dizer_palavra_final(jogadores, jogador_ativo, palavra_final):
        jogadores[jogador_ativo] *= 2
        sucesso(f"Parabéns!!! o jogador {jogador_ativo} ganhou {jogadores[jogador_ativo]} reais!!!")
    else:
        erro(f"Infelizmente você errou, a palavra certa era {palavra_final.upper()}, você saiu com {jogadores[jogador_ativo]} reais")


def pegar_nome_por_numero(dicionario: dict, i: int) -> str:
    """Retorna o chave de um dicionário com base no índice dela.
    
    Args:
        dicionario: um dicionário onde a chave será o item retornado.
        i: é po índice que será procurado no dicionário.
    Returns:
        Retorna o valor da chave do dicionário.
    """
    return list(dicionario.keys())[i]


def pegar_valor_por_numero(dicionario: dict, i: int) -> list:
    """Retorna o valor de uma lista com base no índice dela.
    
    Args:
        dicionario: um dicionário onde a chave será o item retornado.
        i: é po índice que será procurado no dicionário.
    Returns:
        Retorna o valor da chave do dicionário que é uma lista.
    """
    return dicionario[pegar_nome_por_numero(dicionario, i)]


def definir_palavras(base: dict, tema: str) -> list:
    """Retorna uma lista com as palavras do tema.

    Ele retorna uma lista de tamanho 3 com os valores do dicionário passado no parâmetro.

    Args:
        base: um dicionário que será utilizado para extrair os valores.
        tema: é a chave que será utilizada no dicionário.
    Returns:
        Retorna uma lista com 3 valores do dicionário.
    """
    if len(base[tema]) > 3:
        return sample(base[tema], k=3)
    else:
        return base[tema]


def definir_mascaras(palavras: list) -> list:
    """ Retorna as máscaras das palavras do tema escolhido.

    Args:
        palavras: uma lista com as palavras que vão ser mascaradas.
    Returns:
        Retorna uma lista com as máscaras definidas com underscore (_)
    """
    return [mascara(p) for p in palavras]


def mascara(palavra: str) -> str:
    """Retorna uma máscara de uma palavra.

    Retorna uma máscara baseada em underscore (_) de uma string.

    Args:
        palavra: uma string que será utilizada na máscara.
    Returns:
        Retorna uma string com a máscara feita utilizindo underscode (_).
    """
    return sub('\w', '_', palavra)


def adicionar_turno(valor_turno: int) -> int:
    """Adiociona mais um no valor do turno.

    Args:
        valor_turno: o valor do turno que será utilizado.
    Returns:
        Retorna o valor novo do turno.
    """
    return valor_turno + 1


def rodar_roleta() -> any:
    """Retorna o valor da roleta girada.

    Returns:
        Retorna um novo valor da roleta.
    """
    valores = [i for i in range(100, 951, 50)]
    valores.extend([passa_vez, perdeu_tudo, 1000, 1000])
    return sample(valores, k=1)[0]


def passa_vez(jogadores: dict, jogador_ativo: str) -> str:
    """Passa a vez do jogador ativo.

    Args:
        jogadores: um dicionário com os dados dos jogadores.
        jogador_ativo: uma string com o nome do jogador ativo.
    Returns:
        Retorna o nome do próximo jogador.
    """
    pos = list(jogadores.keys()).index(jogador_ativo) + 1

    if pos < len(jogadores):
        return pegar_nome_por_numero(jogadores, pos)
    return pegar_nome_por_numero(jogadores, 0)


def perdeu_tudo(jogadores: dict, jogador_ativo: str) -> str:
    """O jogador ativo perde toda a sua pontuação e passa a vez.

    Args:
        jogadores: um dicionário com os dados dos jogadores.
        jogador_ativo: uma string com o nome do jogador ativo.
    Returns:
        Retorna o nome do próximo jogador.
    """
    jogadores[jogador_ativo] = 0
    return passa_vez(jogadores, jogador_ativo)


def painel(valor_rodada: int, valor_turno: int, valor_roleta: any, jogadores: dict, jogador_ativo: str, tema: str, palavras_mascaradas: list, letras_usadas: list) -> None:
    """Mostra na tela o painel contendo as informações para o jogador.

    Args:
        valor_rodada: o valor da rodada.
        valor_turno: o valor do turno.
        valor_roleta: o valor da roleta.
        jogadores: base de dados dos jogadores.
        jogador_ativo: o nome do jogador ativo.
        tema: o tema da rodada.
        palavras_mascaradas: uma lista com as palavras mascaradas.
        letras_usadas: uma lista com as letras usadas.
    """
    sleep(.1)
    painel_separacao()
    msg_cor(f"RODADA {valor_rodada} - TURNO {valor_turno}", 37)
    painel_separacao()
    sleep(.1)

    for i in range(len(jogadores.keys())):
        msg_cor(f"| {pegar_nome_por_numero(jogadores, i)} - {pegar_valor_por_numero(jogadores, i)}", 35, end=" ")

    print("")
    painel_separacao()
    sleep(.1)

    msg_cor(f"Jogador ativo:\033[m \033[1;35;40m{jogador_ativo}\033[m", 37)
    msg_cor(f"Pontuação atual: \033[1;33;40m{jogadores[jogador_ativo]}\033[m", 37)

    sleep(.1)
    if isinstance(valor_roleta, int):
        msg_cor(f"Roleta:\033[m \033[1;32;40m{valor_roleta}\033[m", 37)
        msg_cor(f"Nova pontuação:\033[m \033[1;32;40m{jogadores[jogador_ativo] + valor_roleta}\033[m", 37)
    elif valor_roleta.__name__ == 'passa_vez':
        msg_cor(f"Roleta:\033[m \033[1;31;40mPASSOU A VEZ!!!\033[m", 37)
        msg_cor(f"Nova pontuação:\033[m \033[1;37;40m{jogadores[jogador_ativo]}\033[m", 37)
    else:
        msg_cor(f"Roleta:\033[m \033[1;31;40mPERDEU TUDO!!!\033[m", 37)
        msg_cor(f"Nova pontuação:\033[m \033[1;37;40m0\033[m", 37)

    painel_separacao()
    sleep(.1)

    msg_cor(f"\033[1;37;40mTema:\033[m \033[1;{randint(30, 37)};40m{tema}\033[m", 37)
    painel_separacao()
    sleep(.1)

    msg_cor(f"P1) {palavras_mascaradas[0]}", 31)
    msg_cor(f"P1) {palavras_mascaradas[1]}", 33)
    msg_cor(f"P1) {palavras_mascaradas[2]}", 32)
    msg_cor(f"Letras já faladas:\033[m \033[1;{randint(30, 37)};40m{'Nenhuma' if len(letras_usadas) == 0 else str.join(', ', letras_usadas)}\033[m", 37)
    painel_separacao()
    sleep(.1)


def painel_separacao() -> None:
    """Mostra na tela uma linha de separação."""
    print(f"\033[4;31m+{'=' * 48}\033[m", sep='')


def msg_cor(msg: str, cor: int, **kwargs: dict) -> None:
    """Mostra na tela uma mensagem com uma cor personalizada.

    Args:
        msg: uma string com a mensagem.
        cor: um inteiro contendo o número da cor.
    """
    print(f"\033[1;{cor};40m{msg}\033[m", **kwargs)


def erro(msg: str) -> None:
    """Mostra uma mensagem de erro.

    Args:
        msg: mensagem a ser exibida.
    """
    print(f"\033[1;31;40m{msg}\033[m")


def sucesso(msg: str) -> None:
    """Mostra uma mensagem de sucesso.

    Args:
        msg: mensagem a ser exibida.
    """
    print(f"\033[1;32;40m{msg}\033[m")


def falta_letras(palavras_mascaradas: list) -> int:
    """Retorna o valor de quantos understore existem.

    Args:
        palavras_mascaradas: lista com as palavras que serão verificadas.
    Returns:
        retorna o valor da soma de underscore da lista.
    """
    return sum([str.count(p, '_') for p in palavras_mascaradas])


def pergunta(valor_roleta: int, letras_usadas: list) -> str:
    """Faz a pergunta de qual letra é a de umas palavra do tema.

    Args:
        valor_roleta: usa o valor da roleta para mostrar no input.
        letras_usadas: lista com as letras usadas ao longo da rodada.
    Returns:
        retorna a letra dita.
    """
    while True:
        resposta = input(f"Valendo {valor_roleta} reais, uma letra: ")

        sleep(1)
        msg_cor("Processando...", 37)
        sleep(1)

        resposta_validada = validar_resposta(resposta, letras_usadas)

        if not resposta_validada[0]:
            erro(resposta_validada[1])
            continue
        return resposta


def validar_resposta(resposta: str, letras_usadas: list):
    """Valida uma string.

    Verifica se a palavra tem acentuação, se a palavra é maior que 1, se a letra foi utilizada,
    ou se a palavra é menor que 1.

    Args:
        resposta: a string a ser verificada.
        letras_usadas: lista com as letras usadas.
    Returns:
        retorna uma tupla com o primeiro argumento um bool, e o segundo um texto com o motivo do erro.
    """
    palavra = resposta.strip().upper()

    if search('[\u00C0-\u017F]', palavra):
        return (False, 'Digite uma letra sem acento. Tente novamente.')
    elif len(palavra) > 1:
        return (False, 'Digite apenas uma letra. Tente novamente.')
    elif search('\W', palavra) or search('\d', palavra):
        return (False, 'Digite apenas letras. Tente novamente.')
    elif palavra in letras_usadas:
        return (False, 'A letra já foi utilizada. Tente novamente.')
    elif len(palavra) < 1:
        return (False, 'É preciso digitar uma letra. Tente novamente.')
    else:
        return (True,)


def adicionar_letra_usada(letra: str, letras_usadas: list) -> list:
    """Adiciona uma letra usada.

    Args:
        letra: a letra que vai ser adicionada.
        letras_usadas: lista com as letras usadas.
    Returns:
        retorna uma lista com as letras_usadas atualizada.
    """
    letras_usadas.append(letra.upper())
    return letras_usadas


def substituir_letras_mascarada(letra: str, palavras_mascaradas: list, palavras: list) -> list:
    """Substitui a letra na máscara.

    Args:
        letra: a letra que vai ser substituída.
        palavras_mascaradas: uma lista onde estão as máscaras.
        palavras: uma lista onde estão as respostas das máscaras.
    Returns:
        Retorna uma nova lista com as máscaras atualizadas.
    """
    palavras_sem_acento = [sem_acento(p).upper() for p in palavras]

    for i in range(len(palavras_sem_acento)):
        matchs = finditer(letra, palavras_sem_acento[i], flags=IGNORECASE)
        pos = [match.span()[0] for match in matchs]

        for j in pos:
            palavras_mascaradas[i] = palavras_mascaradas[i][:j] + palavras[i][j].upper() + palavras_mascaradas[i][j + 1:]

    return palavras_mascaradas


def sem_acento(palavra: str) -> str:
    """Remove qualquer acentuação da palavra.

    Args:
        palavra: A string que vai ser removida a acentuação.
    Returns:
        Retorna a string sem acentuação.
    """
    return unicodedata.normalize('NFKD', palavra).encode('ASCII', 'ignore').decode("utf-8")


def acertou_letra(letra: str, palavras: str) -> bool:
    """Verifica se a letra dita foi acertada.

    Args:
        letra: a letra dita pelo jogador.
        palavras: lista de palavras com as respostas.
    Returns
        returna True ou False dependendo se a palavra está na lista de resposta.
    """
    palavras_sem_acento = [sem_acento(p).upper() for p in palavras]

    for p in palavras_sem_acento:
        if letra in p:
            return True
    return False


def perguntar_palavras() -> bool:
    """Pergunta se o jogador quer falar as 3 palavras.

    Returns:
        Retorna um bool de acordo com a resposta do jogador.
    """
    while True:
        resposta = input('Deseja dizer todas as palavras? [S/N] ')

        sleep(1)
        msg_cor("Processando...", 37)
        sleep(.5)

        if resposta.upper() not in 'SN':
            erro('Digite um caracter válido.')
            continue
        elif resposta.upper() == 'S':
            return True
        else:
            return False


def dizer_palavras(jogador_ativo: str, palavras: list) -> bool:
    """Pergunta as 3 palavras do tema da rodada.

    Args:
        jogador_ativo: um texto com o nome do jogador ativo.
        palavras: uma lista com as palavras certas.
    Returns:
        Irá retornar um bool dependendo se o jogador acertar as 3 palavras.
    """
    quantidade_acertos = 0

    for i in range(3):
        palavra = sem_acento(input(f"Valendo, 1000 reais, digite a {i + 1}º palavra: "))

        sleep(1)
        msg_cor("Processando...", 37)
        sleep(.5)

        palavras_sem_acento = [sem_acento(p).upper() for p in palavras]

        if palavra.upper() in palavras_sem_acento:
            quantidade_acertos += 1
        else:
            return False

    if quantidade_acertos == 3:
        sucesso(f"O jogador {jogador_ativo}, ganhou 1000 reais")
        return True


def ganhador(jogadores: dict) -> None:
    """Verifica qual foi o ganhador, envia uma mensagem e indica para a rodada final.

    Args:
        jogadores: um dicionário com os dados dos jogadores.
    """
    maior_valor = sorted(list(jogadores.values()), reverse=True)[0]

    for jogador in jogadores.items():
        if jogador[1] == maior_valor:
            jogador_ganhador = jogador[0]
            break

    sucesso(f"O grande ganhou foi {jogador_ganhador}!!!")
    sleep(.25)
    sucesso(f"Parabéns {jogador_ganhador}, você ganhou {jogadores[jogador_ganhador]} reais!!!")
    sleep(.25)
    sucesso(f"O ganhador {jogador_ganhador} foi selecionado para a RODADA FINAL")
    sleep(2)


def pedir_tema(base: dict) -> str:
    """Pede para escolher um número de 1 a 10 para escolher o tema.

    Args:
        base: o dicionário com os temas.
    Returns:
        Retorna o nome do tema.
    """
    while True:
        numero = input('Digite um número de 1 a 10 para escolher o tema: ')

        if not validar_numero(numero):
            continue
        
        return pegar_nome_por_numero(base, int(numero) - 1)


def validar_numero(numero: str) -> bool:
    """Valida o número de um input, verifica se é um número valido para escolher o tema.

    Args:
        numero: o numero que vai ser validado.
    Returns:
        retorna um bool se o valor é válido.
    """
    if search('\D', numero):
        erro('Digite apenas números. Tente novamente.')
        return False
    elif len(numero) > 2 or len(numero) < 1:
        erro('Digite um número de 1 a 2 digitos. Tente novamente.')
        return False
    elif search('[^1-9|10]', numero):
        erro('Digite um número de 1 a 10. Tente novamente.')
        return False
    else:
        return True


def painel_final(jogadores: dict, jogador_ativo: str, palavras_mascaradas_final: str, tema: str) -> None:
    """Mostra os dados para o jogador.

    Args:
        jogadores: Lista de dados dos jogadores.
        jogador_ativo: nome do jogador ativo.
        palavras_mascaradas_final: a máscara da palavra final.
        tema: o nome do tema ativo.
    """
    painel_separacao()
    msg_cor("RODADA FINAL", 37)
    painel_separacao()

    msg_cor(f"Jogador ativo:\033[m \033[1;35;40m{jogador_ativo}\033[m", 37)
    msg_cor(f"Pontuação atual: \033[1;33;40m{jogadores[jogador_ativo]}\033[m", 37)
    msg_cor(f"Nova pontuação:\033[m \033[1;32;40m{jogadores[jogador_ativo] * 2}\033[m", 37)

    painel_separacao()
    msg_cor(f"Tema:\033[m \033[1;{randint(30, 37)};40m{tema}\033[m", 37)

    painel_separacao()
    msg_cor(f"Palavra Final: {palavras_mascaradas_final}", 37)
    painel_separacao()


def pedir_letras() -> str:
    """Pede 5 consoantes e 1 vogal para serem reveladas na máscara.

    Returns:
        Retorna uma string com a escolha do jogador. 
    """
    while True:
        letras = input('Digite 5 consoantes e 1 vogal sem utilizar espaço ou qualquer separação: ')

        if not validar_letras(letras):
            continue
        return letras


def validar_letras(letras: str) -> bool:
    """ Valida as escolhas do jogador sobre as letras da palavra final.

    Args:
        letras: letras que vão ser validadas.
    Returns:
        Retorna se as letras são válidas. 
    """
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


def substituir_letras_mascarada_final(letras: str, palavras_mascaradas_final: str, palavra_final: str) -> list:
    """Substitui a letra na máscara.

    Args:
        letras: as letras que vão ser substituídas.
        palavras_mascaradas_final: a máscaras da palavra final.
        palavras: a palavra final.
    Returns:
        A máscara atualizada com as letras novas.
    """
    palavra_sem_acento = sem_acento(palavra_final)

    for i in range(len(letras)):
        matchs = finditer(letras[i], palavra_sem_acento, flags=IGNORECASE)
        pos = [match.span()[0] for match in matchs]

        for j in pos:
            palavras_mascaradas_final = palavras_mascaradas_final[:j] + palavra_final[j].upper() + palavras_mascaradas_final[j + 1:]

    return palavras_mascaradas_final


def dizer_palavra_final(jogadores: dict, jogador_ativo: str, palavra_final: str) -> bool:
    """Pergunta a palavra final ao jogador.

    Args:
        jogadores: o dicionário com os dados dos jogadores.
        jogador_ativo: o nome do jogador ativo.
        palavra_final: a palavra final da rodada.
    Returns:
        Retorna se o jogador acertou a palavra final.
    """
    palavra = sem_acento(input(f"Valendo {jogadores[jogador_ativo] * 2} reais, digite a palavra: "))

    if palavra.upper() == sem_acento(palavra_final).upper():
        return True
    return False


if __name__ == "__main__":
    main()

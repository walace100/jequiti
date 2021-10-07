from random import randint, sample, shuffle
from re import sub, search, findall, IGNORECASE


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

    # Armazena a palavra para a rodada final.
    palavra_final = ''
    # Armazena a máscara da palavra da rodada final.
    palavras_mascaradas_final = ''


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
        tema = definir_tema(base_de_dados)

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

            painel(valor_rodada, valor_turno, valor_roleta, jogadores, jogador_ativo, tema, palavras_mascaradas, letras_usadas)

            if not isinstance(valor_roleta, int):
                valor_roleta(jogadores, jogador_ativo)
                continue

            if falta_letras() != 0:
                letra = pergunta(valor_roleta, letras_usadas)

                letras_usadas = adicionar_letra_usada(letra, letras_usadas)
                #substituir_letras_mascarada


def definir_tema(base: dict) -> str:
    """Retorna um tema de uma base de dados.

    Ele escolhe um índice de 0 a 9 para escolher o tema de uma base de dados vinda por parâmetros.

    Args:
        base: um dicionário que como chave será o tema retornado.
    Returns:
        Retorna uma string com o nome do tema
    """
    return pegar_nome_por_numero(base, randint(0, 9))


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
    valores.extend([passa_vez, perdeu_tudo])
    return sample(valores, k=1)


def passa_vez(jogadores: dict, jogador_ativo) -> str:
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


def perdeu_tudo(jogadores, jogador_ativo):
    """O jogador ativo perde toda a sua pontuação e passa a vez.

    Args:
        jogadores: um dicionário com os dados dos jogadores.
        jogador_ativo: uma string com o nome do jogador ativo.
    Returns:
        Retorna o nome do próximo jogador.
    """
    jogadores[jogador_ativo] = 0
    return passa_vez(jogadores, jogador_ativo)


def painel(valor_rodada: int, valor_turno: int, valor_roleta: int, jogadores: dict, jogador_ativo: str, tema: str, palavras_mascaradas: list, letras_usadas: list) -> None:
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
    painel_separacao()
    msg_cor(f"RODADA {valor_rodada} - TURNO {valor_turno}", 37)
    painel_separacao()

    for i in range(len(jogadores.keys())):
        msg_cor(f"| {pegar_nome_por_numero(jogadores, i)} - {pegar_valor_por_numero(jogadores, i)}", 35, end=" ")

    print("")
    painel_separacao()

    msg_cor(f"Jogador ativo:\033[m \033[1;35;40m{jogador_ativo}\033[m", 37)
    msg_cor(f"Pontuação atual: \033[1;33;40m{jogadores[jogador_ativo]}\033[m", 37)

    if isinstance(valor_roleta, int):
        msg_cor(f"Roleta:\033[m \033[1;32;40m{valor_roleta}\033[m", 37)
        msg_cor(f"Nova pontuação:\033[m \033[1;32;40m{jogadores[jogador_ativo] + valor_roleta}\033[m", 37)
    elif valor_roleta.__name__ == 'passa_vez':
        msg_cor(f"Roleta:\033[m \033[1;31;40mPASSOU A VEZ!!!\033[m")
        msg_cor(f"Nova pontuação:\033[m \033[1;37;40m{jogadores[jogador_ativo]}\033[m")
    else:
        msg_cor(f"Roleta:\033[m \033[1;31;40mPERDEU TUDO!!!\033[m")
        msg_cor(f"Nova pontuação:\033[m \033[1;37;40m0\033[m")

    painel_separacao()

    msg_cor(f"\033[1;37;40mTema:\033[m \033[1;{randint(30, 37)};40m{tema}\033[m", 37)
    painel_separacao()

    msg_cor(f"P1) {palavras_mascaradas[0]}", 31)
    msg_cor(f"P1) {palavras_mascaradas[1]}", 33)
    msg_cor(f"P1) {palavras_mascaradas[2]}", 32)
    msg_cor(f"Letras já faladas:\033[m \033[1;{randint(30, 37)};40m{'Nenhuma' if len(letras_usadas) == 0 else str.join(', ', letras_usadas)}\033[m", 37)
    painel_separacao()


def painel_separacao() -> None:
    """Mostra na tela uma linha de separação."""
    print(f"\033[4;31m+{'=' * 48}\033[m", sep='')


def msg_cor(msg: str, cor: int, **kwargs) -> None:
    """Mostra na tela uma mensagem com uma cor personalizada.

    Args:
        msg: uma string com a mensagem.
        cor: um inteiro contendo o número da cor.
    """
    print(f"\033[1;{cor};40m{msg}\033[m", **kwargs)


def erro(msg) -> None:
    """Mostra uma mensagem de erro.

    Args:
        msg: mensagem a ser exibida.
    """
    print(f"\033[1;31;40m{msg}\033[m")


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
    letras_usadas.append(letra)
    return letras_usadas


if __name__ == "__main__":
    print(adicionar_letra_usada('a', []))
    # main()
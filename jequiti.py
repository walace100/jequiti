base_de_dados = {
    'merda': [
        'bosta',
        'pinto',
        'merda',
        'mijo'
    ],
    'cozinha': [
        'colher',
        'panela',
        'geladeira'
    ]
}

jogadores = {'Ana': 0, 'Bárbara': 0, 'Carlos': 0}
jogador_ativo = 'Ana'
roleta = 0
tema = ''
palavras = []
letras_erradas = []
rodada = 0
turno = 0

def painel():
    print('+', '=' * 48, sep='')
    print('RODADA {} - TURNO {}'.format(rodada, turno))
    print('+', '=' * 48, sep='')

    for i in range(len(jogadores.keys())):
        print('|', '{} - {}'.format(pegar_nome_jogadores(i), pegar_pontuacao_jogador(i)), end=' ')

    print('')
    print('+', '=' * 48, sep='')
    print('Jogador ativo: '.format(jogador_ativo))
    print('Pontuação atual: '.format(jogadores[jogador_ativo]))
    print('Roleta: '.format(roleta))
    print('Nova pontuação: '.format(jogadores[jogador_ativo]))
    print('+', '=' * 48, sep='')
    print('Tema: '.format(tema))
    print('+', '=' * 48, sep='')

def pegar_nome_jogadores(i):
    return list(jogadores.keys())[i]

def pegar_pontuacao_jogador(i):
    return jogadores[pegar_nome_jogadores(i)]

painel()
#Código de Irina Cojocari (IST1117890) irina.b.cojocari@tecnico.ulisboa.pt

"""constantes"""
LETRAS = {'A':1, 'B':3, 'C':2, 'Ç':3, 'D':2, 'E':1, 'F':4, 'G':4,
          'H':4, 'I':1, 'J':5, 'L':2,'M': 1, 'N':3, 'O':1, 'P':2,
          'Q':6, 'R':1, 'S':1, 'T':1, 'U':1, 'V':4, 'X':8, 'Z':8}

SACO = {'A':14, 'B':3, 'C':4, 'Ç':2, 'D':5, 'E':11, 'F':2, 'G':2,
        'H':2, 'I':10, 'J':2, 'L':5, 'M': 6, 'N':4, 'O':10, 'P':4,
        'Q':1, 'R':6, 'S':8, 'T':5, 'U':7, 'V':2, 'X':1, 'Z':1}

ALTURA = 15
LARGURA = 15
CENTRO = (8, 8)
MAX_JOG = 4
MAX_LETRAS_INIT = 7
NIVEIS = {'FACIL', 'MEDIO', 'DIFICIL'}
HORIZONTAL = 'H'
VERTICAL = 'V'


def c_cedilha(letra): 
    """Chave para garantir que, na ordem alfabética,
    o Ç fica entre o C e o D e não no final."""
    if letra == 'Ç':
        return ord('C') + 0.5  
    return ord(letra)

def expande_conjunto(conjunto):
    """Arg -> dict = {letra : ocorrencia}    Return -> [letra, letra,...]"""
    expandido = []
    for key in conjunto:
        adicionada = 0
        while adicionada < conjunto[key]:
            expandido.append(key)
            adicionada += 1
    return expandido

def obtem_direcao(casa1, casa2):
    """Arg -> casa, casa        Returns -> str"""
    if obtem_lin(casa1) == obtem_lin(casa2):
        return HORIZONTAL
    elif obtem_col(casa1) == obtem_col(casa2):  
        return VERTICAL
    else:
        return 'I' #de inválido
    
#----------------------------------------------------------------------------
""" 
TAD casa 
Representação: (linha, coluna) - tuplo de dois inteiros

Construtores:
   cria_casa: int x int -> casa

Seletores:
   obtem_lin: casa -> int
   obtem_col: casa -> int

Reconhecedor:
   eh_casa: universal -> bool

Teste:
   casas_iguais: casa x casa -> bool

Transformadores(saída e entrada, respetivamente):
   casa_para_str: casa -> str
   str_para_casa: str -> casa
"""
#construtor
def cria_casa(linha, coluna):
    """Arg -> int, int   Returns -> casa"""
    if type(linha) != int or type(coluna) != int or \
       not(0 < linha <= ALTURA) or not (0 < coluna <= LARGURA):
        raise ValueError('cria_casa: argumentos inválidos')
    else:
        return (linha, coluna)

#seletores
def obtem_lin(casa):
    """Arg -> Casa   Returns -> int"""
    if eh_casa(casa):
        return casa[0]

def obtem_col(casa):
    """Arg -> Casa  Returns -> int"""
    if eh_casa(casa):
        return casa[1]

#reconhecedor
def eh_casa(c):
    """Arg -> Casa  Returns -> bool""" #2 = max coordenadas, já que o tabuleiro é 2D
    if type(c)!= tuple or len(c) !=2 or \
    type(c[0]) != int or type(c[1]) != int or \
    not(0 < c[0] <= ALTURA) or not (0 < c[1] <= LARGURA):
        return False
    else:
        return True

#teste
def casas_iguais(casa1, casa2):
    """Arg -> casa, casa     Returns -> bool"""
    if eh_casa(casa1) and eh_casa(casa2) and \
     obtem_lin(casa1) == obtem_lin(casa2) and \
     obtem_col(casa1)==obtem_col(casa2):
        return True
    else: 
        return False

#transformadores
def casa_para_str(casa):
    """Arg -> casa      Returns -> str"""
    if eh_casa(casa):
        return f'({obtem_lin(casa)},{obtem_col(casa)})'

def str_para_casa(string):
    "Arg -> str     Returns -> casa"
    string.strip()
    string=(string[1: (len(string)-1)]).split(',') #tirar os parenteses

    return cria_casa(int(string[0]), int(string[1]))

#funcoes de alto nivel
def incrementa_casa(casa, direcao, distancia):
    """
    Aumenta uma das coordenadas de uma dada casa.
    Arg -> casa, direcao, distancia
    Returns -> casa (atualizada)
    """
    if direcao == HORIZONTAL and 0 < (obtem_col(casa) + distancia) <= LARGURA:
        return cria_casa(obtem_lin(casa), obtem_col(casa)  + distancia)
    
    elif direcao == VERTICAL and 0 < (obtem_lin(casa) + distancia) <= ALTURA:
        return cria_casa(obtem_lin(casa)  + distancia, obtem_col(casa))
    
    else:
        return casa

#----------------------------------------------------------------------------
"""
TAD jogador
Representação: dicionário {'id': str, 'pontos': int, 'letras': str, 'agente': bool}

Construtores:
   cria_humano: str -> jogador
   cria_agente: str -> jogador

Seletores:
   jogador_identidade: jogador -> str
   jogador_pontos: jogador -> int  
   jogador_letras: jogador -> str

Modificadores:
   recebe_letra: jogador x str -> jogador
   usa_letra: jogador x str -> jogador
   soma_pontos: jogador x int -> jogador

Reconhecedores:
   eh_jogador: universal -> bool
   eh_humano: universal -> bool
   eh_agente: universal -> bool

Teste:
   jogadores_iguais: jogador x jogador -> bool

Transformador(saída):
   jogador_para_str: jogador -> str
"""

#construtores
def cria_humano(nome):
    """Arg -> str
    Returns -> dict = {id: id, pontos: pontos, letras: letras, agente: bool}"""
    if type(nome) != str or len(nome) == 0:
        raise ValueError('cria_humano: argumento inválido')
    else:
        return {'id': nome, 'pontos': 0, 'letras': '', 'agente':False}
    
def cria_agente(nivel):
    """Arg -> str
    Returns -> dict = {id: id, pontos: pontos, letras: letras, agente: bool}"""
    if type(nivel) != str or nivel not in NIVEIS:
        raise ValueError('cria_agente: argumento inválido')
    else:
        return {'id': f'{nivel}', 'pontos': 0, 'letras': '', 'agente': True}

#seletores
def jogador_identidade(jogador):
    """Arg -> jogador    Returns -> str"""
    return jogador['id']

def jogador_pontos(jogador):
    """Arg -> jogador    Returns -> int"""
    return jogador['pontos']

def jogador_letras(jogador):
    """Arg -> jogador    Returns -> sorted list"""
    return ''.join(sorted(jogador['letras'], key = c_cedilha))

#modificadores
def recebe_letra(jogador, letra):
    """Arg -> jogador, str    Returns -> jogador"""
    jogador['letras'] = jogador['letras'] + letra
    return jogador

def usa_letra(jogador, letra):
    """Arg -> jogador, str    Returns -> jogador"""
    jogador['letras'] = jogador['letras'].replace(letra, '', 1)
    return jogador

def soma_pontos(jogador, pontos):
    """Arg -> jogador, int    Returns -> jogador"""
    jogador['pontos'] = jogador['pontos'] + pontos
    return jogador

#reconhecedores
def eh_jogador(arg):
    """Arg -> universal     Returns -> bool"""
    return (type(arg) == dict and set(arg.keys()) == {'id', 'pontos', 'letras', 'agente'})

def eh_humano(jogador):
    """Arg -> jogador    Returns -> bool"""
    return eh_jogador(jogador) and not jogador['agente']
    
def eh_agente(jogador):
    """Arg -> jogador    Returns -> bool"""
    return eh_jogador(jogador) and jogador['agente']

#teste
def jogadores_iguais(jog1, jog2):
    """Arg -> jogador, jogador   Returns -> bool"""
    return ((eh_humano(jog1) and eh_humano(jog2)) or \
            (eh_agente(jog1) and eh_agente(jog2))) and \
           jogador_identidade(jog1) == jogador_identidade(jog2) and\
           jogador_pontos(jog1) == jogador_pontos(jog2) and \
            jogador_letras(jog1) == jogador_letras(jog2) 

#transformador
def jogador_para_str(jogador):
    """Arg -> jogador    Returns -> str"""
    letras_display = jogador_letras(jogador)
    if letras_display:
        letras_str = ' ' + ' '.join(letras_display)
    else:
        letras_str = ''
    if eh_agente(jogador):
        return (f'BOT({jogador_identidade(jogador)}) ({str(jogador_pontos(jogador)):>3}):{letras_str}')
    if eh_humano(jogador):
        return (f'{jogador_identidade(jogador)} ({str(jogador_pontos(jogador)):>3}):{letras_str}') 

#funcoes de alto nivel
def distribui_letras(jogador, letras, num): 
    """
    Dá num letras de uma pilha a um jogador.
    Arg -> jogador, str, int    
    Returns -> jogador
    """
    for i in range(num):
        if len(letras) > 0:
            recebe_letra(jogador, letras.pop())

    return jogador

#----------------------------------------------------------------------------
"""
TAD vocabulario

Representação: dicionário {comprimento: {letra_inicial: {palavra: pontos}}}

Construtor:
   cria_vocabulario: tuple -> vocabulario

Seletores:
   obtem_pontos: vocabulario x str -> int
   obtem_palavras: vocabulario x int x str -> tuple

Teste:
   testa_palavra_padrao: vocabulario x str x str x str -> bool

Transformadores(entrada e saída, respetivamente):
   ficheiro_para_vocabulario: str -> vocabulario
   vocabulario_para_str: vocabulario -> str
"""

#construtor
def cria_vocabulario(v):
    """
    Organiza as palavras de um tuplo num dicionário do tipo:
    vocabulario = {comprimento: {inicial: {palavra : pontos}}}

    Arg -> tuple  

    Returns -> vocabulário
    """
    if type(v) != tuple or len(v) != len(set(v)) or len(v) < 1:
        raise ValueError('cria_vocabulario: argumento inválido')
    vocabulario = {}
    for palavra in v:
        if type(palavra) != str or \
        not all(letra in LETRAS.keys() for letra in palavra):
            raise ValueError('cria_vocabulario: argumento inválido')
        if len(palavra) < 2 or len(palavra) > 15:
            raise ValueError('cria_vocabulario: argumento inválido')
    
        comprimento, inicial, pontos = len(palavra), palavra[0], 0
        if comprimento not in vocabulario:
            vocabulario[comprimento]={}
        if inicial not in vocabulario[comprimento]:
            vocabulario[comprimento][inicial]={}
        
        for i in range(comprimento):
            pontos += LETRAS[palavra[i]]
        vocabulario[comprimento][inicial][palavra] = pontos            
    return vocabulario

#seletores
def obtem_pontos(vocabulario, palavra):
    """Arg -> vocabulario, str      Returns -> int"""
    if len(palavra) in vocabulario and \
    palavra[0] in vocabulario[len(palavra)] and \
    palavra in vocabulario[len(palavra)][palavra[0]]:
        
        return vocabulario[len(palavra)][palavra[0]][palavra]
    
    else:
        return 0

def obtem_palavras(vocabulario, comprimento, letra):
    """Arg -> Vocabulario, int, letra       Returns -> ((palavra, pontos), (palavra, pontos),...)"""
    if comprimento not in vocabulario or letra not in vocabulario[comprimento]:
        return ()
    
    palavra_pontos = []
    for palavra in vocabulario[comprimento][letra]:
        palavra_pontos.append((palavra, obtem_pontos(vocabulario, palavra)))

    for i in range(comprimento-1,-1,-1): #ordenar por ordem alfabetica, da ultima para a primeira letra
        palavra_pontos.sort(key = lambda x: c_cedilha(x[0][i]) if len(x[0]) > i else 0) 
    palavra_pontos.sort(key = lambda x: -x[1]) #dentro das com os mesmos pontos, ficam por ordem alfabetica
        
    return tuple(palavra_pontos)

#teste
def testa_palavra_padrao(vocabulario, palavra, padrao, letras):
    """
    Averigua se é possivel formar uma palavra que encaixe no padrao com as letras disponiveis

    Arg -> vocabulario, palavra(str), padrao(str), letras(str)

    Returns -> bool
    """    
    if len(palavra) not in vocabulario or palavra[0] not in vocabulario[len(palavra)]\
     or palavra not in vocabulario[len(palavra)][palavra[0]]:
        return False
   
    letras_disponiveis = letras
    possibilidade = ''

    if len(padrao) != len(palavra):
        return False
    if '.' not in padrao: #padrao ja preenchido
        return False
    
    for i in range(len(padrao)):
        if padrao[i] == '.' and palavra[i] in letras_disponiveis:
           letras_disponiveis= letras_disponiveis.replace(palavra[i], '', 1)
           possibilidade += palavra[i]
        elif padrao[i] != '.' and padrao[i] == palavra[i]:
            possibilidade += palavra[i]
        elif padrao[i] == '.' and palavra[i] not in letras_disponiveis:
            return False
    
    return possibilidade == palavra  

#transformadores de entrada e saída, respetivamente
def ficheiro_para_vocabulario(nome_fich):
    """
    'Descodifica' um ficheiro, transformando-o num vocabulário

    Arg -> nome do ficheiro (str)

    Returns -> vocabulario
    """
    with open(nome_fich, 'r', encoding = 'utf-8') as f:
        vocab = set() #tirar palavras repetidas
        for palavra in f.readlines():
            palavra = palavra.strip().upper()
            if 2<= len(palavra) <= 15 and all(letra in LETRAS.keys() for letra in palavra):
               vocab.add(palavra)

        return cria_vocabulario(tuple(vocab)) 

def vocabulario_para_str(vocabulario):
    """Arg -> vocabulario      Returns -> str"""
    if type(vocabulario) == tuple:
        vocabulario = cria_vocabulario(vocabulario)

    vocabulario_str=[]
    for length in sorted(vocabulario):
        for letra in sorted(vocabulario[length], key = c_cedilha):
            vocabulario_str += [word[0] for word in obtem_palavras(vocabulario, length, letra)]

    return'\n'.join(vocabulario_str)
    
#funcoes alto nivel
def procura_palavra_padrao(vocabulario, padrao, letras, min_pontos):
    """
    Procura, entre as palavras que podem preencher um certo padrao, as que
    garantem um certo numero de pontos e podem ser formadas com as letras disponiveis,
    ordenando as por ordem de maior numero de pontos

    Arg -> vocabulario, str, str, int

    Returns -> [palavra, palavra, ...]
    """
    opcoes=[]

    if padrao[0] != '.':
        palavras_pontos = obtem_palavras(vocabulario, len(padrao), padrao[0])
        if len(palavras_pontos) != 0:
            for palavra in palavras_pontos:
                if testa_palavra_padrao(vocabulario, palavra[0], padrao, letras)\
                and palavra[1] >= min_pontos:
                    opcoes.append(palavra)

    elif padrao[0] == '.':
        for letra in letras:
            palavras_pontos = obtem_palavras(vocabulario, len(padrao), letra)
            if len(palavras_pontos) != 0 :
                for palavra in palavras_pontos:
                    if testa_palavra_padrao(vocabulario, palavra[0], padrao, letras)\
                     and palavra[1] >= min_pontos:
                        opcoes.append(palavra)

    if len(opcoes) == 0:
        return ('',0)
    
    for i in range(len(padrao)-1,-1,-1): #ordenacao semelhante à da funcao obtem_palavras
        opcoes.sort(key = lambda x: c_cedilha(x[0][i]) if len(x[0]) > i else 0)
    opcoes.sort(key = lambda x: -x[1])
    return opcoes[0]


#----------------------------------------------------------------------------
"""
TAD tabuleiro
  
Representação: lista de listas de strings (matriz 15x15)

Construtor:
   cria_tabuleiro: {} -> tabuleiro

Seletores:
   obtem_letra: tabuleiro x casa -> str

Modificadores:
   insere_letra: tabuleiro x casa x str -> tabuleiro

Reconhecedores:
   eh_tabuleiro: universal -> bool
   eh_tabuleiro_vazio: universal -> bool

Teste:
   tabuleiros_iguais: tabuleiro x tabuleiro -> bool

Transformador (saída):
   tabuleiro_para_str: tabuleiro -> str
"""

#construtor
def cria_tabuleiro():
    """Returns -> tabuleiro"""
    tabuleiro = []
    for i in range(ALTURA):
        linha = ['.' for j in range(LARGURA)]
        tabuleiro.append(linha)
    return tabuleiro

#seletor
def obtem_letra(tabuleiro, casa):
    """Arg -> tabuleiro, casa       Returns -> str"""
    letra = tabuleiro[obtem_lin(casa) - 1][obtem_col(casa)- 1] # 1 - 15 -> 0 - 14
    return letra

#modificador
def insere_letra(tabuleiro, casa, letra):
    """Arg -> tabuleiro, casa, str      Returns -> tabuleiro (atualizado)"""
    tabuleiro[obtem_lin(casa) - 1][obtem_col(casa) - 1] = letra
    return tabuleiro

#reconhecedor
def eh_tabuleiro(arg):
    """Arg -> tabuleiro     Returns -> bool"""
    if type(arg) != list or len(arg) != ALTURA:
        return False
    
    for i in range(len(arg)):
        if type(arg[i]) != list or len(arg[i]) != LARGURA:
            return False
        for j in range(len(arg[i])):
            if type(obtem_letra(arg, cria_casa(i+1, j+1))) != str:
                return False
            
    return True

def eh_tabuleiro_vazio(arg):
    """Arg -> tabuleiro     Returns -> bool"""
    if eh_tabuleiro(arg):
        for i in range(len(arg)):
            for j in range(len(arg[i])):
                if obtem_letra(arg, cria_casa(i+1, j+1)) != '.':
                    return False
    
    else: 
        return False 
    
    return True
    
#teste
def tabuleiros_iguais(t1, t2):
    """Arg -> tabuleiro, tabuleiro     Returns -> bool"""
    if eh_tabuleiro(t1) and eh_tabuleiro(t2):
        for i in range(len(t1)):
            for j in range(len(t1[i])):
                if obtem_letra(t1, cria_casa(i+1, j+1)) !=  obtem_letra(t2, cria_casa(i+1, j+1)):
                    return False
    else:
        return False
    return True

#transformador
def tabuleiro_para_str(tabuleiro):
    """Arg -> tabuleiro     Returns -> str"""
    tabuleiro_str = (f'{"1 1 1 1 1 1":>34}\n'
                    f'{"1 2 3 4 5 6 7 8 9 0 1 2 3 4 5":>34}\n'
                    f'{"+-------------------------------+":>36}')
    
    linha = 0
    for i in range(ALTURA):
        tabuleiro_str += f'\n{str(i+1):>2} |'
        for c in tabuleiro[linha]:
            tabuleiro_str += f'{c:>2}'
        tabuleiro_str += ' |'
        linha += 1
    
    tabuleiro_str += f'\n{"+-------------------------------+":>36}'
    
    return tabuleiro_str

#funcoes alto nivel
def obtem_padrao(tabuleiro, inicio, fim):
    """
    Obtem a sequência de caracteres de uma porção do tabuleiro.

    Arg -> tabuleiro, casa, casas
    Returns -> padrao(str)
    """
    padrao=''
    direcao = obtem_direcao(inicio, fim)

    if direcao == VERTICAL:
        while obtem_lin(inicio) <= obtem_lin(fim):        
            padrao += obtem_letra(tabuleiro, inicio)
            novo_inicio = incrementa_casa(inicio, direcao, 1)
            if novo_inicio == inicio:
                break
            inicio = novo_inicio

    elif direcao == HORIZONTAL:
        while obtem_col(inicio) <= obtem_col(fim):
            padrao += obtem_letra(tabuleiro, inicio)
            novo_inicio = incrementa_casa(inicio, direcao, 1)
            if novo_inicio == inicio:
                break
            inicio = novo_inicio

    return padrao

def insere_palavra(tabuleiro, casa, direcao, palavra):
    """
    Altera os caracteres de uma porção do tabuleiro.

    Arg -> tabuleiro, casa, str, str     
    
    Returns -> Tabuleiro(atualizado)
    """
    for letra in palavra:
        insere_letra(tabuleiro, casa, letra)
        casa=incrementa_casa(casa, direcao, 1)

    return tabuleiro

def obtem_subpadroes(tabuleiro, inicio, fim, length):
    """
    Obtem todos os subpadrões contidos entre inicio e fim, que tenham no máximo length espaços livres ('.').

    Arg -> tabuleiro, casa, casa, int

    Returns -> (subpadrao, subpadrao,...), (casa_inicio, casa_inicio,...)
    """
    subpadroes = ()
    inicios = ()
    padrao = obtem_padrao(tabuleiro, inicio, fim)
    
    for i in range (len(padrao)-1):
        for j in range(len(padrao), i, -1):
            if (not all(c == '.' for c in padrao[i : j])) and\
            (not all(c != '.' for c in padrao[i : j])) and\
            (padrao[i : j].count('.') <= length) and\
            not (i > 0 and padrao[i-1] != '.') and\
            not (j < len(padrao) and padrao[j] != '.'):
                subpadroes += (padrao[i : j], )
                inicios += ((incrementa_casa(inicio, obtem_direcao(inicio, fim), i)), )
    return subpadroes, inicios

def gera_todos_padroes(tabuleiro, length):
    """
    Gera todos os padrões possíveis de um tabuleiro que tenham até
    length espaços livres ('.').

    Arg -> tabuleiro, length

    Returns -> ((padrao, padrao, ...), (inicio, inicio, ...), (direcao, direcao, ...))
    """
    padroes_tuplo = ()
    inicio_tuplo = ()
    direcoes_tuplo = ()
    
    for i in range(1, ALTURA+1):
        subpadroes_horizontal = obtem_subpadroes(tabuleiro, cria_casa(i, 1), cria_casa(i, LARGURA), length)
        padroes_tuplo += subpadroes_horizontal[0]
        inicio_tuplo += subpadroes_horizontal[1]
        direcoes_tuplo += (HORIZONTAL, ) * len(subpadroes_horizontal[0])
    
    for j in range(1, LARGURA+1):
        subpadroes_vertical = obtem_subpadroes(tabuleiro, cria_casa(1, j), cria_casa(ALTURA, j), length)
        padroes_tuplo += subpadroes_vertical[0]
        inicio_tuplo += subpadroes_vertical[1]
        direcoes_tuplo += (VERTICAL, ) * len(subpadroes_vertical[0])

    return padroes_tuplo, inicio_tuplo, direcoes_tuplo


#----------------------------------------------------------------------------
"""Funções adicionais"""

def baralha_saco(seed):
    """"
    Dada uma determinada seed, baralha o saco (cujas letras são constantes) de forma pseudoaleatoria.

    Arg -> Seed

    Returns -> Saco baralhado (lst)
    """
    def gera_numero_aleatorio(estado):
        """Recebe o estado do gerador (int) e devolve um número pseudoaleatório."""
        estado ^= ( estado << 13 ) & 0xFFFFFFFF
        estado ^= ( estado >> 17 ) & 0xFFFFFFFF
        estado ^= ( estado << 5 ) & 0xFFFFFFFF
        return estado

    def permuta_letras(letras, estado):
        """Baralha uma lista, de forma pseudoaleatória."""
        j = (gera_numero_aleatorio(estado))
        for i in range(len(letras)-1, 0, -1): 
            letras[(j) % (i + 1)], letras[i] = letras[i], letras[(j) % (i + 1)]
            j = gera_numero_aleatorio(j)

    letras = sorted(expande_conjunto(SACO), key = c_cedilha)
    permuta_letras(letras, seed) 
    return letras


def jogada_humano(tabuleiro, jogador, vocabulario, pilha):
    """
    Recebe, valida e processa o input de um jogador humano. O jogador pode passar a vez, 
    trocar letras ou jogar uma palavra.

    Args -> tabuleiro, jogador, vocabulario, saco(func anterior)

    Returns -> bool    
    """
    inputvalido = False
    while not inputvalido:
        acao = input(f'Jogada {jogador_identidade(jogador)}: ').split()

        if len(acao) == 0: #Se estiver em branco/for só espaços
            continue

        if acao[0] == 'T' and len(pilha) >= 7: 
            letras = acao[1:] #Tirar o T, porque já foi avaliado
            if len(letras) < 1: #Se não tiver fornecido nenhuma letra
                continue

            char_invalido = False
            letras_jogador = jogador_letras(jogador)
            for letra in letras:
                if letra not in LETRAS  or letras.count(letra) > letras_jogador.count(letra):
                    char_invalido = True
                    break
            if char_invalido:
                continue

            for letra in letras: #Se passar nas condições todas
                usa_letra(jogador, letra) 
            distribui_letras(jogador, pilha, len(letras)) 
            return True
        
        elif acao[0] == 'J':
            acao = acao[1:]
            if len(acao) < 4: #Tira o J e vê se forneceu as duas coordenadas, a direção e um conjunto de letras
                continue

            #se a casa fornecida não for válida, volta a pedir uma jogada, em vez de crashar o programa
            if not eh_casa(cria_casa((int(acao[0])), (int(acao[1])))):
                continue
            try: 
                inicio, direcao, palavra = cria_casa((int(acao[0])), (int(acao[1]))), acao[2], acao[3]
            except ValueError:
                continue
            if direcao == HORIZONTAL:
                try:
                     fim = cria_casa(obtem_lin(inicio), obtem_col(inicio) + len(palavra)-1)
                except ValueError:
                    continue
            elif direcao == VERTICAL:
                try:
                    fim = cria_casa(obtem_lin(inicio) + len(palavra) -1, obtem_col(inicio))
                except ValueError:
                    continue

            padrao = obtem_padrao(tabuleiro, inicio, fim)
            
            if eh_tabuleiro_vazio(tabuleiro) and testa_palavra_padrao(vocabulario, palavra, padrao, jogador_letras(jogador)):
                insere_palavra(tabuleiro, inicio, direcao, palavra)

                if obtem_letra(tabuleiro, cria_casa(CENTRO[0], CENTRO[1])) == '.':
                    insere_palavra(tabuleiro, inicio, direcao, padrao) #volta a inserir o padrao para "apagar" a palavra

                else:
                    soma_pontos(jogador, obtem_pontos(vocabulario, palavra))
                    adicionar = 0
                    for i in range(len(palavra)):
                        if padrao[i] == '.':
                            usa_letra(jogador, palavra[i])
                            adicionar += 1
                    distribui_letras(jogador, pilha, adicionar)
                    return True
                   
            
            elif (not eh_tabuleiro_vazio(tabuleiro)) and padrao.count('.') != len(padrao) and\
            testa_palavra_padrao(vocabulario, palavra, padrao, jogador_letras(jogador)) and\
            (obtem_letra(tabuleiro, incrementa_casa(inicio, direcao, -1)) == '.') and \
            (obtem_letra(tabuleiro, incrementa_casa(fim, direcao, 1)) == '.'):
        
                insere_palavra(tabuleiro, inicio, direcao, palavra)
                soma_pontos(jogador, obtem_pontos(vocabulario, palavra))
                adicionar = 0
                for i in range(len(palavra)):
                    if padrao[i] == '.':
                        usa_letra(jogador, palavra[i])
                        adicionar += 1
                distribui_letras(jogador, pilha, adicionar)
                return True
                
        elif acao[0] == 'P':
            return False


def jogada_agente(tabuleiro, jogador, vocabulario, pilha):
    """
    Gera todos os padrões possíveis do tabuleiro de forma a averiguar se é possível que o agente jogue.
    Procura as melhores palavras para jogar, de acordo com o nível do agente e as letras que tem.
    Troca todas as letras ou passa a vez se não conseguir jogar.

    Args -> tabuleiro, jogador, vocabulario, pilha(lst)

    Returns -> bool
    """

    #agentes nunca são os primeiros a jogar
    if eh_tabuleiro_vazio(tabuleiro):
        print(f'Jogada {jogador_identidade(jogador)}: P')
        return False
    
    padroes, inicios, direcoes = gera_todos_padroes(tabuleiro, len(jogador_letras(jogador)))
    if len(padroes) != 0: #cada nivel de agente avalia sucessivamente mais padroes, procurando o melhor
        if jogador_identidade(jogador) == 'FACIL':
            n = 100
        elif jogador_identidade(jogador) == 'MEDIO':
            n = 50
        elif jogador_identidade(jogador) == 'DIFICIL':
            n = 10
        padroes, inicios, direcoes = padroes[::n], inicios[::n], direcoes[::n]

    possibilidades = []
    for i in range(len(padroes)):
        if any(c != '.' for c in padroes[i]) and any(c == '.' for c in padroes[i]):
            padrao, inicio, direcao = padroes[i], inicios[i], direcoes[i]
            resultado = procura_palavra_padrao(vocabulario, padrao, jogador_letras(jogador), 0)
            if resultado[0] != '':  
                possibilidades.append((resultado, inicio, direcao))

    possibilidades.sort(key = lambda x : x[0][1], reverse = True) #ordena as palavras por pontos
    
    if possibilidades != []: 
        melhor = possibilidades[0] 
        palavra, pontos = melhor[0]  
        inicio = melhor[1]  
        direcao = melhor[2]
        
        if direcao == HORIZONTAL:
            padrao = obtem_padrao(tabuleiro, inicio, cria_casa(obtem_lin(inicio), obtem_col(inicio) + len(palavra)-1))
        if direcao == VERTICAL:
            padrao = obtem_padrao(tabuleiro, inicio, cria_casa(obtem_lin(inicio) + len(palavra) -1, obtem_col(inicio)))
        
        #a palavra ja foi validada no procura palavra padrao
        insere_palavra(tabuleiro,  inicio, direcao, palavra)
        tirar = 0
        for i in range(len(palavra)):
            if padrao[i] == '.':
                usa_letra(jogador, palavra[i])
                tirar += 1
        distribui_letras(jogador, pilha, tirar)
        soma_pontos(jogador, pontos)
        print(f"Jogada {jogador_identidade(jogador)}: J {obtem_lin(inicio)} {obtem_col(inicio)} {direcao} {palavra}")
        return True

    #se não puder jogar e a pilha tiver letras suficientes, troca todas
    elif possibilidades == [] and len(pilha) >= MAX_LETRAS_INIT:
        print(f'Jogada {jogador_identidade(jogador)}: T {" ".join(jogador_letras(jogador))}')
        for letra in jogador_letras(jogador):
            usa_letra(jogador, letra)
        distribui_letras(jogador, pilha, MAX_LETRAS_INIT)
        return True
    
    #se nao puder jogar nem trocar, passa
    else:
        print(f'Jogada {jogador_identidade(jogador)}: P')
        return False


def scrabble2(jogadores, nome_fich, seed):
    """
    Fluxo principal do jogo. Inicializa variáveis antes do inicio do jogo, valida argumentos,
    estrutura agentes e jogadores humanos, distribui letras, determina o próximo jogador a jogar,
    gera a representação gráfica do tabuleiro e de cada jogador e calcula a pontuação dos jogadores.
    
    Arg -> (humano, humano, @agente, ...), str, int

    Returns -> tuplo (pontos de todos os jogadores)
    """
    if type(jogadores) != tuple or type(seed) != int  \
    or seed < 0 or not(1 < len(jogadores) <= MAX_JOG) \
    or type(nome_fich) != str:
        raise ValueError('scrabble2: argumentos inválidos')
    
    pilha =baralha_saco(seed)
    players = []
    tabuleiro = cria_tabuleiro()
    continuar = True
    jogador_atual = 0
    passes_consecutivos = 0 
    vocabulario = ficheiro_para_vocabulario(nome_fich)

    for jogador in jogadores: #Discriminar humanos, agentes e input invalido
        if type(jogador) == str and jogador[0] == '@' and jogador[1:] in NIVEIS:
            players.append(cria_agente(jogador[1:]))
        elif type(jogador) == str and jogador[0] == '@' and jogador[1:] not in NIVEIS:
            raise ValueError('scrabble2: argumentos inválidos')
        elif type(jogador) == str:
            players.append(cria_humano(jogador))
        else:
            raise ValueError('scrabble2: argumentos inválidos')
        
    #se não houverem letras suficientes para todos os jogadores...
    if len(pilha) < (MAX_LETRAS_INIT * len(jogadores)):
        raise ValueError("scrabble2: argumentos inválidos")
    
    for player in players:
        distribui_letras(player, pilha,  MAX_LETRAS_INIT)


    print('Bem-vindo ao SCRABBLE2.')
    while continuar: 
        
        print(tabuleiro_para_str(tabuleiro))
        for player in players:
            print(jogador_para_str(player))

        if eh_humano(players[jogador_atual]):
            resultado = jogada_humano(tabuleiro, players[jogador_atual], vocabulario, pilha)
        elif eh_agente(players[jogador_atual]): 
            resultado = jogada_agente(tabuleiro, players[jogador_atual], vocabulario, pilha)
        
        #se todos passarem ou alguem estiver sem letras e nao houverem mais letras na pilha...
        if not resultado:
            passes_consecutivos += 1
        else:
            passes_consecutivos = 0
        if passes_consecutivos >= len(players):
            continuar = False
        for player in players:
            if len(jogador_letras(players[jogador_atual])) == 0 and len(pilha) == 0:
                continuar = False  
        
        if continuar:
            jogador_atual = (jogador_atual + 1)  % len(players) 
         
    scores = tuple(jogador_pontos(player) for player in players)
    return scores


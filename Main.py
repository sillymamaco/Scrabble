import sys

#--- HELPER FUNCTIONS ---

def get_cedilla_key(char):
    """Specific sorting for Portuguese to put Ç after C"""
    if char == 'Ç':
        return ord('C') + 0.5
    return ord(char)

def get_standard_key(char):
    """Standard sorting for English/French"""
    return ord(char)

#--- GLOBAL SETTINGS ---

LANGUAGES = {
    'PT': {
        'LETTER_VALUES': {
            'A':1, 'B':3, 'C':2, 'Ç':3, 'D':2, 'E':1, 'F':4, 'G':4,
            'H':4, 'I':1, 'J':5, 'L':2,'M': 1, 'N':3, 'O':1, 'P':2,
            'Q':6, 'R':1, 'S':1, 'T':1, 'U':1, 'V':4, 'X':8, 'Z':8
        },
        'BAG_DISTRIBUTION': {
            'A':14, 'B':3, 'C':4, 'Ç':2, 'D':5, 'E':11, 'F':2, 'G':2,
            'H':2, 'I':10, 'J':2, 'L':5, 'M': 6, 'N':4, 'O':10, 'P':4,
            'Q':1, 'R':6, 'S':8, 'T':5, 'U':7, 'V':2, 'X':1, 'Z':1
        },
        'SORT_FUNC': get_cedilla_key,
        'TEXTS': {
            'welcome': 'Bem-vindo ao SCRABBLE2.',
            'play_prompt': 'Jogada {}: ', 
            'play_format': 'Jogada {}: J {} {} {} {}',
            'pass_format': 'Jogada {}: P',
            'exchange_format': 'Jogada {}: T {}',
            'invalid_args': 'argumentos inválidos',
            'board_header_1': '1 1 1 1 1 1',
            'board_header_2': '1 2 3 4 5 6 7 8 9 0 1 2 3 4 5'
        },
        'VOCABULARY_FILE': 'pt.txt'
    },
    'EN': {
        'LETTER_VALUES': {
            'A':1, 'B':3, 'C':3, 'D':2, 'E':1, 'F':4, 'G':2, 'H':4, 'I':1, 
            'J':8, 'K':5, 'L':1, 'M':3, 'N':1, 'O':1, 'P':3, 'Q':10, 'R':1, 
            'S':1, 'T':1, 'U':1, 'V':4, 'W':4, 'X':8, 'Y':4, 'Z':10
        },
        'BAG_DISTRIBUTION': {
            'A':9, 'B':2, 'C':2, 'D':4, 'E':12, 'F':2, 'G':3, 'H':2, 'I':9, 
            'J':1, 'K':1, 'L':4, 'M':2, 'N':6, 'O':8, 'P':2, 'Q':1, 'R':6, 
            'S':4, 'T':6, 'U':4, 'V':2, 'W':2, 'X':1, 'Y':2, 'Z':1
        },
        'SORT_FUNC': get_standard_key,
        'TEXTS': {
            'welcome': 'Welcome to SCRABBLE2.',
            'play_prompt': 'Turn {}: ',
            'play_format': 'Turn {}: P {} {} {} {}', 
            'pass_format': 'Turn {}: P', 
            'exchange_format': 'Turn {}: E {}', 
            'invalid_args': 'invalid arguments',
            'board_header_1': '1 1 1 1 1 1',
            'board_header_2': '1 2 3 4 5 6 7 8 9 0 1 2 3 4 5'
        },
        'VOCABULARY_FILE': 'en.txt'
    },
    'FR': {
        'LETTER_VALUES': {
            'A':1, 'B':3, 'C':3, 'D':2, 'E':1, 'F':4, 'G':2, 'H':4, 'I':1, 
            'J':8, 'K':10, 'L':1, 'M':2, 'N':1, 'O':1, 'P':3, 'Q':8, 'R':1, 
            'S':1, 'T':1, 'U':1, 'V':4, 'W':10, 'X':10, 'Y':10, 'Z':10
        },
        'BAG_DISTRIBUTION': {
            'A':9, 'B':2, 'C':2, 'D':3, 'E':15, 'F':2, 'G':2, 'H':2, 'I':8, 
            'J':1, 'K':1, 'L':5, 'M':3, 'N':6, 'O':6, 'P':2, 'Q':1, 'R':6, 
            'S':6, 'T':6, 'U':6, 'V':2, 'W':1, 'X':1, 'Y':1, 'Z':1
        },
        'SORT_FUNC': get_standard_key,
        'TEXTS': {
            'welcome': 'Bienvenue au SCRABBLE2.',
            'play_prompt': 'Tour {}: ',
            'play_format': 'Tour {}: J {} {} {} {}',
            'pass_format': 'Tour {}: P',
            'exchange_format': 'Tour {}: E {}',
            'invalid_args': 'arguments invalides',
            'board_header_1': '1 1 1 1 1 1',
            'board_header_2': '1 2 3 4 5 6 7 8 9 0 1 2 3 4 5'
        },
        'VOCABULARY_FILE': 'fr.txt'
    }
}
#--- GLOBAL SETTINGS (Initialized via select_language) ---
CURRENT_LANG = 'PT' #Default
LETTER_VALUES = {}
BAG_DISTRIBUTION = {}
TEXTS = {}
SORT_KEY = None #Function pointer

def select_language(lang_code):
    global CURRENT_LANG, LETTER_VALUES, BAG_DISTRIBUTION, TEXTS, SORT_KEY
    if lang_code not in LANGUAGES:
        raise ValueError("Language not supported")
    
    CURRENT_LANG = lang_code
    data = LANGUAGES[lang_code]
    LETTER_VALUES = data['LETTER_VALUES']
    BAG_DISTRIBUTION = data['BAG_DISTRIBUTION']
    TEXTS = data['TEXTS']
    SORT_KEY = data['SORT_FUNC']

#--- CONSTANTS ---
HEIGHT = 15
WIDTH = 15
CENTER = (8, 8)
MAX_PLAYERS = 4
MAX_LETTERS_INIT = 7
LEVELS = {'FACIL', 'MEDIO', 'DIFICIL'} 
HORIZONTAL = 'H'
VERTICAL = 'V'

def expand_set(subset):
    """Arg -> dict = {letter : occurrence}    Return -> [letter, letter,...]"""
    expanded = []
    for key in subset:
        added = 0
        while added < subset[key]:
            expanded.append(key)
            added += 1
    return expanded

def get_direction(sq1, sq2):
    """Arg -> square, square        Returns -> str"""
    if get_row(sq1) == get_row(sq2):
        return HORIZONTAL
    elif get_col(sq1) == get_col(sq2):  
        return VERTICAL
    else:
        return 'I' #I for Invalid

#----------------------------------------------------------------------------
""" 
ADT Square (Coordinate)
Representation: (row, col) - tuple of two integers
"""
#Constructor
def create_square(row, col):
    """Arg -> int, int   Returns -> square"""
    if type(row) != int or type(col) != int or \
       not(0 < row <= HEIGHT) or not (0 < col <= WIDTH):
        raise ValueError(f"create_square: {TEXTS['invalid_args']}")
    else:
        return (row, col)

#Selectors
def get_row(square):
    """Arg -> Square   Returns -> int"""
    if is_square(square):
        return square[0]

def get_col(square):
    """Arg -> Square  Returns -> int"""
    if is_square(square):
        return square[1]

#Recognizer
def is_square(c):
    """Arg -> Square  Returns -> bool""" 
    if type(c)!= tuple or len(c) !=2 or \
    type(c[0]) != int or type(c[1]) != int or \
    not(0 < c[0] <= HEIGHT) or not (0 < c[1] <= WIDTH):
        return False
    else:
        return True

#Test
def squares_equal(sq1, sq2):
    """Arg -> square, square     Returns -> bool"""
    if is_square(sq1) and is_square(sq2) and \
     get_row(sq1) == get_row(sq2) and \
     get_col(sq1)==get_col(sq2):
        return True
    else: 
        return False

#Transformers
def square_to_str(square):
    """Arg -> square      Returns -> str"""
    if is_square(square):
        return f'({get_row(square)},{get_col(square)})'

def str_to_square(string):
    "Arg -> str     Returns -> square"
    string.strip()
    string=(string[1: (len(string)-1)]).split(',') 

    return create_square(int(string[0]), int(string[1]))

#High Level Functions
def increment_square(square, direction, distance):
    """
    Increases one coordinate of a given square.
    Arg -> square, direction, distance
    Returns -> square (updated)
    """
    if direction == HORIZONTAL and 0 < (get_col(square) + distance) <= WIDTH:
        return create_square(get_row(square), get_col(square)  + distance)
    
    elif direction == VERTICAL and 0 < (get_row(square) + distance) <= HEIGHT:
        return create_square(get_row(square)  + distance, get_col(square))
    
    else:
        return square

#----------------------------------------------------------------------------
"""
ADT Player
Representation: dictionary {'id': str, 'points': int, 'letters': str, 'agent': bool}
"""

#Constructors
def create_human(name):
    """Arg -> str
    Returns -> dict"""
    if type(name) != str or len(name) == 0:
        raise ValueError(f"create_human: {TEXTS['invalid_args']}")
    else:
        return {'id': name, 'points': 0, 'letters': '', 'agent':False}
    
def create_agent(level):
    """Arg -> str
    Returns -> dict"""
    if type(level) != str or level not in LEVELS:
        raise ValueError(f"create_agent: {TEXTS['invalid_args']}")
    else:
        return {'id': f'{level}', 'points': 0, 'letters': '', 'agent': True}

#Selectors
def player_identity(player):
    """Arg -> player    Returns -> str"""
    return player['id']

def player_points(player):
    """Arg -> player    Returns -> int"""
    return player['points']

def player_letters(player):
    """Arg -> player    Returns -> sorted list"""
    #Uses the dynamic SORT_KEY from the language file
    return ''.join(sorted(player['letters'], key = SORT_KEY))

#Modifiers
def receive_letter(player, letter):
    """Arg -> player, str    Returns -> player"""
    player['letters'] = player['letters'] + letter
    return player

def use_letter(player, letter):
    """Arg -> player, str    Returns -> player"""
    player['letters'] = player['letters'].replace(letter, '', 1)
    return player

def add_points(player, points):
    """Arg -> player, int    Returns -> player"""
    player['points'] = player['points'] + points
    return player

#Recognizers
def is_player(arg):
    """Arg -> universal     Returns -> bool"""
    return (type(arg) == dict and set(arg.keys()) == {'id', 'points', 'letters', 'agent'})

def is_human(player):
    """Arg -> player    Returns -> bool"""
    return is_player(player) and not player['agent']
    
def is_agent(player):
    """Arg -> player    Returns -> bool"""
    return is_player(player) and player['agent']

#Test
def players_equal(p1, p2):
    """Arg -> player, player   Returns -> bool"""
    return ((is_human(p1) and is_human(p2)) or \
            (is_agent(p1) and is_agent(p2))) and \
           player_identity(p1) == player_identity(p2) and\
           player_points(p1) == player_points(p2) and \
            player_letters(p1) == player_letters(p2) 

#Transformer
def player_to_str(player):
    """Arg -> player    Returns -> str"""
    letters_display = player_letters(player)
    if letters_display:
        letters_str = ' ' + ' '.join(letters_display)
    else:
        letters_str = ''
    if is_agent(player):
        return (f'BOT({player_identity(player)}) ({str(player_points(player)):>3}):{letters_str}')
    if is_human(player):
        return (f'{player_identity(player)} ({str(player_points(player)):>3}):{letters_str}') 

#High Level Functions
def distribute_letters(player, letters_stack, num): 
    """
    Gives num letters from a stack to a player.
    Arg -> player, str, int    
    Returns -> player
    """
    for i in range(num):
        if len(letters_stack) > 0:
            receive_letter(player, letters_stack.pop())

    return player

#----------------------------------------------------------------------------
"""
ADT Vocabulary
Representation: dictionary {length: {start_letter: {word: points}}}
"""

#Constructor
def create_vocabulary(v):
    """
    Organizes words from a tuple into a dictionary.
    Arg -> tuple  
    Returns -> vocabulary
    """
    if type(v) != tuple or len(v) != len(set(v)) or len(v) < 1:
        raise ValueError(f"create_vocabulary: {TEXTS['invalid_args']}")
    vocabulary = {}
    for word in v:
        if type(word) != str or \
        not all(letra in LETTER_VALUES.keys() for letra in word):
            raise ValueError(f"create_vocabulary: {TEXTS['invalid_args']}")
        if len(word) < 2 or len(word) > 15:
            raise ValueError(f"create_vocabulary: {TEXTS['invalid_args']}")
    
        length, initial, points = len(word), word[0], 0
        if length not in vocabulary:
            vocabulary[length]={}
        if initial not in vocabulary[length]:
            vocabulary[length][initial]={}
        
        for i in range(length):
            points += LETTER_VALUES[word[i]]
        vocabulary[length][initial][word] = points            
    return vocabulary

#Selectors
def get_points(vocabulary, word):
    """Arg -> vocabulary, str      Returns -> int"""
    if len(word) in vocabulary and \
    word[0] in vocabulary[len(word)] and \
    word in vocabulary[len(word)][word[0]]:
        
        return vocabulary[len(word)][word[0]][word]
    
    else:
        return 0

def get_words(vocabulary, length, letter):
    """Arg -> Vocabulary, int, letter       Returns -> ((word, points), (word, points),...)"""
    if length not in vocabulary or letter not in vocabulary[length]:
        return ()
    
    word_points = []
    for word in vocabulary[length][letter]:
        word_points.append((word, get_points(vocabulary, word)))

    for i in range(length-1,-1,-1): #sort alphabetically, last to first letter
        word_points.sort(key = lambda x: SORT_KEY(x[0][i]) if len(x[0]) > i else 0) 
    word_points.sort(key = lambda x: -x[1]) #then by points
        
    return tuple(word_points)

#Test
def test_word_pattern(vocabulary, word, pattern, letters):
    """
    Checks if it is possible to form a word that fits the pattern with available letters.
    Arg -> vocabulary, word(str), pattern(str), letters(str)
    Returns -> bool
    """    
    if len(word) not in vocabulary or word[0] not in vocabulary[len(word)]\
     or word not in vocabulary[len(word)][word[0]]:
        return False
   
    letters_avail = letters
    possibility = ''

    if len(pattern) != len(word):
        return False
    if '.' not in pattern: #pattern already filled
        return False
    
    for i in range(len(pattern)):
        if pattern[i] == '.' and word[i] in letters_avail:
           letters_avail= letters_avail.replace(word[i], '', 1)
           possibility += word[i]
        elif pattern[i] != '.' and pattern[i] == word[i]:
            possibility += word[i]
        elif pattern[i] == '.' and word[i] not in letters_avail:
            return False
    
    return possibility == word  

#Transformers
def file_to_vocabulary(filename_or_list):
    """
    Decodes a file or uses the list from config.
    Arg -> filename (str) or list/tuple
    Returns -> vocabulary
    """
    if type(filename_or_list) in (list, tuple):
         return create_vocabulary(tuple(filename_or_list))

    with open(filename_or_list, 'r', encoding = 'utf-8') as f:
        vocab = set()
        for word in f.readlines():
            word = word.strip().upper()
            if 2<= len(word) <= 15 and all(letra in LETTER_VALUES.keys() for letra in word):
               vocab.add(word)

        return create_vocabulary(tuple(vocab)) 

def vocabulary_to_str(vocabulary):
    """Arg -> vocabulary      Returns -> str"""
    if type(vocabulary) == tuple:
        vocabulary = create_vocabulary(vocabulary)

    vocabulary_str=[]
    for length in sorted(vocabulary):
        for letter in sorted(vocabulary[length], key = SORT_KEY):
            vocabulary_str += [word[0] for word in get_words(vocabulary, length, letter)]

    return'\n'.join(vocabulary_str)
    
#High Level Functions
def search_pattern_word(vocabulary, pattern, letters, min_points):
    """
    Searches for words filling pattern, sorting by points.
    Arg -> vocabulary, str, str, int
    Returns -> [word, word, ...]
    """
    options=[]

    if pattern[0] != '.':
        words_points = get_words(vocabulary, len(pattern), pattern[0])
        if len(words_points) != 0:
            for word in words_points:
                if test_word_pattern(vocabulary, word[0], pattern, letters)\
                and word[1] >= min_points:
                    options.append(word)

    elif pattern[0] == '.':
        for letter in letters:
            words_points = get_words(vocabulary, len(pattern), letter)
            if len(words_points) != 0 :
                for word in words_points:
                    if test_word_pattern(vocabulary, word[0], pattern, letters)\
                     and word[1] >= min_points:
                        options.append(word)

    if len(options) == 0:
        return ('',0)
    
    for i in range(len(pattern)-1,-1,-1):
        options.sort(key = lambda x: SORT_KEY(x[0][i]) if len(x[0]) > i else 0)
    options.sort(key = lambda x: -x[1])
    return options[0]


#----------------------------------------------------------------------------
"""
ADT Board
Representation: list of lists of strings (15x15 matrix)
"""

#Constructor
def create_board():
    """Returns -> board"""
    board = []
    for i in range(HEIGHT):
        row = ['.' for j in range(WIDTH)]
        board.append(row)
    return board

#Selector
def get_letter(board, square):
    """Arg -> board, square       Returns -> str"""
    letter = board[get_row(square) - 1][get_col(square)- 1] 
    return letter

#Modifier
def insert_letter(board, square, letter):
    """Arg -> board, square, str      Returns -> board (updated)"""
    board[get_row(square) - 1][get_col(square) - 1] = letter
    return board

#Recognizer
def is_board(arg):
    """Arg -> board     Returns -> bool"""
    if type(arg) != list or len(arg) != HEIGHT:
        return False
    
    for i in range(len(arg)):
        if type(arg[i]) != list or len(arg[i]) != WIDTH:
            return False
        for j in range(len(arg[i])):
            if type(get_letter(arg, create_square(i+1, j+1))) != str:
                return False
            
    return True

def is_board_empty(arg):
    """Arg -> board     Returns -> bool"""
    if is_board(arg):
        for i in range(len(arg)):
            for j in range(len(arg[i])):
                if get_letter(arg, create_square(i+1, j+1)) != '.':
                    return False
    
    else: 
        return False 
    
    return True
    
#Test
def boards_equal(t1, t2):
    """Arg -> board, board     Returns -> bool"""
    if is_board(t1) and is_board(t2):
        for i in range(len(t1)):
            for j in range(len(t1[i])):
                if get_letter(t1, create_square(i+1, j+1)) !=  get_letter(t2, create_square(i+1, j+1)):
                    return False
    else:
        return False
    return True

#Transformer
def board_to_str(board):
    """Arg -> board     Returns -> str"""
    board_str = (f'{TEXTS["board_header_1"]:>34}\n'
                    f'{TEXTS["board_header_2"]:>34}\n'
                    f'{"+-------------------------------+":>36}')
    
    row_count = 0
    for i in range(HEIGHT):
        board_str += f'\n{str(i+1):>2} |'
        for c in board[row_count]:
            board_str += f'{c:>2}'
        board_str += ' |'
        row_count += 1
    
    board_str += f'\n{"+-------------------------------+":>36}'
    
    return board_str

#High Level Functions
def get_pattern(board, start, end):
    """
    Gets sequence of chars from a portion of the board.
    Arg -> board, square, square
    Returns -> pattern(str)
    """
    pattern=''
    direction = get_direction(start, end)

    if direction == VERTICAL:
        while get_row(start) <= get_row(end):        
            pattern += get_letter(board, start)
            new_start = increment_square(start, direction, 1)
            if new_start == start:
                break
            start = new_start

    elif direction == HORIZONTAL:
        while get_col(start) <= get_col(end):
            pattern += get_letter(board, start)
            new_start = increment_square(start, direction, 1)
            if new_start == start:
                break
            start = new_start

    return pattern

def insert_word(board, square, direction, word):
    """
    Alters chars on a board portion.
    Arg -> board, square, str, str     
    Returns -> Board(updated)
    """
    for letter in word:
        insert_letter(board, square, letter)
        square=increment_square(square, direction, 1)

    return board

def get_subpatterns(board, start, end, length):
    """
    Gets all subpatterns between start and end with max length empty spaces.
    Arg -> board, square, square, int
    Returns -> (subpattern, subpattern,...), (start_square, start_square,...)
    """
    subpatterns = ()
    starts = ()
    pattern = get_pattern(board, start, end)
    
    for i in range (len(pattern)-1):
        for j in range(len(pattern), i, -1):
            if (not all(c == '.' for c in pattern[i : j])) and\
            (not all(c != '.' for c in pattern[i : j])) and\
            (pattern[i : j].count('.') <= length) and\
            not (i > 0 and pattern[i-1] != '.') and\
            not (j < len(pattern) and pattern[j] != '.'):
                subpatterns += (pattern[i : j], )
                starts += ((increment_square(start, get_direction(start, end), i)), )
    return subpatterns, starts

def generate_all_patterns(board, length):
    """
    Generates all possible patterns on board with up to length empty spaces.
    Arg -> board, length
    Returns -> ((pattern, ...), (start, ...), (direction, ...))
    """
    patterns_tpl = ()
    start_tpl = ()
    directions_tpl = ()
    
    for i in range(1, HEIGHT+1):
        subpatterns_h = get_subpatterns(board, create_square(i, 1), create_square(i, WIDTH), length)
        patterns_tpl += subpatterns_h[0]
        start_tpl += subpatterns_h[1]
        directions_tpl += (HORIZONTAL, ) * len(subpatterns_h[0])
    
    for j in range(1, WIDTH+1):
        subpatterns_v = get_subpatterns(board, create_square(1, j), create_square(HEIGHT, j), length)
        patterns_tpl += subpatterns_v[0]
        start_tpl += subpatterns_v[1]
        directions_tpl += (VERTICAL, ) * len(subpatterns_v[0])

    return patterns_tpl, start_tpl, directions_tpl


#----------------------------------------------------------------------------
"""Additional Functions"""

def shuffle_bag(seed):
    """"
    Shuffles the bag pseudo-randomly given a seed.
    Arg -> Seed
    Returns -> Shuffled Bag (lst)
    """
    def generate_random_num(state):
        state ^= ( state << 13 ) & 0xFFFFFFFF
        state ^= ( state >> 17 ) & 0xFFFFFFFF
        state ^= ( state << 5 ) & 0xFFFFFFFF
        return state

    def permute_letters(letters, state):
        j = (generate_random_num(state))
        for i in range(len(letters)-1, 0, -1): 
            letters[(j) % (i + 1)], letters[i] = letters[i], letters[(j) % (i + 1)]
            j = generate_random_num(j)

    letters = sorted(expand_set(BAG_DISTRIBUTION), key = SORT_KEY)
    permute_letters(letters, seed) 
    return letters


def human_play(board, player, vocabulary, stack):
    """
    Receives, validates and processes human input.
    Args -> board, player, vocabulary, bag(prev func)
    Returns -> bool    
    """
    input_valid = False
    while not input_valid:
        action = input(TEXTS['play_prompt'].format(player_identity(player))).split()

        if len(action) == 0: 
            continue

        if action[0] == 'T' and len(stack) >= 7: 
            letters = action[1:] 
            if len(letters) < 1: 
                continue

            char_invalid = False
            player_letters_list = player_letters(player)
            for letter in letters:
                if letter not in LETTER_VALUES  or letters.count(letter) > player_letters_list.count(letter):
                    char_invalid = True
                    break
            if char_invalid:
                continue

            for letter in letters: 
                use_letter(player, letter) 
            distribute_letters(player, stack, len(letters)) 
            return True
        
        elif action[0] == 'J':
            action = action[1:]
            if len(action) < 4: 
                continue

            if not is_square(create_square((int(action[0])), (int(action[1])))):
                continue
            try: 
                start, direction, word = create_square((int(action[0])), (int(action[1]))), action[2], action[3]
            except ValueError:
                continue
            if direction == HORIZONTAL:
                try:
                     end = create_square(get_row(start), get_col(start) + len(word)-1)
                except ValueError:
                    continue
            elif direction == VERTICAL:
                try:
                    end = create_square(get_row(start) + len(word) -1, get_col(start))
                except ValueError:
                    continue

            pattern = get_pattern(board, start, end)
            
            if is_board_empty(board) and test_word_pattern(vocabulary, word, pattern, player_letters(player)):
                insert_word(board, start, direction, word)

                if get_letter(board, create_square(CENTER[0], CENTER[1])) == '.':
                    insert_word(board, start, direction, pattern) 

                else:
                    add_points(player, get_points(vocabulary, word))
                    add_count = 0
                    for i in range(len(word)):
                        if pattern[i] == '.':
                            use_letter(player, word[i])
                            add_count += 1
                    distribute_letters(player, stack, add_count)
                    return True
                   
            
            elif (not is_board_empty(board)) and pattern.count('.') != len(pattern) and\
            test_word_pattern(vocabulary, word, pattern, player_letters(player)) and\
            (get_letter(board, increment_square(start, direction, -1)) == '.') and \
            (get_letter(board, increment_square(end, direction, 1)) == '.'):
        
                insert_word(board, start, direction, word)
                add_points(player, get_points(vocabulary, word))
                add_count = 0
                for i in range(len(word)):
                    if pattern[i] == '.':
                        use_letter(player, word[i])
                        add_count += 1
                distribute_letters(player, stack, add_count)
                return True
                
        elif action[0] == 'P':
            return False


def agent_play(board, player, vocabulary, stack):
    """
    Generates patterns and finds best move for agent.
    Args -> board, player, vocabulary, stack(lst)
    Returns -> bool
    """

    if is_board_empty(board):
        print(TEXTS['pass_format'].format(player_identity(player)))
        return False
    
    patterns, starts, directions = generate_all_patterns(board, len(player_letters(player)))
    if len(patterns) != 0: 
        if player_identity(player) == 'FACIL':
            n = 100
        elif player_identity(player) == 'MEDIO':
            n = 50
        elif player_identity(player) == 'DIFICIL':
            n = 10
        patterns, starts, directions = patterns[::n], starts[::n], directions[::n]

    possibilities = []
    for i in range(len(patterns)):
        if any(c != '.' for c in patterns[i]) and any(c == '.' for c in patterns[i]):
            pattern, start, direction = patterns[i], starts[i], directions[i]
            result = search_pattern_word(vocabulary, pattern, player_letters(player), 0)
            if result[0] != '':  
                possibilities.append((result, start, direction))

    possibilities.sort(key = lambda x : x[0][1], reverse = True) 
    
    if possibilities != []: 
        best = possibilities[0] 
        word, points = best[0]  
        start = best[1]  
        direction = best[2]
        
        if direction == HORIZONTAL:
            pattern = get_pattern(board, start, create_square(get_row(start), get_col(start) + len(word)-1))
        if direction == VERTICAL:
            pattern = get_pattern(board, start, create_square(get_row(start) + len(word) -1, get_col(start)))
        
        insert_word(board,  start, direction, word)
        remove_count = 0
        for i in range(len(word)):
            if pattern[i] == '.':
                use_letter(player, word[i])
                remove_count += 1
        distribute_letters(player, stack, remove_count)
        add_points(player, points)
        
        #Display formatted output
        print(TEXTS['play_format'].format(player_identity(player), get_row(start), get_col(start), direction, word))
        return True

    elif possibilities == [] and len(stack) >= MAX_LETTERS_INIT:
        print(TEXTS['exchange_format'].format(player_identity(player), " ".join(player_letters(player))))
        for letter in player_letters(player):
            use_letter(player, letter)
        distribute_letters(player, stack, MAX_LETTERS_INIT)
        return True
    
    else:
        print(TEXTS['pass_format'].format(player_identity(player)))
        return False


def scrabble_game(players_tuple, seed, language='PT'):
    """
    Main game flow.
    Arg -> (human, human, @agent, ...), int, lang_code
    Returns -> tuple (scores)
    """
    select_language(language) 

    #VALIDATION
    if type(players_tuple) != tuple or type(seed) != int  \
    or seed < 0 or not(1 < len(players_tuple) <= MAX_PLAYERS):
        raise ValueError(f"scrabble_game: {TEXTS['invalid_args']}")
    
    #LOAD VOCABULARY FROM CONFIG FILE
    filename = LANGUAGES[language]['VOCABULARY_FILE']
    try:
        vocabulary = file_to_vocabulary(filename)
    except FileNotFoundError:
        print(f"CRITICAL ERROR: The vocabulary file '{filename}' was not found.")
        print("Please make sure pt.txt, en.txt, and fr.txt are in the same folder.")
        return

    #GAME SETUP
    stack = shuffle_bag(seed)
    players = []
    board = create_board()
    continue_game = True
    current_player_idx = 0
    consecutive_passes = 0 
    
    for player_name in players_tuple: 
        if type(player_name) == str and player_name[0] == '@' and player_name[1:] in LEVELS:
            players.append(create_agent(player_name[1:]))
        elif type(player_name) == str and player_name[0] == '@' and player_name[1:] not in LEVELS:
            raise ValueError(f"scrabble_game: {TEXTS['invalid_args']}")
        elif type(player_name) == str:
            players.append(create_human(player_name))
        else:
            raise ValueError(f"scrabble_game: {TEXTS['invalid_args']}")
        
    if len(stack) < (MAX_LETTERS_INIT * len(players_tuple)):
        raise ValueError(f"scrabble_game: {TEXTS['invalid_args']}")
    
    for player in players:
        distribute_letters(player, stack,  MAX_LETTERS_INIT)

    print(TEXTS['welcome'])
    
    #GAME LOOP
    while continue_game: 
        
        print(board_to_str(board))
        for player in players:
            print(player_to_str(player))

        if is_human(players[current_player_idx]):
            result = human_play(board, players[current_player_idx], vocabulary, stack)
        elif is_agent(players[current_player_idx]): 
            result = agent_play(board, players[current_player_idx], vocabulary, stack)
        
        if not result:
            consecutive_passes += 1
        else:
            consecutive_passes = 0
        if consecutive_passes >= len(players):
            continue_game = False
        for player in players:
            if len(player_letters(players[current_player_idx])) == 0 and len(stack) == 0:
                continue_game = False  
        
        if continue_game:
            current_player_idx = (current_player_idx + 1)  % len(players) 
         
    scores = tuple(player_points(player) for player in players)
    return scores

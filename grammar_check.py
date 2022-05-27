import sys
import numpy as np
import re

def main():
        try:
            grammar, num_of_nodes, word = init()
        except IndexError:
            print("Correct usage: ./grammar_check.py file word", end = "\n")
            return
        start = 0
        t = check_word(grammar, word, start, num_of_nodes)
        if t is True:
            print(f"Yes, the word {word} is constructable via the given grammar.\n")
        else:
            print(f"No, the word {word} is not constructable via the given grammar.\n")
        print("*----------------------------------------------------------------*")

def init():
    ''' print user info '''

    print("\n\n")
    print("//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++//\n")
    print("Conventions: Please name your nodes in ascending order from 0 to n.\n")
    print("Also make sure that the letters(which can be numbers as well) of your word differ from those used as your node's names.\n")
    print("//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++//")
    print("\n\n")

    '''the first argument is the name of the file '''
    if len(sys.argv[0:]) != 3:
        raise IndexError

    word = sys.argv[2]
    grammar = []
    num_of_nodes = 0

    try:
        with open(sys.argv[1], 'r') as my_file:
            lines = my_file.readlines()
            lines = [line.rstrip() for line in lines]
            num_of_nodes = len(lines)
            for entr in lines:
                grammar.append(re.split('[>|]', entr))
    except IndexError:
        print("Correct usage: ./grammar_check.py file word", end = "\n")
    except FileNotFoundError:
        print("Could not open given file.", end = "\n")

    ''' check correct syntax of grammar '''
    set_of_nodes = [el[0] for el in grammar]
    for i, el in enumerate(set_of_nodes):
        assert el == str(i), "Please name your nodes in ascending order from 0 to n."

    return grammar, num_of_nodes, word

def check_word(grammar, word, cur_state, num_of_nodes):
    '''assume: grammar is already aligned in respect to syntactic standards of clean'''

    opt = np.squeeze([e for e in grammar if int(e[0]) == cur_state])
    pos_rules = select_fit(opt, word, num_of_nodes)

    if not pos_rules:
        return False

    if np.any(np.where(np.array(pos_rules) == "epsilon")):
        return True #word valid

    if '-1' in np.array(pos_rules)[:,1]:
        return True #word valid

    ''' recursice call '''
    for el in pos_rules:

        if check_word(grammar, el[2], el[1], num_of_nodes) is True:
            return True

    return False

def select_fit(opt, word, num_of_nodes):
    possible_fits = []
    entr_cpy = ''
    word_cpy = ''
    for idx, entr in enumerate(opt[1:]):
        entr_cpy = entr
        word_cpy = word

        if entr_cpy == "epsilon" and word_cpy == '':
            possible_fits.append((idx, -1, "epsilon")) #done

        try:
            '''left sided pattern matching'''
            while entr_cpy[0] is word_cpy[0]:
                entr_cpy = entr_cpy[1:]
                word_cpy = word_cpy[1:]
            '''right sided pattern matching'''
            while entr_cpy[-1] is word_cpy[-1]:
                entr_cpy = entr_cpy[:-1]
                word_cpy = word_cpy[:-1]

            try:
                if int(entr_cpy) in np.arange(num_of_nodes):
                    possible_fits.append((idx, int(entr_cpy), word_cpy))
            except ValueError:
                pass

            if entr_cpy == "" and word_cpy == "":
                possible_fits.append((idx, -1, word_cpy)) #insert -1 if no other node is accessible

        except IndexError:

            try:
                if int(entr_cpy) in np.arange(num_of_nodes):
                    possible_fits.append((idx, int(entr_cpy), word_cpy))
            except ValueError:
                    pass
            if entr_cpy == "" and word_cpy == "":
                possible_fits.append((idx, -1, word_cpy))

    ''' return tuple: (index/row of rule appearance, new state, matched word) '''
    return possible_fits

if __name__ == "__main__":
    main()

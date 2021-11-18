# simplified grammar to use for the cyk algorithm implemented as a dictionary
# These are the productions for the simplified grammar in CNF
# 
# S -> FB
# B -> CB | b
# C -> a
# D -> b
# E -> CD
# F -> HB | CD
# G -> IB | a
# H -> EG
# I -> CG 

# this is the dictionary that stores the above CFG in CNF
productions = {
     "S": ["FB"],
     "B": ["b"],
     "C": ["a"],
     "D": ["b"],
     "E": ["CD"],
     "F": ["HB", "CD"],
     "G": ["IB", "a"],
     "H": ["EG"],
     "I": ["CG"]
    }


def cyk_algorithm(w):

    # capture length of input string
    str_length = len(w)

    # create N x N table where n is length of input string
    # initial values of the table will be ""
    table = []
    table_row = []
    for i in range(str_length):
        table_row = []
        for j in range(str_length):
            table_row.append("")
        table.append(table_row)

    # build list of variables, full non terminal productions (two capital letters)
    # and also a list to store terminals
    variables = []
    full_non_terminals = []
    terminals = []
    for i in range(str_length):
        # go through rules of the grammar
        for lhs, transition in productions.items():
            # add variables to variable list if not there
            if lhs not in variables:
                variables.append(lhs)
            # iterate through rhs list of rules
            for j in range(len(transition)):
                # if length is one then we know it is a terminal
                if len(transition[j]) == 1 and transition[j] not in terminals:
                    terminals.append(transition[j])
                # if length is more than one then we know this is a non terminal rule consisting of two non_terminals
                elif len(transition[j]) != 1 and transition[j] not in full_non_terminals:
                    full_non_terminals.append(transition[j])

    # iterate through length of string
    for i in range(str_length):
        # iterate through the variables of the grammar
        for var in variables:
            # check if a production exists of the form A -> x
            # where A is any non_terminal of the grammar and x is any terminal
            for x in terminals:
                if x in productions[var] and x == w[i]:
                    table[i][i] += var

    # fill in the rest of the table above the diagonal with the produced variables
    # iterate through length of input string
    for index in range(str_length):
        # we want index to start at the second position so continue to next iter when index == 0
        if index == 0:
            continue
        else:
            # do this for every iter where index is not 0
            # iterate through the substrings of the string
            for j in range(str_length-index):
                # l and k are index variables used to fill the triangular table
                l = j + index
                for k in range(j, l):
                    # iterate through the variables of the grammar
                    for var in variables:
                        # iterate through every rule that contains a nt combination
                        # these are of the form AB, CD, EF, GH, etc..
                        # full non-terminals are assumed to be a combination of 2 capital letters
                        for nt in full_non_terminals:
                            # check if the combination of nt symbols exists as a production rule of the grammar
                            if nt in productions[var]:
                                # if true, store the string of non_terminal variables from the cells of the table
                                # that you would want to union together
                                str1 = table[j][k]
                                str2 = table[k+1][l]
                                # if the first non_terminal is in the first cell and the second non_terminal is
                                # in the second cell, (str1 and str2 respectively) then concatenate current
                                # variable to the string at position j,l
                                if nt[0] in str1 and nt[1] in str2:
                                    table[j][l] += var

    # print the table to ensure whether S is appears in position 0, n-1 in the table
    for row in table:
        print(row)

    # capture string of variables at position 0,n-1 in our table
    # if this string in this position contains the start symbol, then the input string w is accepted by the grammar
    check_line = table[0]
    if check_line[-1] == 'S':
        print("The string was accepted by the grammar!")
    else:
        print("The string was rejected by the grammar.")


# This is the test string for our grammar in CNF
# Pass testString to the CYK Algorithm to test membership of grammar
# CNF Grammar is hardcoded from result/output from of cfgtocnf.py
testString = "abb"
cyk_algorithm(testString)

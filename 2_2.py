import itertools
from tabulate import tabulate
import re
from typing import Iterable
import os
from termcolor import colored
import copy

os.system("color")


# initial data

# sem task 3
# seen_examples = [1, 3, 4, 6, 8]
# amount = 3
# solutions = [("10.", 1), ("0.1", 1), (".11", 1), ("...", 0)]

# sem task 4
seen_examples = [2, 15, 3, 14, 12, 6, 8, 10, 4, 13, 9, 11]
amount = 4
solutions = [("10..", 1), ("..01", 1), ("....", 0)]

# my
# seen_examples = [14, 4, 6, 13, 3, 11, 5, 8, 5, 7, 2, 9]
# amount= 4
# solutions = [('..01',1), ('00..', 1), ('....',0)]


def gen_headers():
    headers = ["N"]
    for i in range(1, amount + 1):
        headers += ["p{}".format(i)]
    headers += ["L", "h", "ошибка"]
    return headers


def to_string(t: Iterable[int]) -> str:
    """
    (0,0,0) -> "000"
    """
    return "".join(map(str, t))


def gen_literal_regex_list():
    literal_regex_list = list(
        map(to_string, itertools.product([".", "1", "0"], repeat=amount))
    )
    return literal_regex_list


def prettify(input_table):
    """colors output"""
    tbl = copy.deepcopy(input_table)
    for idx, row in enumerate(tbl):
        if not (idx + 1 in seen_examples):
            continue
        new_row = list(
            map(
                lambda x: colored(x if x is not None else "", "green")
                if row[amount]
                else colored(x if x is not None else "", "red"),
                row,
            )
        )
        tbl[idx] = tuple(new_row)
    return tbl


print(colored("soltuions: ", "blue"), solutions)
seen_examples.sort()

table = list(itertools.product([0, 1], repeat=amount))
for idx, row in enumerate(table):
    new_row = list(row)
    new_row += [None, None, None]
    table[idx] = tuple(new_row)

for (value, result) in solutions:
    for idx, row in enumerate(table):
        if row[amount]:
            continue
        if re.match(str(value), to_string(row[:amount])):
            new_row = list(row)
            new_row[amount] = result
            table[idx] = tuple(new_row)

S_plus = []
S_minus = []
for idx, row in enumerate(table):

    if not (idx + 1 in seen_examples):
        continue
    if row[amount]:
        S_plus.append(to_string(row[:amount]))
    else:
        S_minus.append(to_string(row[:amount]))

print(colored("S+ : ", "blue"), S_plus)
print(colored("S- :", "blue"), S_minus)


# TODO check hypothises, 'cause they don't seem right
literals = gen_literal_regex_list()
f = lambda x: x.count(".")
sorted(literals, key=f, reverse=True)
literals = literals[1:]
print(colored("literals: ", "blue"), literals)
h = []

for idx, literal in enumerate(literals):
    if not S_plus or not S_minus:
        break

    match_minus = [re.match(literal, x) for x in S_minus if re.match(literal, x) is not None]
    match_plus = [re.match(literal, x) for x in S_plus if re.match(literal, x) is not None]
    if match_plus and not match_minus:
        h.append((literal, 1))
        to_remove = [x.string for x in match_plus]
        S_plus = list(set(S_plus) - set(to_remove))
    elif not match_plus and match_minus:
        h.append((literal, 0))
        to_remove = [x.string for x in match_minus]
        S_minus = list(set(S_minus) - set(to_remove))
    print('step {}'.format(idx))
    print("literal: ", literal)
    print("S+: ", S_plus)
    print("S-: ", S_minus)
    print("h: ", h)

h.append(solutions[-1])
print(colored("h: ", "blue"), h)

for idx, row in enumerate(table):
    is_seen = idx + 1 in seen_examples
    if is_seen:
        h_row = row[amount]
    else:
        for (value, result) in h:
            if not row[amount + 1]:
                if re.match(value, to_string(row[:amount])):
                    h_row = result
                    break
    new_row = list(row)
    new_row[amount + 1] = h_row
    if not is_seen:
        new_row[-1] = "-" if new_row[amount] == new_row[amount + 1] else "+"
    table[idx] = tuple(new_row)

print(
    tabulate(
        prettify(table),
        headers=gen_headers(),
        tablefmt="pretty",
        showindex=list(
            map(
                lambda x: colored(x, "yellow") if x in seen_examples else x,
                range(1, 2 ** amount + 1),
            )
        ),
    )
)

epsilon = len([row[-1] for row in table if row[-1] == "+"]) / 2 ** amount
print("epsilon: ", epsilon)
assert epsilon <= (2 ** amount - seen_examples.__len__()) / 2 ** amount

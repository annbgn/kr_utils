import itertools
from tabulate import tabulate
import re
from typing import Iterable

# initial data
seen_examples = [14, 4, 6, 13, 3, 11, 5, 8, 5, 7, 2, 9]
# seen_examples = [1, 3, 4, 6, 8]
amount= 4
# amount = 3
solutions = [('..01',1), ('00..', 1), ('....',0)]
# solutions = [("10.", 1), ("0.1", 1), (".11", 1), ("...", 0)]


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

print("S+ : ", S_plus)
print("S- :", S_minus)


# TODO check hypothises, 'cause they don't seem right
literals = gen_literal_regex_list()
f = lambda x: x.count(".")
sorted(literals, key=f, reverse=True)
literals = literals[1:]
h = []
for idx, row in enumerate(table):
    if not (idx + 1 in seen_examples):
        continue
    for literal in literals:
        if not S_plus or not S_minus:
            break
        templates_so_far = [x[0] for x in h]
        if literal in templates_so_far:
            break  # prevent duplicates +  preserve order

        bool_row = to_string(row[:amount])
        mtch = re.match(literal, bool_row)
        if bool_row in S_plus and not bool_row in S_minus:
            h.append((literal, 1))
            S_plus.remove(bool_row)
        elif not bool_row in S_plus and bool_row in S_minus:
            h.append((literal, 0))
            S_minus.remove(bool_row)
h.append(solutions[-1])
print("h: ", h)

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
        table,
        headers=gen_headers(),
        tablefmt="pretty",
        showindex=list(range(1, 2 ** amount + 1)),
    )
)

epsilon = len([row[-1] for row in table if row[-1] == "+"]) / 2 ** amount
print("epsilon: ", epsilon)
assert epsilon <= (2 ** amount - seen_examples.__len__()) / 2 ** amount

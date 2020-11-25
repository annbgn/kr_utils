import itertools
from tabulate import tabulate

# initial data
# both indices are given in the task and reduced by 1
# amount is given
index1 = 0
index2 = 2
amount = 5


def prettify(coefficient_list):
    s = ''
    for i in range(1, amount):
        s += 'p{i} + '.format(i=i)
    s += 'p{amount} > {amount}/2'.format(amount=amount)
    s = s.replace('p', '{}p')
    return s.format(*coefficient_list)


def gen_headers():
    headers = []
    for i in range(1, amount+1):
        headers += ["x{}".format(i)]
    headers += ["x{} v x{}".format(index1 + 1, index2 + 1), "h", " "]
    return headers


table = list(itertools.product([0, 1], repeat=amount))
for idx, row in enumerate(table):
    new_row = list(row)
    new_row += [row[index1] or row[index2], prettify([None] * amount), None]
    table[idx] = tuple(new_row)

for idx, row in enumerate(table):
    if idx != 0:
        coefficient_list = table[idx - 1][amount + 1]
        new_row = list(row)
        new_row[amount + 1] = coefficient_list

        if table[idx - 1][-1] == "П":
            coefficient_list = [
                (lambda x, y: (y if not x else 2 * y))(i, j)
                for (i, j) in list(
                    zip(table[idx - 1][:amount], table[idx - 1][amount + 1])
                )
            ]
            new_row[amount + 1] = coefficient_list
        elif table[idx - 1][-1] == "У":
            coefficient_list = [
                (lambda x, y: (0 if x else y))(i, j)
                for (i, j) in list(
                    zip(table[idx - 1][:amount], table[idx - 1][amount + 1])
                )
            ]
            new_row[amount + 1] = coefficient_list

        condition = (
            sum([i * j for (i, j) in list(zip(coefficient_list, row[:amount]))])
            >= amount / 2
        )
        if row[amount] and not condition:
            result = "П"
        elif not row[amount] and condition:
            result = "У"
        else:
            result = " - "
        new_row[-1] = result
        table[idx] = tuple(new_row)
    else:
        coefficient_list = [1] * amount
        result = " - "
        new_row = list(row)
        new_row[amount + 1] = coefficient_list
        table[idx] = tuple(new_row)

for idx, row in enumerate(table):
    new_row = list(row)
    new_row[-2] = prettify(row[-2])
    table[idx] = tuple(new_row)

print(tabulate(table, headers=gen_headers(), tablefmt="pretty"))

from itertools import product
import multiprocessing

def process(i):
    if max(map(i.count, i)) > 3:
        return 0
    for j0, j1 in zip(i, i[1:]):
        if (j0 % 2) == (j1 % 2):
            return 0
    return 1

pool = multiprocessing.Pool(multiprocessing.cpu_count() - 1)

ans = sum(pool.map(process, product(range(1, 9), repeat=9)))
print(ans)
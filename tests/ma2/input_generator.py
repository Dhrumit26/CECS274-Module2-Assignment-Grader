import random


def gen_1_insert_book():
    f = random.randint(1, 9)
    key = str(random.randint(20, 3000)) + chr(random.randint(65, 90)) + str(random.randint(1000, 3000))
    rank = str(random.randint(1000, 5000))
    idx = random.randint(0, 20000)
    file = open("input_1.txt", 'w')
    file.write(f"2\n1\nbooks_{f}.txt\n3\n{idx}\n2\n1\n{key}\nThe Newly Added Book\nBook/Novel\n{rank}\n0\n{idx}\nq")
    file.write(f"\n3\n{idx}\n3\n{idx + 1}\nq\nq")
    file.close()
    return


def gen_2_remove_book():
    f = random.randint(1, 9)
    idx = random.randint(0, 20000)
    file = open("input_2.txt", 'w')
    file.write(f"2\n1\nbooks_{f}.txt\n3\n{idx}\n2\n2\n{idx}\nq\n3\n{idx}\nq\nq")
    file.close()
    return


def gen_3_get_book():
    f = random.randint(1, 9)
    idx = random.randint(0, 20000)
    file = open("input_3.txt", 'w')
    file.write(f"2\n1\nbooks_{f}.txt\n3\n{idx}\nq\nq")
    file.close()
    return


def gen_4_srch_infx():
    n = str(random.randint(2, 7))
    f = str(random.randint(1, 5))
    file = open("input_4.txt", 'w')
    file.write(f"2\n1\nbooks_{f}.txt\n4\nTrees\n{n}\nq\nq")
    file.close()
    return


def gen_5_add_by_idx():
    f = random.randint(1, 9)
    file = open("input_5.txt", 'w')
    file.write(f"2\n1\nbooks_{f}.txt\n")
    n = random.randint(3, 6)
    for i in range(n):
        idx = random.randint(0, 20000)
        file.write(f"5\n{idx}\n")
    file.write("6\n" * (n+1))
    file.write("q\nq\n")
    file.close()
    return


gen_1_insert_book()
gen_3_get_book()
gen_2_remove_book()
gen_4_srch_infx()
gen_5_add_by_idx()
import random
import time
from queue import PriorityQueue, Queue

# -------------------------------
# Алгоритмы
# -------------------------------
def BFSD(M, start):
    dist = [-1] * len(M)
    pq = PriorityQueue()
    dist[start] = 0
    pq.put((0, start))
    while not pq.empty():
        current_dist, current_vertex = pq.get()
        if current_dist > dist[current_vertex]:
            continue
        for i in range(len(M)):
            if M[current_vertex][i] > 0:
                new_dist = dist[current_vertex] + M[current_vertex][i]
                if dist[i] == -1 or new_dist < dist[i]:
                    dist[i] = new_dist
                    pq.put((new_dist, i))
    return dist

def BFSD_2(M, start):
    dist = [-1] * len(M)
    q = Queue()
    q.put(start)
    dist[start] = 0
    while not q.empty():
        current = q.get()
        for i in range(len(M)):
            if M[current][i] and dist[i] == -1:
                dist[i] = dist[current] + M[current][i]
                q.put(i)
    return dist

def isolation(M, vertex):
    counter = 0
    for j in range(len(M)):
        counter += M[vertex][j]
        counter += M[j][vertex]
    return counter == 0

# -------------------------------
# Безопасный ввод числа
# -------------------------------
def input_int(prompt, min_val=1):
    while True:
        try:
            value = int(input(prompt))
            if value < min_val:
                print(f"Ошибка: введите число >= {min_val}")
                continue
            return value
        except ValueError:
            print("Ошибка: введите корректное число!")

# -------------------------------
# Безопасный ввод да/нет
# -------------------------------
def input_yes_no(prompt):
    while True:
        value = input(prompt).strip().lower()
        if value in ['y', 'n']:
            return value == 'y'
        print("Ошибка: введите 'y' для да или 'n' для нет")

# -------------------------------
# Главная функция
# -------------------------------
def main():
    random.seed(time.time())

    # --- Ввод пользователем с защитой ---
    sizeM = input_int("Введите размер графа: ")
    weighted = input_yes_no("Граф взвешенный? (y/n): ")
    oriented = input_yes_no("Граф ориентированный? (y/n): ")

    # --- Создание матрицы ---
    print("\nМатрица смежности:")
    M = [[0]*sizeM for _ in range(sizeM)]
    for i in range(sizeM):
        start_j = 0 if oriented else i
        for j in range(start_j, sizeM):
            if i == j:
                M[i][j] = 0
            else:
                M[i][j] = random.randint(0, 1)
                if weighted and M[i][j]:
                    M[i][j] = random.randint(1, 9)
                if not oriented:
                    M[j][i] = M[i][j]
        for j in range(sizeM):
            print(f"{M[i][j]:3d}", end=" ")
        print()

    # --- Первый вариант BFSD ---
    print("\nМассив расстояний для "
          f"{'взвешенного ' if weighted else 'невзвешенного '}"
          f"{'ориентированного ' if oriented else 'неориентированного '}"
          "графа:")

    tmp_arr = []
    for i in range(sizeM):
        row = BFSD(M, i)
        tmp_arr.append(row)
        for d in row:
            print("   _" if d == -1 else f"{d:4d}", end="")
        print()

    # --- Второй вариант BFSD_2 ---
    print("\n2-ой вариант:")
    tmp_arr_2 = []
    for i in range(sizeM):
        row = BFSD_2(M, i)
        tmp_arr_2.append(row)
        for d in row:
            print("   _" if d == -1 else f"{d:4d}", end="")
        print()

    # --- Эксцентриситеты ---
    ecc_for_vertexes = []
    for i in range(sizeM):
        max_dist = max([d for d in tmp_arr[i] if d != -1], default=-1)
        if max_dist != -1 and not isolation(M, i):
            ecc_for_vertexes.append(max_dist)
        else:
            ecc_for_vertexes.append(-1)

    # --- Радиус и диаметр ---
    valid_ecc = [e for e in ecc_for_vertexes if e != -1]
    if valid_ecc:
        radius = min(valid_ecc)
        diametr = max(valid_ecc)
    else:
        radius = diametr = None
        print(f"\nРадиус: {radius}\nДиаметр: {diametr}\n")

    # --- Вывод эксцентриситетов ---
    print("Эксцентриситеты:")
    for i, e in enumerate(ecc_for_vertexes):
        if e == -1:
            print(f"Вершина {i+1} изолирована")
        else:
            print(f"для {i+1} вершины: {e}")

    # --- Центральные и периферийные вершины ---
    print("\nЦентральные вершины: ", end="")
    for i, e in enumerate(ecc_for_vertexes):
        if e == radius:
            print(i + 1, end=" ")
    print("\nПериферийные вершины: ", end="")
    for i, e in enumerate(ecc_for_vertexes):
        if e == diametr:
            print(i + 1, end=" ")
    print()

    # --- Сумма расстояний ---
    print("\nСумма расстояний у каждой вершины:")
    summ_dist = []
    for i in range(sizeM):
        s = sum([d if d != -1 else 0 for d in tmp_arr[i]])
        summ_dist.append(s)
        print(f"для {i+1} вершины - {s}")

    # --- Центр тяжести ---
    if summ_dist:
        min_sum = min(summ_dist)
        index_of_vertex = summ_dist.index(min_sum) + 1
        print("\nЦентр тяжести:\nВершина", index_of_vertex)
    else:
        print("\nЦентр тяжести: невозможно определить")


if __name__ == "__main__":
    main()


import random
import time

# Глобальные переменные
graph = []  # Матрица смежности
pairU = []  # Массив пар для левой части графа
pairV = []  # Массив пар для правой части графа
dist = []  # Массив расстояний
n, m = 0, 0  # Количество вершин в левой и правой части графа


# Поиск в ширину (BFS)
def bfs():
    queue = []
    for i in range(n):
        if pairU[i] == -1:
            dist[i] = 0
            queue.append(i)
        else:
            dist[i] = float('inf')

    dist[n] = float('inf')

    front = 0
    while front < len(queue):
        u = queue[front]
        front += 1
        if dist[u] < dist[n]:
            for v in range(m):
                if graph[u][v] and dist[pairV[v]] == float('inf'):
                    dist[pairV[v]] = dist[u] + 1
                    queue.append(pairV[v])

    return dist[n] != float('inf')


# Поиск в глубину (DFS)
def dfs(u):
    if u != -1:
        for v in range(m):
            if graph[u][v] and dist[pairV[v]] == dist[u] + 1:
                if dfs(pairV[v]):
                    pairV[v] = u
                    pairU[u] = v
                    return True
        dist[u] = float('inf')
        return False
    return True


# Алгоритм Хопкрофта-Карпа
def hopcroft_karp():
    global pairU, pairV, dist
    pairU = [-1] * n
    pairV = [-1] * m
    dist = [0] * (n + 1)

    matching = 0
    while bfs():
        for u in range(n):
            if pairU[u] == -1 and dfs(u):
                matching += 1
    return matching


# Функция для генерации случайной матрицы смежности
def generate_random_graph():
    random.seed(time.time())
    for i in range(n):
        for j in range(m):
            graph[i][j] = random.randint(0, 1)


# Функция для ввода матрицы вручную
def input_graph():
    print("Введите матрицу смежности (где 1 — ребро, 0 — отсутствие ребра):")
    for i in range(n):
        for j in range(m):
            while True:  # Цикл для проверки правильности ввода
                try:
                    value = int(input(f"graph[{i}][{j}]: "))
                    if value in [0, 1]:
                        graph[i][j] = value
                        break  # Прерываем цикл, если ввод правильный
                    else:
                        print("Некорректный ввод. Введите 0 или 1.")
                except ValueError:
                    print("Некорректный ввод. Пожалуйста, введите число 0 или 1.")



# Функция для сохранения результата в файл results.txt
def save_results(max_matching):
    # Сохранение результатов в файл
    with open("results.txt", "a") as file:
        file.write("------------------------------------\n")
        file.write(f"Кол-во вершин в левой части графа: {n}\n")
        file.write(f"Кол-во вершин в правой части графа: {m}\n\n")

        file.write("Матрица смежности:\n")
        for i in range(n):
            file.write(" ".join(map(str, graph[i])) + "\n")

        file.write(f"\nРазмер наибольшего паросочетания: {max_matching}\n")

        file.write("\nСвязь между вершинами (Un; Vm):\n")
        for i in range(n):
            if pairU[i] != -1:
                file.write(f"(U{i}; V{pairU[i]})\n")

    # Вывод результатов в консоль
    print("\nМатрица смежности:")
    for i in range(n):
        print(" ".join(map(str, graph[i])))  # Выводим строку матрицы в консоль
    print(f"\nРазмер наибольшего паросочетания: {max_matching}")
    print("\nСвязь между вершинами (Un; Vm):")
    for i in range(n):
        if pairU[i] != -1:
            print(f"(U{i}; V{pairU[i]})")

    print("\nРезультаты сохранены в файл results.txt.")


# Основная программа
def main():
    global n, m, graph

    cont = 1

    while cont:
        print("Меню:")
        print("1. Ввести матрицу смежности вручную")
        print("2. Генерировать случайную матрицу смежности")
        print("3. Выход")
        option = int(input("Выберите опцию: "))

        if option == 3:
            break
        elif option != 1 and option != 2:
            print("Неверный выбор. Попробуйте снова.")
            continue

        n = int(input("Введите количество вершин в левой части графа: "))
        m = int(input("Введите количество вершин в правой части графа: "))

        # Инициализация графа
        graph = [[0] * m for _ in range(n)]

        if option == 1:
            input_graph()
        elif option == 2:
            generate_random_graph()

        # Вычисление максимального паросочетания
        max_matching = hopcroft_karp()

        # Сохранение результата в файл
        save_results(max_matching)

        # Повторить?
        cont = int(input("\nХотите повторить? (1 - да, 0 - нет): "))

    print("Программа завершена.")


if __name__ == "__main__":
    main()

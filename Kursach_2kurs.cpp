#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <locale.h>

#define MAX_NODES 1000  // Максимальное количество вершин

int graph[MAX_NODES][MAX_NODES];  // Граф, представленный матрицей смежности
int pairU[MAX_NODES], pairV[MAX_NODES];  // Массивы пар
int dist[MAX_NODES];  // Массив расстояний
int n, m;  // Количество вершин в двух частях двудольного графа

// Поиск в ширину (BFS)
int bfs() {
    int queue[MAX_NODES], front = 0, rear = 0;

    for (int i = 0; i < n; i++) {
        if (pairU[i] == -1) {
            dist[i] = 0;
            queue[rear++] = i;
        }
        else {
            dist[i] = INT_MAX;
        }
    }

    dist[-1] = INT_MAX;

    while (front < rear) {
        int u = queue[front++];
        if (dist[u] < dist[-1]) {
            for (int v = 0; v < m; v++) {
                if (graph[u][v] && dist[pairV[v]] == INT_MAX) {
                    dist[pairV[v]] = dist[u] + 1;
                    queue[rear++] = pairV[v];
                }
            }
        }
    }

    return dist[-1] != INT_MAX;
}

// Поиск в глубину (DFS)
int dfs(int u) {
    if (u != -1) {
        for (int v = 0; v < m; v++) {
            if (graph[u][v] && dist[pairV[v]] == dist[u] + 1) {
                if (dfs(pairV[v])) {
                    pairV[v] = u;
                    pairU[u] = v;
                    return 1;
                }
            }
        }
        dist[u] = INT_MAX;
        return 0;
    }
    return 1;
}

// Алгоритм Хопкрофта-Карпа
int hopcroftKarp() {
    memset(pairU, -1, sizeof(pairU));
    memset(pairV, -1, sizeof(pairV));

    int matching = 0;
    while (bfs()) {
        for (int u = 0; u < n; u++) {
            if (pairU[u] == -1 && dfs(u)) {
                matching++;
            }
        }
    }
    return matching;
}

int main() {
    setlocale(LC_ALL, "RUS");

    // Ввод данных
    printf("Введите количество вершин в левой части графа: ");
    scanf("%d", &n);
    printf("Введите количество вершин в правой части графа: ");
    scanf("%d", &m);

    printf("Введите матрицу смежности (где 1 — ребро, 0 — отсутствие ребра):\n");
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            scanf("%d", &graph[i][j]);
        }
    }

    // Вычисление максимального паросочетания
    int maxMatching = hopcroftKarp();

    // Вывод результата
    printf("Размер наибольшего паросочетания: %d\n", maxMatching);

    return 0;
}

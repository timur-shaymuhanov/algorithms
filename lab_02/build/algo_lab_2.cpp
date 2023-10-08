#include <iomanip>
#include <iostream>
#include <cstring>
#include <random>

using namespace std;

const int INF = INT_MAX; // бесконечность

int main()
{
    int n;
    cin >> n;
    double x[n], y[n];

    // если очень хочется вводить точки руками, можно раскомментить код
    // for (int i = 0; i < n; i++)
    // {
    //     cin >> x[i];
    //     cin >> y[i];
    // }
    // for (int i = 0; i < n; i++)
    // {
    //     cout << fixed << setprecision(2) << "point #" << i + 1 << string(3 - log10(i + 1), ' ') << x[i] << " " << y[i] << endl;
    // }

    // генерим точки случайным образом

    random_device rd;                        // non-deterministic generator
    mt19937 gen(rd());                       // to seed mersenne twister.
    uniform_real_distribution<> dist(0, 10); // distribute results between -10 and 10 inclusive.

    for (int i = 0; i < n; i++)
    {
        x[i] = dist(gen);
        y[i] = dist(gen);

        cout << fixed << setprecision(2) << "point #" << i + 1 << string(3 - log10(i + 2), ' ') << x[i] << " " << y[i] << endl;
    }
    cout << string(10, '-') << endl;

    // создаем матрицу, в которой храним веса (расстояния между точками)

    double dist_matrix[n][n];
    for (int i = 0; i < n; i++)
    {
        for (int j = i; j < n; j++)
        {
            dist_matrix[i][j] = sqrt((x[i] - x[j]) * (x[i] - x[j]) + (y[i] - y[j]) * (y[i] - y[j]));
            dist_matrix[j][i] = sqrt((x[i] - x[j]) * (x[i] - x[j]) + (y[i] - y[j]) * (y[i] - y[j]));
        }
    }

    // если хочется посмотреть на матрицу, можно раскомментить
    // for (int i = 0; i < n; i++)
    // {
    //     for (int j = 0; j < n; j++)
    //     {
    //         cout << fixed << setprecision(2) << dist_matrix[i][j] << " ";
    //     }
    //     cout << endl;
    // }

    /*в качестве динамики (по подмножествам) будем сохранять состояния как оптимальный (на данный момент) вес пути h[mask][node]. Траектория зашифрована
    // в булевском массиве mask, а заканчивается она в вершине node (не отраженной в mask). Для удобства и экономии памяти храним mask как int
    и пользуеммся побитовыми операциями для получения значения нужного бита. mask устроен так: 1 на i-й позиции <=> мы посетили вершину i; 0 <=> не посетили */

    double h[(1 << n)][n]; // здесь храним длины путей

    // изначально ставим все веса = inf
    for (int i = 0; i < (1 << n); i++)
    {
        for (int j = 0; j < n; j++)
        {
            h[i][j] = INF;
        }
    }
    h[0][0] = 0;       // стартуем нулевой вершины
    double best = INF; // сюда будем собирать ответ

    for (int mask = 0; mask < (1 << n); mask++) // перебираем маски
    {
        for (int u = 0; u < n; u++) // перебираем конечные точки
        {
            if (h[mask][u] != INF) // идем только туда, где еще не были - здесь мы и отходим от факториальной сложности
            {
                int new_mask = mask | (1 << u); // перебираем кандидатов, для этого обновляем траекторию в new_mask, записывая посещение вершины u

                for (int v = 0; v < n; v++) // перебираем кандидатов на следующий шаг
                {
                    double w = dist_matrix[u][v]; // записываем вес следующего шага

                    if (!((new_mask >> v) & 1)) // смотрим только туда, где еще не были
                    {
                        if (h[mask][u] + w < h[new_mask][v]) // если нашли более оптимальный путь к вершине v, переписываем значение в h
                        {
                            h[new_mask][v] = h[mask][u] + w;
                        }
                    }
                    if ((v == 0) && (new_mask == (1 << n) - 1) && (h[mask][u] + w < best)) // если посетили всех и вернулись в начало дешевле, чем умели раньше, обновляем ответ
                    {
                        best = h[mask][u] + w;
                    }
                }
            }
        }
    }

    cout << "best = " << best << endl;

    // // если хочется посмотреть, что у нас получилось в h, можно раскомментить следующий код
    // for (int i = 0; i < (1 << n); i++)
    // {
    //     for (int j = 0; j < n; j++)
    //     {
    //         if (h[i][j] == INF)
    //         {
    //             cout << " INF ";
    //         }
    //         else
    //         {
    //             cout << fixed << setprecision(2) << h[i][j] << " ";
    //         }
    //     }
    //     cout << endl;
    // }


}
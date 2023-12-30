import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

relabel_map = {(0, 0): 'A', (0, 1): 'B', (0, 2): 'C', (0, 3): 'D', (1, 0): 'E', (1, 1): 'F', (1, 2): 'G', (1, 3): 'H',
               (2, 0): 'I', (2, 1): 'J', (2, 2): 'K', (2, 3): 'L', (3, 0): 'M', (3, 1): 'N', (3, 2): 'O', (3, 3): 'P'}


class Car:
    def __init__(self, g: nx.DiGraph):

        self.graph = g
        self.generate_path(4)

    def generate_path(self, max_len: int):
        self.start = random.choice(list(self.graph.nodes()))

        if not list(self.graph.successors(self.start)):
            while not list(self.graph.successors(self.start)):
                self.start = random.choice(list(self.graph.nodes()))

        self.path = [self.start]

        for i in range(max_len):
            node = self.path[-1]
            nxt = random.choice(list(self.graph.successors(node)))
            self.path.append(nxt)
            if not list(self.graph.successors(nxt)):
                break

        self.stop = self.path[-1]
        self.index_in_path = 0
        self.current_edge = (self.path[self.index_in_path], self.path[self.index_in_path + 1])

    def update(self):
        self.index_in_path += 1
        self.current_edge = (self.path[self.index_in_path], self.path[self.index_in_path + 1])

    def get_next_edge(self):
        if self.index_in_path < len(self.path) - 2:
            return self.path[self.index_in_path], self.path[self.index_in_path + 1]
        else:
            return None

    def __repr__(self):
        return f"\n From: {self.start} \n To: {self.stop} \n Path: {self.path}"


class Model(nx.Graph):
    def __init__(self, n, m, opt=False):
        super().__init__()

        G0 = nx.grid_2d_graph(n, m)

        # создание направленных ребер
        for (u, v) in G0.edges():
            direct = random.choice([True, False])
            G0[u][v]['flag'] = direct

        # создание списка ребер с направлениями
        edges = []
        for (u, v) in G0.edges(data=False):
            edges.append((u, v))


        for (u, v, data) in G0.edges(data=True):
            if data['flag']:
                edges.append((v, u))

        # создание направленного графа
        self.graph = nx.DiGraph()
        self.graph.add_edges_from(edges)
        self.n = n
        self.m = m

        # self.graph = nx.grid_2d_graph(n, m)
        print(f"num_of_edges = {len(self.graph.edges)}")
        # self.graph = nx.relabel_nodes(self.graph, relabel_map)
        for (u, v) in self.graph.edges:
            self.graph.edges[u, v]['max_load'] = 100
            self.graph.edges[u, v]['current_load'] = 0
            self.graph.edges[u, v]['processed'] = 0

        self.can_process = 15
        self.optimizer = opt
        self.g_edges = [(u, v) for (u, v, d) in self.graph.edges(data=True)]
        self.y_edges = []
        self.r_edges = []
        self.top_loaded = []
        self.time = 0
        self.num_gen_start = 200
        self.num_gen_step = 100
        self.cars = []
        self.text = f"Optimizer: {self.optimizer}"
        self.gen_cars(self.num_gen_start)

    def gen_cars(self, num):
        for i in range(num):
            car = Car(self.graph)

            if self.graph.edges[car.current_edge]['current_load'] <= 99:
                self.cars.append(car)
                self.graph.edges[car.current_edge]['current_load'] += 1

            else:
                # print("overloaded")
                continue

    def update_model(self):
        self.loads = []

        self.top_loaded = []
        self.gen_cars(self.num_gen_step)

        new_graph = self.graph.copy()
        for edge in new_graph.edges:
            new_graph.edges[edge]["processed"] = 0

            if self.optimizer:
                edge_cars = [car for car in self.cars if
                             new_graph.edges[edge]["current_load"] >= 90 and car.current_edge == edge]
                if edge_cars:
                    #print(f"Deleting cars: {len(edge_cars)}")
                    self.cars = list(set(self.cars) - set(edge_cars))
                    new_graph.edges[edge]["current_load"] -= len(edge_cars)

        for car in self.cars:
            edge = new_graph.edges[car.current_edge]

            # print(car.get_next_edge())

            if car.get_next_edge() is None:
                edge['current_load'] -= 1
                # print("car arrived")
                self.cars.remove(car)
                continue

            elif car.get_next_edge() and new_graph.edges[car.get_next_edge()]['current_load'] <= 99 and \
                    edge['processed'] < self.can_process:

                #print(f"current load = {new_graph.edges[car.get_next_edge()]['current_load']}")
                edge['current_load'] -= 1
                edge['processed'] += 1
                car.update()
                new_graph.edges[car.current_edge]['current_load'] += 1

        for edge in new_graph.edges:
            if new_graph.edges[edge]["current_load"] > new_graph.edges[edge]["max_load"]:
                new_graph.edges[edge]["current_load"] = new_graph.edges[edge]["max_load"]
            if new_graph.edges[edge]["current_load"] < 0:
                new_graph.edges[edge]["current_load"] = 0

        self.graph = new_graph.copy()

        sorted_loads = sorted(self.graph.edges(data=True), key=lambda x: x[2]['current_load'], reverse=True)

        self.top_loaded = f""
        for edg in sorted_loads[:10]:
            if edg[2]['current_load'] >= 50:
                self.top_loaded += f"{edg[0]} -- {edg[1]}: {edg[2]['current_load']}, time_for_solve: {int((edg[2]['current_load'] - 50)/self.can_process)+1} \n"


        self.g_edges = [(u, v) for (u, v, d) in self.graph.edges(data=True) if 0 <= d["current_load"] < 50]
        self.y_edges = [(u, v) for (u, v, d) in self.graph.edges(data=True) if 50 <= d["current_load"] < 90]
        self.r_edges = [(u, v) for (u, v, d) in self.graph.edges(data=True) if 90 <= d["current_load"] <= 100]

        self.time += 1

        if (10 < self.time <= 20) or (60 < self.time <= 70):
            self.num_gen_step = 250
            self.text = f"Optimizer: {self.optimizer} \n Time: {self.time} \n" + "RUSH HOUR\n"
            if self.top_loaded:
                self.text += "\nTOP-LOADED\n" + self.top_loaded
        else:
            self.num_gen_step = 150
            self.text = f"Optimizer: {self.optimizer} \n Time: {self.time} \n"
            if self.top_loaded:
                self.text += "\nTOP-LOADED\n" + self.top_loaded

        if self.time >= 99:
            print("SIMULATION FINISHED")
            exit()


def update_graph(i):
    G.update_model()
    ax1.clear()
    pos = {(i, j): (i, j) for i in range(G.n) for j in range(G.m)}
    # edges
    nx.draw_networkx_edges(G.graph, pos, ax=ax1, edgelist=G.g_edges, edge_color='g', width=3, connectionstyle="arc3,rad=0.1")
    nx.draw_networkx_edges(G.graph, pos, ax=ax1, edgelist=G.y_edges, edge_color='y', width=3, connectionstyle="arc3,rad=0.1")
    nx.draw_networkx_edges(G.graph, pos, ax=ax1, edgelist=G.r_edges, edge_color='r', width=3, connectionstyle="arc3,rad=0.1")

    # nodes
    nx.draw_networkx_nodes(G.graph, pos, ax=ax1, node_size=70)

    # labels
    edge_labels = nx.get_edge_attributes(G.graph, "current_load")
    nx.draw_networkx_edge_labels(G.graph, pos, edge_labels, ax=ax1, label_pos=0.2, font_size=8)
    # nx.draw_networkx_labels(G.graph, pos, font_size=12, font_family="sans-serif")


def update_text(num):
    # Генерируем случайное число и обновляем текст во втором subplot
    ax2.clear()
    ax2.text(0.5, 0.5, G.text, ha='center', fontsize=15)


# создаем граф
G = Model(4, 4, opt=True)
fig, (ax2, ax1) = plt.subplots(1, 2, figsize=(20, 10))
ax1.axison = False
ax2.axison = False
ani1 = animation.FuncAnimation(fig, update_text, interval=500)
ani2 = animation.FuncAnimation(fig, update_graph, interval=500)
# # создаем анимацию
# ani = animation.FuncAnimation(plt.gcf(), animate, frames=1, interval=500)

# выводим анимацию на экран
plt.show()

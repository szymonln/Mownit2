import networkx as nx
import matplotlib.pyplot as plt


def gauss_jordan(m, eps=1.0/(10**10)):
  (h, w) = (len(m), len(m[0]))

  for y in range(0, h):
    mx_pivot_row = y

    for y2 in range(y+1, h):
      if abs(m[y2][y]) > abs(m[mx_pivot_row][y]):
        mx_pivot_row = y2
    (m[y], m[mx_pivot_row]) = (m[mx_pivot_row], m[y])

    if abs(m[y][y]) <= eps:
      print("It happens to be a singular matrix")
      return False

    for y2 in range(y+1, h):
      c = m[y2][y] / m[y][y]
      for x in range(y, w):
        m[y2][x] -= m[y][x] * c

  for y in range(h-1, 0-1, -1):
    c  = m[y][y]

    for y2 in range(0, y):
      for x in range(w-1, y-1, -1):
        m[y2][x] -= m[y][x] * m[y2][y] / c
    m[y][y] /= c
    for x in range(h, w):
      m[y][x] /= c
  return m


cars_in = [80.0, 0.0, 0.0, 100.0]
cars_out = [0.0, 50.0, 130.0, 0.0]


def graph_to_mtx(g):
  matrix = []
  for i in range(len(g)):
    eq = []
    for j in range(len(g[i])):
      if graph[i][j] == 1:
        eq.append(-1.0)
      if graph[j][i] == 1:
        eq.append(1.0)
      if graph[j][i] == 0 and graph[i][j] == 0:
        eq.append(0.0)
    eq.append(cars_in[i]*-1.0 + cars_out[i])
    matrix.append(eq)
  return matrix


# A graph is represented as a list of edges [(Root, Destination), ...]
edges = [(0, 1), (0, 2), (1, 2), (3, 2), (3, 0)]
edges_values = []
nodes = [0, 1, 2, 3]

equation = []

for n in nodes:
  eqn = []
  for e in edges:
    if e[0] == n:
      eqn.append(-1.0)
    if e[1] == n:
      eqn.append(1.0)
    if e[0] != n and e[1] != n:
      eqn.append(0.0)
  eqn.append(cars_out[n] + cars_in[n]*(-1))
  equation.append(eqn)

print(equation)
print(gauss_jordan(equation))
print(equation)

G = nx.DiGraph()
G.add_edges_from(edges)
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_size=500)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='r', arrows=True)

plt.show()


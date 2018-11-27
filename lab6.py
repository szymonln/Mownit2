import numpy as np
from scipy import linalg
import time


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


# LU BENCHMARK
start = time.time()
A = np.array(
    [[1.0, 3.0, 4.0, 2.0],
    [3.0, 0.0, -2.0, 1.0],
    [8.0, 10.0, 22.0, -5.0],
    [0.0, 3.0, 12.0, 1.0]]
    )

b = np.array(
    [6.0,
     12.0,
    -10.0,
     5.0]
    )

P, L, U = linalg.lu(A)
Y = linalg.solve_triangular(L, b, lower=True)
X = linalg.solve_triangular(U, Y)
end = time.time()
print(str(A) + " * " + str(X) + " = " + str(b))
print("****LU TIME: {}".format(end-start))


# GAUSS JORDAN BENCHMARK
start = time.time()

matrix = [[1.0, 3.0, 4.0, 2.0, 6.0],
          [3.0, 0.0, -2.0, 1.0, 1.0],
          [8.0, 10.0, 22.0, -5.0, -5.0],
          [0.0, 3.0, 12.0, 1.0, 1.0]]

if gauss_jordan(matrix):
    end = time.time()
    print("****OWN GAUSS TIME: {}".format(end - start))
else:
    print("GAUSS FAILED")
print(matrix)


# LIBRARY SOLVE
start = time.time()

X = linalg.solve(A, b)
end=time.time()
print("****LIBRARY GAUSS TIME: {}".format(end - start))
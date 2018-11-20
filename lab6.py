import numpy as np
from scipy import linalg

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

print(A.dot(b))

Y = linalg.solve_triangular(L, b, lower=True)
X = linalg.solve_triangular(U, Y)
print(X)




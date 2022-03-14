import numpy as np

M = np.arange(5, 21)
print(M, end ='\n\n')

M = M.reshape(4,4)
print(M, end ='\n\n')

M[1:3, 1:3] = 0
print(M, end ='\n\n')

M = M@M
print(M, end ='\n\n')

v = np.sqrt(M[0]@M[0].T)
print(v)

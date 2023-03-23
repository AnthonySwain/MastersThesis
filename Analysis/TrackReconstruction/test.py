import numpy as np

# create a 2D numpy array
a = np.array([[1, 2], [3, 4], [5, 6]])
print(a)
# create a 1D numpy array to divide the matrix by
b = np.array([[2], [3]])
print(b)
# divide the matrix by the array using broadcasting
result = a / b.T
#print(b[:,np.newaxis])
print(result)
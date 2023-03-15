import h5py
import numpy as np

with h5py.File('SO_57342918_h5py.h5','w') as h5f:

    i_arr=np.arange(10)
    x_arr=np.arange(10.0)

    my_dt = np.dtype([ ('i_arr', int), ('x_arr', float) ] )
    table_arr = np.recarray( (10,), dtype=my_dt )
    table_arr['i_arr'] = i_arr
    table_arr['x_arr'] = x_arr

    my_ds = h5f.create_dataset('/ds1',data=table_arr)

# read 1 column using numpy slicing: 
with h5py.File('SO_57342918_h5py.h5','r') as h5f:

    h5_i_arr = h5f['ds1'][np.arange(5)]
    h5_x_arr = h5f['ds1'][:,'x_arr']
    print (h5_i_arr)
    print (h5_x_arr)
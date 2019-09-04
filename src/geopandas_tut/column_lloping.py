"""
 Created on 31 Aug 2019
"""
import numpy as np
import pandas as pd

# prepare data
headers = ['Time','A_x','A_y', 'A_z', 'B_x','B_y','B_z']
df = pd.DataFrame(np.random.randn(10,7),index=range(1,11),columns=headers)
print(df.head())

# make matrix
arr = df.values
print('arr\n', arr.shape, arr)

times = arr[:,0]
print('times\n', times.shape, times)

arr = arr[:,1:]
print('arr1\n', arr.shape, arr)

result = np.sqrt((arr**2).reshape(arr.shape[0],-1,3).sum(axis=-1))/times[:,None]
print("result\n ", result.shape, result)
result = pd.DataFrame(result, columns=['Velocity_%s'%(x,) for x in list('AB')])
print(result)
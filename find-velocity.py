import pandas as pd
import numpy as np

df = pd.read_csv('yC31-speed.csv')

print 'velocity', np.mean(np.linalg.norm(df[['xdt', 'ydt', 'zdt']].values,axis=1))

print 'density', df['rho'].mean()

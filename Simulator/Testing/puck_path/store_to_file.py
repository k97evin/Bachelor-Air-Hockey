import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path


path =  Path(__file__).parent
#path = os.path.join(path,r'Angles.csv')

Angles = {'AngleInn': [1.728,1.885,2.042,2.199,2.356,2.513,2.670,2.827,2.985],
          'AngleOut': [1.754,1.934,2.108,2.275,2.434,2.585,2.730,2.870,3.007]
        }

df = pd.DataFrame(Angles, columns= ['AngleInn', 'AngleOut'])

df.to_csv(path/'Angles.csv',index = False, header=True)

print(df)
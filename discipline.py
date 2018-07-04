import pandas as pd
import numpy as np

f2 = open("专业.txt", 'r')
test = pd.read_table(f2, header=None, sep="\n", quoting=3, error_bad_lines=False)
test = np.mat(test)




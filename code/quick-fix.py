import pandas as pd
import sys
import os
abs_file_path = os.path.abspath(__file__)
file_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(file_dir)

one_city = "fsa_toronto"
one_fsa = "M5B"

old = pd.read_csv( project_dir + '/data-raw/doctors-' + one_fsa + '.csv', header = 0, names = ['CPSO','article'] )

old['one_city'] = "fsa_toronto"
old['one_fsa'] = "M5B"

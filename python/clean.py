import pandas as pd
import numpy as np

def CleanGender(dfSeries):
	return dfSeries.map( {'female': 0, 'male': 1} ).astype(int)


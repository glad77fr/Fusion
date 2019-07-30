import pandas as pd
import re
import numpy as np
from datetime import date
from datetime import datetime

def convert_date(data):
    try:
       return datetime.strptime(str(data),'%d/%m/%Y')
    except:
        pass

def correct_typing(dataframe):
    nb_columns = len(dataframe.columns)
    r = re.compile(r"^\d*[.,]\d*$")
    j = re.compile(r'^\d*$')
    for y in range(nb_columns):
       for i in range(len(dataframe)):
           if pd.notna(dataframe.iat[i,y]):
               if len(str(dataframe.iat[i,y])) == 10 and str(dataframe.iat[i,y]).count('/') == 2: # Test if is a datetime
                  dataframe[dataframe.columns[y]] = dataframe[dataframe.columns[y]].apply(lambda x: convert_date(x))
                  dataframe[dataframe.columns[y]] = dataframe[dataframe.columns[y]].dt.date
                  break

               if r.match(str(dataframe.iat[i, y])):
                   dataframe[dataframe.columns[y]] = dataframe[dataframe.columns[y]].apply(lambda x: str(x).replace(",", "."))
                   dataframe[dataframe.columns[y]] = dataframe[dataframe.columns[y]].astype('float64')
                   break

               if j.match(str(dataframe.iat[i, y])) and (dataframe[dataframe.columns[y]].dtypes == np.int64) == False:
                   try:
                        dataframe[dataframe.columns[y]] = dataframe[dataframe.columns[y]].apply(lambda x: str(x).replace(",", "."))
                        dataframe[dataframe.columns[y]] = dataframe[dataframe.columns[y]].apply(lambda x: float(x))

                   except ValueError:
                        print("Problème de convertion dans sur la colonne " + dataframe.columns[y])
                        pass
               break

    return dataframe
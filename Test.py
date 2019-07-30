import pandas as pd

toto = pd.DataFrame({'Name' :["Mike","John","Mike","Serge"], 'Age':[34,13,46,34]})


liste = ["John","Serge"]

position = toto[(toto["Name"].isin(liste)) & (toto["Age"]>20)].index

print(position)

for val in position:
    toto.at[val, "test"] = "COOOL"


print(toto)
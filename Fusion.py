import pandas as pd
import Correct_typing
from datetime import datetime

class fusion:

    def __init__(self, config_file):
        try :
            self.config_file = pd.read_excel(config_file)
        except FileNotFoundError :
            print("Problème de chargement de fichier de configuration")
            exit()
        self.data = {} #Stock les dataframes
        self.chargements_dataframe()
        self.date_result()

    def chargements_dataframe(self):

        for i, val in enumerate(self.config_file["Répertoire"]):
            if str(val)[-4:] != "xlsx":
                print("problème de format")
            else :
                self.config_file.at[i, "Dataframe"] = val.split('\\')[-1][:-5]

        for i, val in enumerate(self.config_file.itertuples()):
            self.data[self.config_file.at[i, "Dataframe"]] = pd.read_excel(self.config_file.at[i,"Répertoire"])

        for key, value in self.data.items():
            self.data[key] = Correct_typing.correct_typing(value)


    def control_date(self, dataframe, mat, beg_date, end_date): # Méthode contenant les contrôles de cohérence des dates

        dataframe = dataframe[[mat, beg_date, end_date]]
        dataframe = dataframe.sort_values([mat, beg_date])

        #Controle de chevauchement d'historique
        for i, val in enumerate(dataframe[mat]):
            try:
                if pd.notna(dataframe.at[i, end_date]):
                    if dataframe.at[i, mat] == dataframe.at[i+1, mat]:
                        if dataframe.at[i, end_date] > dataframe.at[i, beg_date]:
                            dataframe.at[i, "Anomalie"] = "Chevauchement de date"
            except:
                pass

        # Controle plusieurs lignes valide en même temps
        dataframe_last_occurence = dataframe[dataframe[end_date].isna()]
        dataframe_last_occurence = dataframe_last_occurence[mat].value_counts(dropna=False)
        list_anomalie = dataframe_last_occurence[dataframe_last_occurence>1]
        list_anomalie = list_anomalie.index.tolist()
        anomalie_pos = dataframe[(dataframe[mat].isin(list_anomalie)) & ((dataframe[end_date].isnull()))].index
        print(anomalie_pos)

        for val in anomalie_pos:

         if dataframe.at[val,"Anomalie"] =="nan":
                dataframe.at[val,"Anomalie"]= "Plusieurs lignes valides"
         else:
             dataframe.at[val,"Anomalie"] = str(dataframe.at[val,"Anomalie"]) + " /Plusieurs lignes valides"
        return dataframe

    def date_result(self):
        dataframe = {}
        for i, val in enumerate(self.config_file.itertuples()):
            dataframe[self.config_file.at[i, "Dataframe"]] = self.control_date(self.data[self.config_file.at[i,"Dataframe"]], self.config_file.at[i, "Intitulé du champ matricule"], self.config_file.at[i, "Champ début"], self.config_file.at[i, "Champ fin"])

        def dfs_tabs(df_list, sheet_list, file_name):
            writer = pd.ExcelWriter(file_name, engine='xlsxwriter',datetime_format='dd/mm/yyyy')
            for dataframe, sheet in zip(df_list, sheet_list):
                try:
                    dataframe = dataframe.sort_values(["Anomalie"])
                except:
                    pass

                dataframe.to_excel(writer, sheet_name=sheet, index=False)
                worksheet = writer.sheets[sheet]
                worksheet.set_column('A:D', 25)
            writer.save()

        df_list = [x for x in dataframe.values()]
        sheet_list = [x for x in dataframe.keys()]
        file_name = r'C:\Users\Sabri.GASMI\Desktop\Anomalies.xlsx'
        dfs_tabs(df_list,sheet_list,file_name)




test = fusion(r'C:\Users\Sabri.GASMI\Desktop\Fusion_file.xlsx')




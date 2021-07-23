import pandas as pd
import numpy as np

class Query:
    not_col = False

    def __init__(self,df_dict):
        self.dictionary = df_dict
        self.preprocess_dictionary()

    #Actions in Dictionary

    # Check for a NOT column
    def NOT_col_check(self):
        self.not_col = 'NOT' in self.dictionary.columns

    #Repalce blank spaces with NaN
    def replace_blank_with_nan(self):
        self.dictionary.replace("", np.nan, inplace=True) # replace empty string with np.nan

    #Change position of the NOT column
    def NOT_col_last(self):
        NOT = self.dictionary['NOT']
        self.dictionary.drop(columns=['NOT'], inplace=True)
        self.dictionary['NOT'] = NOT

    #Preprocess dict
    def preprocess_dictionary(self):
        self.NOT_col_check()
        self.replace_blank_with_nan()
        if self.not_col:
            self.NOT_col_last()

    #Actions in Dictionary Temp

    # Combine columns given in col_list
    def combine_columns(self, col_list):
            df_combined = self.dictionary
            col_pivot= col_list[0]

            for c in col_list[1:]:
                for val  in self.dictionary[c]:
                    df_combined = df_combined.append({col_pivot:val}, ignore_index=True)

                df_combined.drop(c,axis=1, inplace=True)

            df_combined.rename(columns={col_pivot:'(' + ' OR '.join(col_list) + ')'},inplace=True)

            self.dictionary = df_combined

    # Join values in a column with OR
    def join_col_vals_OR(self):
        df_temp = self.dictionary
        query_list = [] #lista de palabras concatenadas por OR
        num_cols = np.shape(df_temp)[1] #número de columnas en el documento

        for i in range(num_cols):
            col_val = df_temp.iloc[:,i].dropna().values #valores de la columna filtrando NaN

            if len(col_val)==0:
                print("Columna {} : {} --> VACÍA".format(i,df_temp.columns[i]))
                continue
            for j in range(len(col_val)):
                if col_val[j][0] == "\"":
                    continue
                else:
                    col_val[j] = '('+ col_val[j] + ')'

            query_list.append('(' + ' OR '.join(col_val) + ')') #une los valores con un OR y los agrega a la lista query_list

        return query_list

    # Join column with AND in a query.
    #In case NOT colum exist it goes last and is joined with NOT.
    def get_query(self, twitter_filter=True):
        query_list = self.join_col_vals_OR()

        if self.not_col:
            query = '(' + ' AND '.join(query_list[:-1]) + ' NOT ' + query_list[-1] + ')'

        else:
            query = '(' + ' AND '.join(query_list[:]) + ')'

        if twitter_filter:
            query = query + ' AND metaData.source.socialOriginType:“twitter”' #Filter for twitter only

        else:
            query = query[1:-1]
            
        return query

    #Print the logic expression of the query
    def get_logic_expression(self):
        return ' AND '.join(self.dictionary.columns)

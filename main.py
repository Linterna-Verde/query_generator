from spreadsheet import SpreadSheet
from query import Query
import streamlit as st
#import st_state_patch

import numpy as np
from PIL import Image
from pathlib import Path

#DIRECTORIES
BASE_DIR = Path.cwd()
IMAGES_DIR = BASE_DIR / 'images'

#CREDENTIALS
SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive',
         'https://www.googleapis.com/auth/drive.file']

linterna_logo =  Image.open(IMAGES_DIR/'linterna_logo.jpg')

#sections
header = st.beta_container()
body = st.beta_container()

#st.beta_set_page_config(layout="wide")

with header:

    st.image(linterna_logo)
    st.write('\n'*2)
    col1, col2, col3 = st.beta_columns([0.5,3,0.5])
    col2.title('GENERADOR DE QUERIES')
    st.write('\n'*2)
    st.write('**NOTA:** para que funcione la aplicación debe compartirse el documento de Drive en donde está el diccionario con el siguiente correo: <ins>scrapper@prueba-scapper.iam.gserviceaccount.com </ins>',unsafe_allow_html=True)

with body:
    # GET DATA
    st.write('## Cargar el diccionario')

    url = 'https://docs.google.com/spreadsheets/d/1iilHcaQqvJj6ShrnIbRFlKeqjaCnoNxoza11WGuYwps/edit#gid=0'
    url = st.text_input('Inserte URL del diccionario:', url)

    try:
        spreadsheet = SpreadSheet(SCOPES, st.secrets["gcp_service_account"], url)
        df = spreadsheet.dict_to_df()
        cols = list(df.columns.values)
    except:
        st.error('Ingrese una URL válida.')

    #SELECT DATA
    st.write('## Seleccionar columnas')
    usr_cols = st.multiselect('Columnas' ,cols, default=cols, key='General')

    st.write(df[usr_cols])

    #GROUP BY COLUMN
    st.write('## Agrupar columnas')
    col1, col2 = st.beta_columns(2)
    group1 = col1.multiselect('Grupo 1', usr_cols, default=None, key='group1')
    group2 = col2.multiselect('Grupo 2', list(set(usr_cols).difference(group1)), default=None, key='group2')

    query = Query(df)
    query.preprocess_dictionary()

    for g in [group1,group2]:
        if len(g) != 0:
            query.combine_columns(g)


    # PRINT LOGICAL EXPRESION
    st.write('## Estructura lógica ')
    st.write(query.get_logic_expression())

    if st.button('Generar query'):
        #PRINT & APPEND QUERY
        st.write('## Query ' + ':snake:')

        query_text = query.get_query()
        st.write(query_text)

        if st.button('Agregar al documento de Drive'):
            spreadsheet.append_query_to_spreadsheet(query_text)

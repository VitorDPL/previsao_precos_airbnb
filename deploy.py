# !pip install streamlit

import pandas as pd
import streamlit as st
import joblib


# ['host_is_superhost', 'host_listings_count', 'latitude', 'longitude',
#        'accommodates', 'bathrooms', 'bedrooms', 'beds', 'price',
#        'extra_people', 'minimum_nights', 'instant_bookable',
#        'is_business_travel_ready', 'numero_amenities',
#        'property_type_Apartment', 'property_type_Bed and breakfast',
#        'property_type_Condominium', 'property_type_Guest suite',
#        'property_type_Guesthouse', 'property_type_Hostel',
#        'property_type_House', 'property_type_Loft', 'property_type_Outros',
#        'property_type_Serviced apartment', 'room_type_Entire home/apt',
#        'room_type_Hotel room', 'room_type_Private room',
#        'room_type_Shared room', 'bed_type_Outros', 'bed_type_Real Bed',
#        'cancellation_policy_Outros', 'cancellation_policy_flexible',
#        'cancellation_policy_moderate',
#        'cancellation_policy_strict_14_with_grace_period',
#        'property_type_Apartment', 'property_type_Bed and breakfast',
#        'property_type_Condominium', 'property_type_Guest suite',
#        'property_type_Guesthouse', 'property_type_Hostel',
#        'property_type_House', 'property_type_Loft', 'property_type_Outros',
#        'property_type_Serviced apartment', 'room_type_Entire home/apt',
#        'room_type_Hotel room', 'room_type_Private room',
#        'room_type_Shared room', 'bed_type_Outros', 'bed_type_Real Bed'],
#       dtype='object')

# valores numéricos
x_numericos = {'latitude': 0, 'longitude': 0, 'accommodates': 0, 'bathrooms': 0, 'bedrooms': 0, 'beds': 0, 'extra_people': 0,
               'minimum_nights': 0, 'ano': 0, 'mes': 0, 'n_amenities': 0, 'host_listings_count': 0}

# true or false
x_tf = {'host_is_superhost': 0, 'instant_bookable': 0}

# características
x_listas = {'property_type': ['Apartment', 'Bed and breakfast', 'Condominium', 'Guest suite', 'Guesthouse', 'Hostel', 'House', 'Loft', 'Outros', 'Serviced apartment'],
            'room_type': ['Entire home/apt', 'Hotel room', 'Private room', 'Shared room'],
            'cancellation_policy': ['flexible', 'moderate', 'strict', 'strict_14_with_grace_period']
            }


dicionario = {}

for item in x_listas:
    for valor in x_listas[item]:
        dicionario[f'{item}_{valor}'] = 0


for item in x_numericos:

    if item == 'latitude' or item == 'longitude':
        # step: de quanto em quanto ele modifica/ varia. Tipo, quando apertamos o botão '+', ele irá variar de 1 em 1, de 0.1 em 0.1, etc.
        # value: em qual casa decimal ele começará. Não pode ser 0 inteiro, tem que ser float.
        # format: teremos 5 casas decimais
        valor = st.number_input(f'{item}', step= 0.00001, value=0.0, format="%.5f")

    elif item == 'extra_people':
        # o padrão do float já são duas casas decimais, por isso n precisamos passar o format.
        valor = st.number_input(f'{item}', step= 0.01, value=0.0)

    else:
        # nesse caso, devemos passar o 0 inteiro mesmo, não float. 
        valor = st.number_input(f'{item}', step= 1, value=0)
        
    # preenchendo os campos de acordo com o que o usuário digitou    
    x_numericos[item] = valor
    

for item in x_tf:
    valor = st.selectbox(f'{item}', ('Sim', 'Não'))
    if valor == 'Sim':
        x_tf[item] = 1
    else:
        x_tf[item] = 0

for item in x_listas:
    valor = st.selectbox(f'{item}', x_listas[item])
    dicionario[f'{item}_{valor}'] = 1

botao = st.button('Prever o valor do imóvel')

if botao:
    dicionario.update(x_numericos)
    dicionario.update(x_tf)
    # o modelo precisa de um dataframe para fazer a previsao. Faremos isso com vários índices 0 ( sem motivo específico).
    valores_x = pd.DataFrame(dicionario, index=[0])

    dados = pd.read_csv('dados.csv')
    # os dados estão vindo com uma coluna a mais "Unnamed: 0", portanto, utilizaremos o fatiamento para remover essa coluna
    colunas = list(dados.columns)[1:-1]
    
    # ordenando as colunas de acordo com as colunas que criamos acima. É basicamente a mesma lista de colunas, só que aqui elas estão ORDENADAS.
    # é porque quando criamos o dicionário, nao nos preocupamos com a ordem das colunas, apenas se elas estavam presentes. Esse código coloca elas em ordem novamente.
    valores_x = valores_x[colunas]
    # modelo_joblib é o nome do arquivo que ta o modelo
    modelo = joblib.load('modelo.joblib')
    preco = modelo.predict(valores_x)

    st.write(preco)

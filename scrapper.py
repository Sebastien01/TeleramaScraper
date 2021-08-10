import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import streamlit as st

@st.cache
def build_df(chaine_tv,date_tv):
    ###Renvoie un dataframe (titre,genre,debut,fin,duree,chaine,jour) à partir d'un' chaine et d'un jour donné###
    
    url = f'https://television.telerama.fr{chaine_tv}?{date_tv}'
    response = requests.get(url)
    json_file = response.content
        
    #On regarde la section TELE
    liste_tv = BeautifulSoup(json_file, "html.parser")\
        .find('div',{'id':'LISTETELE'}).find_all(class_='tv10-chaine-item')
    
    #On récupère le titre, debut, fin et genre de chaque programme dans la section TELE (pour une chaine donnée)    
    date,chaine,titre,debut,fin,genre=[],[],[],[],[],[]
    for programme in liste_tv:
        titre.append(programme.find('h2').text.strip())
        debut.append(programme.find_all(class_='placeholder')[0].string.strip().replace('h',':'))
        fin.append(programme.find_all(class_='placeholder')[1].string.strip().replace('h',':'))
        genre.append(programme.find(class_='tv10-chaine-descri-surt').text.strip())
        chaine.append(re.findall('^(.+?),',chaine_tv.replace('/tele/chaine-tv/',''))[0])
        date.append(date_tv)
    
    #Création du Dataframe, formatage date/heure et ajout d'une feature "durée"
    df = pd.DataFrame({'titre':titre,'debut':debut,'fin':fin,'genre':genre,'chaine':chaine,'jour':date})
    df.debut = df.apply(lambda x: f'{x.jour} {x.debut}',axis=1) #
    df.fin = df.apply(lambda x: f'{x.jour} {x.fin}',axis=1)
    df.debut = pd.to_datetime(df.debut,format=('%Y-%m-%d %H:%M'))
    df.fin = pd.to_datetime(df.fin,format=('%Y-%m-%d %H:%M'))
    df['duree'] = df.fin - df.debut
    
    return df

def get_channels():
    ###Renvoie une liste d'urls car les urls des chaines ont chacun un numero unique (tf1,192.php ; arte,111.php...)###
    resp = requests.get('https://television.telerama.fr/tele/liste_chaines.php')
    soup = BeautifulSoup(resp.content,'html.parser').find(class_='tv10-list-chn')
    
    #On ne regarde que pour 30 chaines principales pour des raisons de calcul
    return [i['href'] for i in soup.find_all(href=True)[:30]] 

def user_vision_dataframe(df):
    ###Retourne une copie du dataframe mais plus lisible pour le lecteur (format date + lisible)###
    df = df.copy()
    df.debut = df.debut.dt.strftime('%H:%M') 
    df.fin   = df.fin.dt.strftime('%H:%M')
    return df
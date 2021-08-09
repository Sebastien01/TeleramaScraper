from requests.api import head
from scrapper import *
import streamlit as st
import datetime
import pandas as pd
from random import randrange


header = st.container()
inputs = st.container()
dataset = st.container()

with header:
    st.title('Telerama Scrapper')

with inputs:
    date = st.date_input('Demandez le programme pour une date précise !')

with dataset:
    df = pd.DataFrame()
    if date != '':
        try :
            st.text('Gathering data, this might take a while..')
            for ch in get_channels():
                try:
                    df = df.append(build_df(ch,date))

                except:
                    pass
            
            today = datetime.datetime.today()
            if date.day == today.day:
                #Aperçu des programmes du moment, avec un pick aléatoire pour le fun
                now = df[(df.debut<today) & (df.fin>today)]
                rand_pick = now.iloc[randrange(0,len(now))]
                restant = (rand_pick.fin - datetime.datetime.today())
                
                #Pour un rendu plus propre pour l'utilisateur
                now.debut = now.debut.dt.strftime('%H:%M') 
                now.fin   =   now.fin.dt.strftime('%H:%M')
                now.set_index('chaine',inplace=True)
                
                st.write(f'Vous êtes en train de rater {rand_pick.titre} sur {rand_pick.chaine}...')
                st.write(f'Vite, il reste {restant.seconds//3600}h et {restant.seconds//60%60}min!')
                st.write(now[['titre','debut','fin']])
            
            else:
                st.write('Lol')
    
            
        except:
            st.subheader("Il semble y avoir une erreur... la date est-elle d'actualité ?")
    
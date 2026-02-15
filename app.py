import streamlit as st
from streamlit_authenticator import Authenticate

import pandas as pd
import csv



def chargement_users():
    lesDonneesDesComptes={}
    #csv.DictReader(f, fieldnames=None, restkey=None, restval=None, dialect='excel', *args, **kwds) 
    # => Create an object that operates like a regular reader but maps the information in each 
    # row to a dict whose keys are given by the optional fieldnames parameter.
    #The fieldnames parameter is a sequence. If fieldnames is omitted, the values in the first row of file f 
    # will be used as the fieldnames and will be omitted from the results. If fieldnames is provided, they will 
    # be used and the first row will be included in the results. 
    with open('data/users.csv', mode='r') as f:
        reader = csv.DictReader(f)      #reader va avoir la forme {'name':'util1','password':'zakou',...}
        users = {}
        for line in reader:
            username=line['name']
            users[username]=line
    lesDonneesDesComptes['usernames']=users
    return lesDonneesDesComptes



    
#on crée une instance d'autentification
authenticator = Authenticate(
    chargement_users(),  # Les données des comptes
    "cookie name",       # Le nom du cookie, c'est un str quelconque
    "cookie key",        # La clé du cookie, c'est un str quelconque
    30,                    # Le nombre de jours avant que le cookie expire
)

#on utilise la méthode login qui affiche automatiquement les champs utilisateurs et mot de pass à saisir
#on peut ajouter des paramètres pour définir le nb max de fois de la saisie des 2, un capcha,...
try:
    #user, status =authenticator.login(location='unrendered',max_login_attempts=3)
    authenticator.login(max_login_attempts=3)
except Exception as e:
    st.error(e)

#une fois que le login est passé, on gère l'accès en fonction des information renseignées

def accueil():
    #configuration de la page 
          
    # ===========================
    # SIDEBAR NAVIGATION
    # ===========================
    
    mon_container_sidebar = st.sidebar.container()
    #mon_containerPage=st.container()  A explorer

    with mon_container_sidebar:
        # Le bouton de déconnexion
        authenticator.logout("Déconnexion")
        mon_user = st.session_state["username"]
        st.write(f"Bienvenue *{mon_user}*")
        page1 = st.button('▷  Accueil :star_struck:', key="bienvenue",type="primary",width='stretch')
        page2 = st.button("▷  Les photos de mes chats",key="LesCats", icon="🐱",icon_position="left", width="stretch",)
        
    if page1 == True:

        #col1, col2 = st.columns(2)
        #with col1:
            st.header("Bienvenue Sur Mon App Spécifiquement dédiée aux chats")
            st.image("images/bravo.jpg",width='stretch')
        #with col2:
        #    st.header("")
      
    if page2 == True:
        st.header("Bienvenue dans l'album de mon chat 🐱")
        p2col1, p2col2, p2col3= st.columns(3)
        with p2col1:
            st.image("images/chat1.jpg",width="stretch")
            st.subheader("Pas mal!")  
        with p2col2:
            st.image("images/chat2.jpg",width="stretch")
            st.subheader("j'adore!")  
        with p2col3:
            st.image("images/chat3.jpg",width="stretch")
            st.subheader("Trop Mignon Le Rouquinou...!")  
      

if st.session_state["authentication_status"]:
    accueil() 

elif st.session_state["authentication_status"] is False:
    st.error("L'username ou le password est/sont incorrect")
elif st.session_state["authentication_status"] is None:
    st.warning('Les champs username et mot de passe doivent être remplie')



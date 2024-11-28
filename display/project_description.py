import streamlit as st
from styles import inject_custom_css, display_text

def project_description():

    col1, _, col2 = st.columns([3,1,1])

    with col1:
        st.image("media/header1.png", width=600)
    
    with col2:
        st.image("media/header2.png", width = 240)

    # Inject custom CSS for the background and text container
    inject_custom_css()

    display_text("Descripció del Projecte", font_size="80px", text_color="rgb(56, 182, 255)", shadow_offset= "4px 4px")
    
    text1 = "Barcelona rep un gran flux de turistes, amb 26 milions de visitants el 2023, fet que exerceix una forta pressió sobre els recursos hídrics, especialment en zones turístiques durant les temporades altes. La gestió d’aigua es complica pel consum addicional dels turistes, afegint variabilitat a les necessitats de la població local. Entendre com aquest turisme influeix en el consum d’aigua és clau per garantir la sostenibilitat dels recursos a llarg termini."

    text2 = "El projecte proposa un model predictiu que combina dades de telelectura de comptadors d’aigua amb informació sobre turisme, climatologia i mobilitat urbana per anticipar el consum d’aigua associat al turisme. Aquesta eina interactiva permet simular el consum en zones específiques de Barcelona en funció del nombre de turistes i altres factors externs, oferint prediccions més precises i dinàmiques. Això ajudarà a AGBAR a gestionar els recursos hídrics de manera més eficient, adaptant-se en temps real als canvis en la demanda."

    text3 = "L'enfocament integra variables externes com el turisme, més enllà del modelatge tradicional, i busca una gestió sostenible dels recursos hídrics. Els resultats esperats inclouen prediccions fiables del consum d’aigua en zones turístiques, optimització de la distribució i reducció de l'impacte ambiental. Aquest projecte no només ofereix una solució innovadora per Barcelona, sinó que també pot ser aplicable a altres ciutats amb dinàmiques similars, contribuint a afrontar reptes globals com el canvi climàtic."

    col1, _, col2 = st.columns([20,1,8])

    with col1:        

        display_text(text1)
        display_text(text2)

        
    with col2:
        st.image("media/bcn.jpg", width=380)
        
    display_text(text3)
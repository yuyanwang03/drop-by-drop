import streamlit as st
from styles import inject_custom_css

def project_description():
    # Inject custom CSS for the background and text container
    inject_custom_css()

    # Title of the project description
    st.title("Descripció del Projecte")

    # Project description text
    text1 = "El projecte aborda la creixent demanda d’aigua a causa del turisme massiu a Barcelona, amb un enfocament en el sector comercial. L’augment del nombre de turistes — 8,27 milions l'any 2023, en contrast amb els 1,62 milions de residents de la ciutat — suposa una càrrega significativa per als recursos hídrics de la ciutat, arribant a representar fins a un 15,68% del consum diari d’aigua."

    text2 = "Davant d’aquesta pressió, especialment durant les temporades turístiques més altes quan la població de la ciutat gairebé es duplica, aquest projecte busca analitzar la petjada hídrica associada al turisme. Mitjançant l’ús de dades històriques i variables externes, l’equip desenvoluparà un model predictiu capaç de pronosticar les fluctuacions en la demanda d’aigua. Els resultats oferiran informació pràctica i recomanacions per a AGBAR per optimitzar la gestió de l’aigua, garantint que Barcelona pugui satisfer de manera sostenible les necessitats tant dels residents com dels turistes."

    text3 = "Aquesta col·laboració amb AGBAR s’alinea amb el nostre objectiu d'aplicar habilitats de ciència de dades i enginyeria a reptes reals, especialment en la gestió de recursos urbans crítics com l’aigua. Els resultats d’aquest projecte contribuiran a la sostenibilitat i resiliència a llarg termini de la ciutat davant el creixement del turisme."

    # Display the project description in a styled text container
    st.markdown(f'<div class="stTextContainer">{text1}</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="stTextContainer">{text2}</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="stTextContainer">{text3}</div>', unsafe_allow_html=True)

import streamlit as st
from styles import inject_custom_css, display_text

def about_us():

    col1, _, col2 = st.columns([3,1,1])

    with col1:
        st.image("media/header1.png", width=600)
    
    with col2:
        st.image("media/header2.png", width = 240)
        

    display_text("Sobre Nosaltres", font_size="80px", text_color="rgb(56, 182, 255)", shadow_offset= "4px 4px")
    text = "Som cinc estudiants d'Enginyeria Matemàtica en Ciència de Dades a l'Universitat Pompeu Fabre. Tenim una sòlida experiència en diversos llenguatges de programació, com ara Python, Java, SQL. La nostra experiència en mineria de dades i el nostre coneixement en Mahcine Learning i inteligència artificial, ens permeten desenvolupar un model predictiu per simular el consum d'aigua."
    
    display_text(text, font_size='22px')



    # Team member details
    team = [
        {
            "name": "Bruno Manzano Clotet",
            "linkedin": "https://www.linkedin.com/in/brunomanzano/",
            "image": "https://media.licdn.com/dms/image/v2/D4D03AQEe9r69YxPhVg/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1702547713065?e=1736380800&v=beta&t=NsDZiX6TL7l1a-ms_8RF1yxUSNJoBREEUPpqSMuU27M", 
        },
        {
            "name": "Iván Hernández Gómez",
            "linkedin": "https://www.linkedin.com/in/iv97n",
            "image": "https://media.licdn.com/dms/image/v2/D5603AQGU6dT73FZacA/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1731424586525?e=1738195200&v=beta&t=bFY_R8uN_EL0Xf64Tc8RX-HUTGROQX5mKqvVdQCQam8",  # Replace with actual URL
        },
        {
            "name": "Martí Oms Graells",
            "linkedin": "https://www.linkedin.com/in/martí-oms-graells",
            "image": "https://media.licdn.com/dms/image/v2/D4E03AQEbY575oX9IAA/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1682176916179?e=1736380800&v=beta&t=accroyrSl_GcfJkH98aTJkGfIAKmYNX7qcbPgjN137U",
        },
        {
            "name": "Paula Manzano Clotet",
            "linkedin": "https://www.linkedin.com/in/paula-mateos-marin-954a90300/",
            "image": "https://media.licdn.com/dms/image/v2/D4D03AQEssjLTI5fjlQ/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1711454757196?e=1736380800&v=beta&t=XOADI__DBoNrkuHGorOjFv7-xoMKOKaKo78s97HZC-w",
        },
        {
            "name": "Yuyan Wang",
            "linkedin": "https://www.linkedin.com/in/yuyanwang03/",
            "image": "https://media.licdn.com/dms/image/v2/D4E03AQHJMsWc_cbqUQ/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1673880445852?e=1736380800&v=beta&t=LWpE_eugEjTgNLJFYmlhP2MgAyxd-xcxiTORK1sDCxw",
        }
    ]

# Create columns
    cols = st.columns(5)

    # Display each team member's image, name, and LinkedIn in two columns per row
    for i, member in enumerate(team):
        col = cols[i]  # Alternate between column 1 and column 2

        with col:
            st.markdown(
                f"""
                <div style="
                    background-color: rgba(255, 255, 255, 0);
                    padding: 15px;
                    border-radius: 10px;
                    text-align: center;
                    margin-bottom: 30px;
                ">
                    <img src="{member['image']}" width="250" style="border-radius: 50%; margin-bottom: 10px;">
                    <h4 style="
                        font-family: 'Chau Philomene One', sans-serif; 
                        color: white; 
                        margin: 10px 0;">
                        {member['name']}
                    </h4>
                    <a href="{member['linkedin']}">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" width="30">
                    </a>
                    <br>
                    <a href="{member['linkedin']}"></a>
                </div>
                """, unsafe_allow_html=True)

    contact_text = "Per preguntes, siusplau adreçeu-vos al següent correu:"

    display_text(contact_text, font_size="20px", text_color="white", justify=False)

    st.write(f"""
        <head>
            <link href="https://fonts.googleapis.com/css2?family=Chau+Philomene+One&display=swap" rel="stylesheet">
        </head>
        <div style="
            font-family: 'Chau Philomene One', sans-serif; 
            font-size: 18px; 
            color: white;
            font-weight: 200;
        ">
            <a href="mailto:paula.mateos01@estudiant.upf.edu" style="text-decoration: none; color: inherit;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/4/4e/Gmail_Icon.png" width="30" style="vertical-align: middle; margin-right: 10px;">
            </a> 
            paula.mateos01@estudiant.upf.edu
        </div>
    """, unsafe_allow_html=True)
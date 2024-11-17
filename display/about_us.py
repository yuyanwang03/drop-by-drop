import streamlit as st
from styles import inject_custom_css

def about_us():
    inject_custom_css()

    st.title("About Us")
    
    intro = ("""
    We are five students of Mathematical Engineering in Data Science with strong experience in various programming languages such as Python, Java, and C++. 
    Our expertise in Data Mining and understanding of Recommendation Systems allows us to develop a probabilistic model to represent user opinions effectively.
    """)

    st.write(f'<div class="stTextContainer">{intro}</div>', unsafe_allow_html=True)

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
            "image": "https://media.licdn.com/dms/image/v2/D4D03AQFYwPxRQiywDg/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1728860563140?e=1736380800&v=beta&t=K0kwESnnnqryDVzW-LJvpTWiMQKtaphG0rgbe1F5RzE",  # Replace with actual URL
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


   
    # Display each team member's image on the left, text on the right
    #for member in team:
     #   st.image(member["image"], width=150, use_column_width=False)  # Image on the left
      #  st.write(f'<div class="stTextContainer">{member["name"]}</div>', unsafe_allow_html=True)
       # st.write(f'<a href="{member["linkedin"]}"><img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" width="30"></a>    {member["linkedin"]}', unsafe_allow_html=True)
        #st.write("---")

# Create columns
    cols = st.columns(2)

    # Display each team member's image, name, and LinkedIn in two columns per row
    for i, member in enumerate(team):
        col = cols[i % 2]  # Alternate between column 1 and column 2

        with col:
            st.markdown(
                f"""
                <div style="
                    background-color: rgba(255, 255, 255, 0.8);
                    padding: 15px;
                    border-radius: 10px;
                    text-align: center;
                    margin-bottom: 30px;
                ">
                    <img src="{member['image']}" width="250" style="border-radius: 50%; margin-bottom: 10px;">
                    <h4>{member['name']}</h4>
                    <a href="{member['linkedin']}">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" width="30">
                    </a>
                    <br>
                    <a href="{member['linkedin']}"></a>
                </div>
                """, unsafe_allow_html=True)

    st.write(f"""
             <div style="
                    background-color: rgba(255, 255, 255, 0.8);
                    padding: 15px;
                    border-radius: 10px;
                    text-align: center;
                ">
            For further inquiries, feel free to reach us via email.\n\n
            Contact: 
            <a href="mailto:paula.mateos01@estudiant.upf.edu">
                <img src="https://upload.wikimedia.org/wikipedia/commons/4/4e/Gmail_Icon.png" width="30">
            </a> paula.mate0s01@estudiant.upf.edu
             </div>
        """, unsafe_allow_html=True)

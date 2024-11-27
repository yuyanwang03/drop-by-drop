import streamlit as st
import pickle
from styles import inject_custom_css, display_text
from static_graphs import plot_common

# Function to load the trained model from a pickle file
# def load_model():
#     with open('your_model.pkl', 'rb') as file:  # Update with your model file path
#         model = pickle.load(file)
#     return model

def predict(data, census):

    col1, _, col2 = st.columns([3,1,1])

    with col1:
        st.image("media/header1.png", width=600)
    
    with col2:
        st.image("media/header2.png", width = 240)

    # Custom HTML with text-shadow effect
    display_text("Simulació", font_size="80px", text_color="rgb(56, 182, 255)", shadow_offset= "4px 4px")

    text = "Aquesta pàgina permet veure una simulació a futur del consum d'aigua a Barcelona segons el número de turistes."
    display_text(text)


    # Load the model
    #model = load_model()

    # User input for the number of tourists
    num_tourists = st.number_input("Enter the number of tourists:", min_value=0, step=1)

    # Button to trigger prediction
    if st.button("Predict"):
        # Ensure there is a valid input for prediction (you can modify this depending on your model's input)
        if num_tourists > 0:
            # Example: Assuming the model expects a dictionary or array with the number of tourists as a feature
            input_data = [[num_tourists]]  # Adjust this based on your model's expected input format
            
            # Predict using the loaded model
            #prediction = model.predict(input_data)

            # Display the prediction
            #st.write(f"The predicted result is: {prediction[0]}")
            plot_common(data, census, static=False,year='2023', month=8,group_by='Dia')
        else:
            st.warning("Please enter a valid number of tourists.")

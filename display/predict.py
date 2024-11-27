import streamlit as st
import pickle
from styles import inject_custom_css

# Function to load the trained model from a pickle file
# def load_model():
#     with open('your_model.pkl', 'rb') as file:  # Update with your model file path
#         model = pickle.load(file)
#     return model

def predict(data, census):

    # Custom HTML with text-shadow effect
    html_code = """
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Chau+Philomene+One&display=swap" rel="stylesheet">
    </head>
    <div style="text-shadow: rgba(56, 182, 255, 0.4) 2px 2px 0px;">
        <p style="font-family: 'Chau Philomene One', sans-serif; font-size: 35px; color: rgb(255, 255, 255); line-height: 488px; letter-spacing: 0em;">
            Estudi estàtic
        </p>
    </div>
    """

    # Display HTML in Streamlit
    st.markdown(html_code, unsafe_allow_html=True)


    st.markdown('<div style="height: 65px;"></div>', unsafe_allow_html=True)  # Adjust the height as needed


    inject_custom_css()

    st.image("media/simulació.png")
"""
    # Load the model
    model = load_model()

    # User input for the number of tourists
    num_tourists = st.number_input("Enter the number of tourists:", min_value=0, step=1)

    # Button to trigger prediction
    if st.button("Predict"):
        # Ensure there is a valid input for prediction (you can modify this depending on your model's input)
        if num_tourists > 0:
            # Example: Assuming the model expects a dictionary or array with the number of tourists as a feature
            input_data = [[num_tourists]]  # Adjust this based on your model's expected input format
            
            # Predict using the loaded model
            prediction = model.predict(input_data)

            # Display the prediction
            st.write(f"The predicted result is: {prediction[0]}")
        else:
            st.warning("Please enter a valid number of tourists.")
"""
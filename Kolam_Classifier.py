import streamlit as st
from PIL import Image
import pandas as pd
from kolam_classifier_logic import load_model, predict
from kolam_descriptions import get_description # <--- IMPORT THE NEW FUNCTION

st.set_page_config(page_title="Kolam Classifier", layout="wide")

st.title("🔎 Kolam Classifier")
st.write("Upload an image of a Kolam to classify its type. This tool uses a trained PyTorch model to identify the pattern.")

# Load the model
try:
    model = load_model()
    st.sidebar.success("✅ Model loaded successfully!")
except FileNotFoundError:
    st.error("Model file not found. Please ensure 'simple_kolam_classifier.pth' is in the root directory.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while loading the model: {e}")
    st.stop()


# --- File Uploader ---
uploaded_file = st.file_uploader("Choose a Kolam image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Kolam", use_column_width=True)
    
    if st.button("Classify Kolam", type="primary"):
        with st.spinner("Classifying..."):
            confidences = predict(model, image)
            
            st.subheader("Classification Results")
            
            if confidences:
                # Create a DataFrame for better display
                df = pd.DataFrame(list(confidences.items()), columns=['Kolam Type', 'Probability'])
                df = df.sort_values(by='Probability', ascending=False).reset_index(drop=True)

                # Get the top prediction
                top_prediction = df.iloc[0]
                predicted_class = top_prediction['Kolam Type']
                
                st.success(f"**Top Prediction: {predicted_class}** with {top_prediction['Probability']:.2%} confidence.")

                # Display a bar chart of probabilities
                st.write("Confidence Scores:")
                st.bar_chart(df.set_index('Kolam Type'))
                
                # --- NEW FEATURE: DISPLAY DETAILED WRITE-UP ---
                st.markdown("---") # Add a visual separator
                
                # Get the description data for the predicted class
                description_data = get_description(predicted_class)
                
                if description_data:
                    st.subheader(f"📖 About {description_data['title']}")
                    st.image(description_data['image_url'], caption=f"An example of a {description_data['title']}")
                    st.markdown(description_data['description'], unsafe_allow_html=True)
                else:
                    st.warning(f"No detailed description available for the class: {predicted_class}")

            else:
                st.error("Classification failed. Please try again.")
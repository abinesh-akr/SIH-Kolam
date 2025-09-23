import streamlit as st
from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
import langdetect
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import pandas as pd
from kolam_classifier_logic import predict
from kolam_descriptions import get_description
import os
import requests
from pathlib import Path

load_dotenv()

SUTRA_API = os.getenv("SUTRA_API_KEY")

sutra_model = OpenAILike(
    id="sutra-v2",
    api_key=os.getenv("SUTRA_API_KEY", "sutra_1p8L5c8EmR1gUrtXbmw20kmYzS0GDC2Tq7a86U8pPTNmW6UUz0psboTmC5NK"),
    base_url="https://api.two.ai/v2",
    extra_headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json"
    }
)

sutra_agent = Agent(
    name="Kolam Multilingual Analyzer",
    model=sutra_model,
    instructions=[
        "Be culturally sensitive, clear, and detailed.",
        "Explain the Kolam art type, its regional origin, mathematical significance, grid count, history, and importance in a systematic way.",
        "Respond in the user's preferred language. If you cannot connect to Sutra or face any error, return a short friendly error message instead of crashing."
    ],
    markdown=True,
)

st.set_page_config(page_title="Kolam Insights", layout="wide")

# Function to download the model from GitHub Release
def download_model(url, local_path="simple_kolam_classifier.pth"):
    if not Path(local_path).exists():
        try:
            with st.spinner("Downloading model from GitHub Release..."):
                response = requests.get(url, stream=True)
                response.raise_for_status()
                with open(local_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
            st.sidebar.success(f"Model downloaded to {local_path}")
        except Exception as e:
            st.error(f"Failed to download model: {e}")
            st.stop()
    return local_path

# Define the model architecture matching the .pth file
def load_model():
    model_url = "https://github.com/abinesh-akr/SIH-Kolam/releases/download/kolam/simple_kolam_classifier.pth"  # Replace with your actual URL
    local_model_path = download_model(model_url)
    
    class KolamClassifier(nn.Module):
        def __init__(self, num_classes=6):  # Changed to 6 to match .pth file
            super(KolamClassifier, self).__init__()
            self.features = nn.Sequential(
                nn.Conv2d(1, 16, kernel_size=3, padding=1),  # Grayscale input
                nn.ReLU(inplace=True),
                nn.MaxPool2d(kernel_size=2, stride=2),
                nn.Conv2d(16, 32, kernel_size=3, padding=1),
                nn.ReLU(inplace=True),
                nn.MaxPool2d(kernel_size=2, stride=2),
                nn.Conv2d(32, 64, kernel_size=3, padding=1),
                nn.ReLU(inplace=True),
                nn.MaxPool2d(kernel_size=2, stride=2),
            )
            self.classifier = nn.Sequential(
                nn.Linear(64 * 16 * 16, 512),
                nn.ReLU(inplace=True),
                nn.ReLU(inplace=True),
                nn.Linear(512, num_classes),
            )
        
        def forward(self, x):
            x = self.features(x)
            x = x.view(x.size(0), -1)
            x = self.classifier(x)
            return x
    
    try:
        model = KolamClassifier()
        checkpoint = torch.load(local_model_path, map_location='cpu')
        model.load_state_dict(checkpoint['model_state_dict'] if 'model_state_dict' in checkpoint else checkpoint)
        model.eval()
        return model
    except Exception as e:
        st.error(f"An error occurred while loading the model: {e}")
        st.stop()

st.title("🔍 Kolam Insights")
st.write("Analyze Kolam designs to identify principles and classify types.")

tab1, tab2 = st.tabs(["Multilingual Kolam Analyzer", "Kolam Type Classifier"])

with tab1:
    KOLAM_PROMPT = """
    You are a Kolam expert. Analyze the uploaded Kolam image and provide:
    - Art type and regional origin
    - Mathematical significance (symmetry, grids)
    - History and cultural importance
    """
    uploaded_file = st.file_uploader("Upload Kolam Image", type=["jpg", "png"])
    query = st.text_area("Additional Query")
    preferred_language = st.selectbox("Language", ["Auto-Detect", "English", "Hindi", "Tamil", "Telugu", "Kannada", "Malayalam"])

    if st.button("🧠 Analyze with Sutra"):
        if not uploaded_file:
            st.warning("Please upload a Kolam image first.")
        else:
            full_prompt = f"{KOLAM_PROMPT}\n\nExtra context: {query}" if query.strip() else KOLAM_PROMPT
            with st.spinner("Analyzing Kolam with Sutra..."):
                try:
                    response = sutra_agent.run(full_prompt).content.strip()
                except Exception:
                    st.error("⚠️ Could not connect to Sutra API. Please try again later.")
                    response = ""

                if response:
                    detected_language = "en"
                    try:
                        detected_language = langdetect.detect(query) if query.strip() else "en"
                    except:
                        pass

                    target_language = preferred_language
                    if preferred_language == "Auto-Detect":
                        lang_map = {
                            'en': 'English', 'hi': 'Hindi', 'ta': 'Tamil',
                            'te': 'Telugu', 'kn': 'Kannada', 'ml': 'Malayalam'
                        }
                        target_language = lang_map.get(detected_language, "English")

                    st.markdown("### ✅ Kolam Analysis:")
                    if target_language != "English":
                        try:
                            lang_codes = {
                                "Hindi": "hi", "Tamil": "ta", "Telugu": "te",
                                "Kannada": "kn", "Malayalam": "ml"
                            }
                            lang_code = lang_codes.get(target_language, "en")
                            translated_response = GoogleTranslator(
                                source='auto', target=lang_code
                            ).translate(response)
                            st.markdown(f"### 🌐 Translated Answer ({target_language}):")
                            st.write(translated_response)
                        except Exception as e:
                            st.warning(f"Translation unavailable: {e}")
                            st.write(response)
                    else:
                        st.write(response)

with tab2:
    st.write("Upload an image of a Kolam to classify its type.")
    preferred_language = st.selectbox("Language for Results", ["Auto-Detect", "English", "Hindi", "Tamil", "Telugu", "Kannada", "Malayalam"])
    
    try:
        model = load_model()
        st.sidebar.success("✅ Model loaded successfully!")
    except Exception as e:
        st.error(f"An error occurred while loading the model: {e}")
        st.stop()

    uploaded_file = st.file_uploader("Choose a Kolam image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image = image.convert('L')  # Grayscale conversion
        st.image(image, caption="Uploaded Kolam (Grayscale)", use_column_width=True)
        
        if st.button("Classify Kolam", type="primary"):
            with st.spinner("Classifying..."):
                confidences = predict(model, image)
                
                st.subheader("Classification Results")
                
                if confidences:
                    df = pd.DataFrame(list(confidences.items()), columns=['Kolam Type', 'Probability'])
                    df = df.sort_values(by='Probability', ascending=False).reset_index(drop=True)

                    top_prediction = df.iloc[0]
                    predicted_class = top_prediction['Kolam Type']
                    confidence_text = f"Top Prediction: {predicted_class} with {top_prediction['Probability']:.2%} confidence."

                    description_data = get_description(predicted_class)
                    description_text = description_data['description'] if description_data else f"No detailed description available for the class: {predicted_class}"

                    detected_language = "en"
                    try:
                        detected_language = langdetect.detect(predicted_class) if predicted_class else "en"
                    except:
                        pass

                    target_language = preferred_language
                    if preferred_language == "Auto-Detect":
                        lang_map = {
                            'en': 'English', 'hi': 'Hindi', 'ta': 'Tamil',
                            'te': 'Telugu', 'kn': 'Kannada', 'ml': 'Malayalam'
                        }
                        target_language = lang_map.get(detected_language, "English")

                    if target_language != "English":
                        try:
                            lang_codes = {
                                "Hindi": "hi", "Tamil": "ta", "Telugu": "te",
                                "Kannada": "kn", "Malayalam": "ml"
                            }
                            lang_code = lang_codes.get(target_language, "en")
                            
                            translated_confidence = GoogleTranslator(
                                source='auto', target=lang_code
                            ).translate(confidence_text)
                            translated_description = GoogleTranslator(
                                source='auto', target=lang_code
                            ).translate(description_text)
                            
                            st.markdown(f"### 🌐 Translated Results ({target_language}):")
                            st.success(f"**{translated_confidence}**")
                            st.write("Confidence Scores:")
                            st.bar_chart(df.set_index('Kolam Type'))
                            
                            st.markdown("---")
                            
                            if description_data:
                                st.subheader(f"📖 About {description_data['title']}")
                                st.image(description_data['image_url'], caption=f"An example of a {description_data['title']}")
                                st.markdown(translated_description, unsafe_allow_html=True)
                            else:
                                st.warning(translated_description)
                        except Exception as e:
                            st.warning(f"Translation unavailable: {e}")
                            st.success(f"**{confidence_text}**")
                            st.write("Confidence Scores:")
                            st.bar_chart(df.set_index('Kolam Type'))
                            st.markdown("---")
                            if description_data:
                                st.subheader(f"📖 About {description_data['title']}")
                                st.image(description_data['image_url'], caption=f"An example of a {description_data['title']}")
                                st.markdown(description_text, unsafe_allow_html=True)
                            else:
                                st.warning(description_text)
                    else:
                        st.success(f"**{confidence_text}**")
                        st.write("Confidence Scores:")
                        st.bar_chart(df.set_index('Kolam Type'))
                        st.markdown("---")
                        if description_data:
                            st.subheader(f"📖 About {description_data['title']}")
                            st.image(description_data['image_url'], caption=f"An example of a {description_data['title']}")
                            st.markdown(description_text, unsafe_allow_html=True)
                        else:
                            st.warning(description_text)
                else:
                    st.error("Classification failed. Please try again.")

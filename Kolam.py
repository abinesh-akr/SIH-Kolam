import streamlit as st
from google import genai
from PIL import Image
from io import BytesIO
import json
import os
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = "AIzaSyBMThlSDjHMjrCsfxu8bjUZ8VBkDkCYKHg"

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Advanced Kolam Generator", layout="wide")
st.title("🎨 AI-Powered Kolam Generator - Beautiful & Colorful Designs")

# -----------------------------
# API Key Setup
# -----------------------------
client = genai.Client(api_key=GEMINI_API_KEY)
# -----------------------------
# Kolam Prompt Function
# -----------------------------
def create_advanced_kolam_prompt(kolam_type, state, complexity, grid_size, color_scheme, occasion, custom_elements):
    """Create structured Kolam generation prompt (JSON format)"""
    prompt = """
    Generate a high-quality, artistic Kolam (Rangoli) design based on the following details:

    - Type: Symmetric Kolam design with dots (pulli) as a base grid.
    - Grid: Use a 1-3-5-7-9-7-5-3-1 stepped dot grid.
    - Style: Traditional South Indian Kolam, drawn with white rice powder on a dark, wet floor background.
    - Lines: Smooth, curvilinear, continuous loops enclosing all dots.
    - Symmetry: Both reflectional and rotational symmetry must be present.
    - Visual feel: Elegant, culturally authentic, geometric, and mathematically balanced.
    - Avoid text, borders, or watermarks.
    - Make it look hand-drawn but neat, with fine white strokes.
    - Output: A single, clear Kolam pattern with focus on the design — no extra decorations, no people, no objects.
    """
    return prompt


    """Create sophisticated prompts for stunning Kolam generation with guaranteed colors"""
    
    # Specific color palettes for each scheme
    color_palettes = {
        "Vibrant Festival": {
            "background": "#2C1810",
            "primary": ["#FF6B35", "#FFD23F", "#06FFA5", "#FF1744"],
            "accent": ["#E91E63", "#9C27B0"]
        },
        "Royal Colors": {
            "background": "#1A1A2E", 
            "primary": ["#FFD700", "#4A148C", "#B71C1C", "#FF6F00"],
            "accent": ["#1A237E", "#4A148C"]
        },
        "Pastel Dream": {
            "background": "#F8F8FF",
            "primary": ["#FFB3BA", "#BAFFC9", "#BAE1FF", "#FFFFBA"],
            "accent": ["#E1BAFF", "#FFB3E6"]
        },
        "Nature Inspired": {
            "background": "#2E4057",
            "primary": ["#8BC34A", "#FF9800", "#2196F3", "#FFC107"],
            "accent": ["#795548", "#607D8B"]
        },
        "Traditional White": {
            "background": "#1C1C1C",
            "primary": ["#FFFFFF", "#F5F5F5", "#E0E0E0", "#BDBDBD"],
            "accent": ["#9E9E9E", "#757575"]
        },
        "Monochrome Elegant": {
            "background": "#000000",
            "primary": ["#FFFFFF", "#BDBDBD", "#757575", "#424242"],
            "accent": ["#9E9E9E", "#616161"]
        }
    }
    
    selected_palette = color_palettes.get(color_scheme, color_palettes["Vibrant Festival"])
    
    prompt = f"""
    Create a stunning, highly detailed {kolam_type} design representing {state} tradition.
    
    MANDATORY COLOR REQUIREMENTS - MUST BE INCLUDED:
    {{
        "visual_elements": {{
            "background_color": "{selected_palette['background']}",
            "primary_colors": {selected_palette['primary']},
            "accent_colors": {selected_palette['accent']}
        }},
        "pattern_structure": {{
            "central_motif": {{
                "type": "lotus",
                "position": [400, 400],
                "size": 80,
                "colors": ["{selected_palette['primary'][0]}", "{selected_palette['primary'][1]}"]
            }},
            "border_patterns": [
                {{
                    "pattern": "floral",
                    "thickness": 40,
                    "colors": ["{selected_palette['primary'][2]}", "{selected_palette['accent'][0]}"]
                }}
            ],
            "corner_elements": [
                {{
                    "position": "all_corners",
                    "size": 25,
                    "colors": ["{selected_palette['accent'][1]}"]
                }}
            ],
            "connecting_patterns": [
                {{
                    "type": "radiating_lines",
                    "color": "{selected_palette['primary'][1]}",
                    "width": 3
                }}
            ],
            "decorative_fills": [
                {{
                    "type": "geometric_rings",
                    "colors": {selected_palette['primary'][:3]},
                    "opacity": 0.8
                }}
            ]
        }},
        "design_info": {{
            "name": "Beautiful {kolam_type} from {state}",
            "description": "A vibrant and intricate {kolam_type} featuring traditional {state} motifs with {color_scheme.lower()} colors, perfect for {occasion.lower()}",
            "cultural_meaning": "Traditional {state} kolam symbolizing prosperity, beauty, and spiritual harmony",
            "difficulty": "{complexity}",
            "estimated_time": "45-60 minutes"
        }},
        "step_by_step_guide": [
            "Start by preparing the {selected_palette['background']} background surface",
            "Draw the central lotus motif using {selected_palette['primary'][0]} and {selected_palette['primary'][1]} colors",
            "Add decorative borders with {selected_palette['primary'][2]} colored patterns",
            "Fill in corner elements using {selected_palette['accent'][0]} accent color",
            "Connect all elements with {selected_palette['primary'][1]} radiating lines",
            "Add final decorative touches and color gradients for depth"
        ],
        "pro_tips": [
            "Use {color_scheme.lower()} color palette for authentic {state} style",
            "Blend colors gently for smooth transitions between {selected_palette['primary'][0]} and {selected_palette['primary'][1]}",
            "Ensure symmetry in all four directions for traditional kolam balance",
            "Layer colors from light to dark for better visual depth"
        ],
        "color_mixing_guide": {{
            "primary_mix": "Blend {selected_palette['primary'][0]} with {selected_palette['primary'][1]} for smooth gradients",
            "gradients": "Create transitions between all primary colors: {', '.join(selected_palette['primary'])}",
            "highlights": "Use {selected_palette['accent'][0]} for emphasis and {selected_palette['accent'][1]} for shadows"
        }}
    }}
    
    ADDITIONAL REQUIREMENTS:
    - Grid Size: {grid_size}x{grid_size} underlying structure
    - Complexity: {complexity} level with appropriate detail density
    - Special Elements: {custom_elements if custom_elements else 'Traditional lotus and peacock motifs'}
    - Cultural Style: Authentic {state} regional patterns and symbolism
    - Occasion: Designed specifically for {occasion} celebrations
    
    CRITICAL: Return EXACTLY the JSON structure above with all the specified colors. The visual_elements section with background_color, primary_colors, and accent_colors is MANDATORY and must match the {color_scheme} palette exactly.
    """
    
    return prompt
# -----------------------------
# Streamlit Sidebar
# -----------------------------
st.sidebar.header("🎨 Kolam Design Studio")

col1, col2 = st.sidebar.columns(2)

with col1:
    kolam_type = st.selectbox("Kolam Style", ["Sikku Kolam", "Pulli Kolam", "Rangoli", "Freehand Kolam",
                                              "Geometric Kolam", "Floral Kolam", "Festival Special"], index=2)
    state = st.selectbox("Regional Style", ["Tamil Nadu", "Karnataka", "Andhra Pradesh", "Kerala", "Telangana"])

with col2:
    complexity = st.selectbox("Complexity", ["Beginner", "Intermediate", "Advanced", "Master Level"], index=1)
    grid_size = st.slider("Pattern Density", 8, 20, 12)

color_scheme = st.sidebar.selectbox("Color Theme", ["Vibrant Festival", "Royal Colors", "Pastel Dream",
                                                   "Nature Inspired", "Traditional White", "Monochrome Elegant"])

occasion = st.sidebar.selectbox("Special Occasion", ["Daily Practice", "Diwali", "Pongal",
                                                    "Wedding", "Navratri", "Housewarming"])

custom_elements = st.sidebar.text_area("Custom Elements",
                                       placeholder="e.g., peacock motifs, lotus flowers, temple arches...",
                                       height=80)

# -----------------------------
# Generate Button
# -----------------------------
if st.sidebar.button("🎨 Create Stunning Kolam", type="primary", use_container_width=True):
    with st.spinner("🎭 AI is creating your masterpiece..."):
        try:
            advanced_prompt = create_advanced_kolam_prompt(
                kolam_type, state, complexity, grid_size, color_scheme, occasion, custom_elements
            )

            # Generate image using Gemini Image Preview model
            response = client.models.generate_content(
                model="gemini-2.5-flash-image-preview",
                contents=advanced_prompt
            )

            # Extract image data
            image_parts = [
                part.inline_data.data
                for part in response.candidates[0].content.parts
                if part.inline_data
            ]

            if image_parts:
                image = Image.open(BytesIO(image_parts[0]))
                st.image(image, use_container_width=True, caption=f"✨ {kolam_type} Kolam from {state}")

                # Download option
                img_buffer = BytesIO()
                image.save(img_buffer, format="PNG")
                st.download_button(
                    "📥 Download High-Quality Kolam",
                    data=img_buffer.getvalue(),
                    file_name=f"{kolam_type}_{state}_{complexity}.png",
                    mime="image/png",
                    use_container_width=True
                )
            else:
                st.error("⚠️ No image was generated. Try again with a different configuration.")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("💡 Check your API connection or simplify your prompt.")

st.markdown("---")
st.caption("🎨 AI-Powered Kolam Generator - Bringing Traditional Art to Digital Life")

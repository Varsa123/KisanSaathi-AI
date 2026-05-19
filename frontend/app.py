import streamlit as st
import requests
import cv2
import numpy as np
from PIL import Image
import io
import os
from datetime import datetime

# Page config
st.set_page_config(
    page_title="KisanSaathi AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .title-text {
        color: #2d5016;
        font-size: 3em;
        font-weight: bold;
        text-align: center;
    }
    .subtitle-text {
        color: #558b2f;
        font-size: 1.5em;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-box {
        background-color: #f0f7e8;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #558b2f;
        margin: 10px 0;
    }
    .success-box {
        background-color: #c8e6c9;
        padding: 15px;
        border-radius: 5px;
        color: #1b5e20;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 5px;
        color: #856404;
    }
    .disease-detected {
        background-color: #ffcdd2;
        padding: 20px;
        border-radius: 10px;
        color: #b71c1c;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("### 🌾 KisanSaathi AI")
    st.markdown("AI-powered Agricultural Assistant")
    st.divider()
    
    page = st.radio(
        "Select Feature:",
        ["🏠 Home", "🔍 Disease Detection", "💰 Mandi Prices", "⛅ Weather Alerts", "🎤 Voice Assistant", "ℹ️ About"]
    )
    
    st.divider()
    st.markdown("### About KisanSaathi")
    st.info("An AI assistant helping Indian farmers detect crop diseases, get treatment advice, and access market information in their local language.")

# Backend API URL (change this if needed)
API_URL = "http://localhost:5000"

# ============= HOME PAGE =============
if page == "🏠 Home":
    st.markdown('<p class="title-text">🌾 KisanSaathi AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-text">Your AI-Powered Agricultural Assistant</p>', unsafe_allow_html=True)
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Our Mission")
        st.write("""
        KisanSaathi AI empowers Indian farmers with:
        - **Instant Disease Detection** using AI
        - **Expert Treatment Advice** in local languages
        - **Market Price Updates** from nearby mandis
        - **Weather Alerts** for crop safety
        - **Fertilizer Recommendations** based on soil & crop
        """)
    
    with col2:
        st.markdown("### 📊 Key Features")
        st.markdown("""
        1. **Upload & Detect** - Click a photo, AI identifies disease
        2. **Get Solutions** - Instant treatment suggestions
        3. **Check Prices** - Real-time mandi rates
        4. **Weather Safe** - Get alerts & recommendations
        5. **Voice Support** - Ask questions in Hindi!
        """)
    
    st.divider()
    
    st.markdown("### 🚀 Quick Start")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📸 Detect Disease", use_container_width=True, key="home_detect"):
            st.switch_page("pages/1_disease_detection.py")
    with col2:
        if st.button("💰 Check Prices", use_container_width=True, key="home_prices"):
            st.switch_page("pages/2_mandi_prices.py")
    with col3:
        if st.button("⛅ Weather Info", use_container_width=True, key="home_weather"):
            st.switch_page("pages/3_weather_alerts.py")

# ============= DISEASE DETECTION PAGE =============
elif page == "🔍 Disease Detection":
    st.markdown("### 🔍 Crop Disease Detection")
    st.write("Upload an image of your plant leaf. Our AI will detect if it's healthy or diseased.")
    st.divider()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📸 Upload Image")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "bmp"])
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            if st.button("🔍 Analyze Image", key="analyze_btn"):
                with st.spinner("Analyzing your crop image..."):
                    try:
                        # Convert image to bytes
                        img_bytes = io.BytesIO()
                        image.save(img_bytes, format="PNG")
                        img_bytes.seek(0)
                        
                        # Send to backend
                        files = {"image": ("image.png", img_bytes, "image/png")}
                        response = requests.post(f"{API_URL}/api/detect-disease", files=files, timeout=10)
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.session_state.detection_result = result
                        else:
                            st.error(f"Error: {response.text}")
                    except requests.exceptions.ConnectionError:
                        st.error("⚠️ Cannot connect to backend. Make sure Flask server is running on port 5000.")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    with col2:
        st.markdown("#### 📊 Results")
        if "detection_result" in st.session_state:
            result = st.session_state.detection_result
            
            # Confidence percentage
            confidence = result.get("confidence", 0) * 100
            
            # Disease status
            if result.get("disease", "").lower() == "healthy":
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.success(f"✅ Status: HEALTHY")
                st.write(f"**Confidence:** {confidence:.1f}%")
                st.markdown('</div>', unsafe_allow_html=True)
                st.info("🌱 Your crop is healthy! Continue regular maintenance.")
            else:
                st.markdown('<div class="disease-detected">', unsafe_allow_html=True)
                st.write(f"⚠️ **Disease Detected:** {result.get('disease', 'Unknown')}")
                st.write(f"**Confidence:** {confidence:.1f}%")
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("#### 💊 Treatment")
                st.info(result.get("treatment", "Consult a local agricultural expert."))
                
                st.markdown("#### 📌 Details")
                st.write(result.get("description", "No additional information."))
        else:
            st.info("Upload an image and click 'Analyze Image' to see results.")

# ============= MANDI PRICES PAGE =============
elif page == "💰 Mandi Prices":
    st.markdown("### 💰 Mandi Price Information")
    st.write("Check current prices of crops in nearby mandis.")
    st.divider()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🌾 Select Crop")
        crop = st.selectbox(
            "Choose a crop:",
            ["Tomato", "Potato", "Onion", "Wheat", "Rice", "Cotton", "Sugarcane"],
            key="crop_select"
        )
        
        state = st.selectbox(
            "Choose state:",
            ["Maharashtra", "Tamil Nadu", "Punjab", "Haryana", "Uttar Pradesh", "Karnataka"],
            key="state_select"
        )
        
        if st.button("📊 Get Prices", key="get_prices_btn"):
            with st.spinner("Fetching mandi prices..."):
                try:
                    response = requests.get(
                        f"{API_URL}/api/mandi-prices",
                        params={"crop": crop, "state": state},
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.mandi_data = data
                    else:
                        st.error(f"Error: {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("⚠️ Cannot connect to backend server.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with col2:
        st.markdown("#### 💹 Current Prices")
        if "mandi_data" in st.session_state:
            data = st.session_state.mandi_data
            st.metric("Average Price (per quintal)", f"₹{data.get('avg_price', 0)}", delta=f"{data.get('change', 0)}%")
            st.metric("Today's High", f"₹{data.get('high', 0)}")
            st.metric("Today's Low", f"₹{data.get('low', 0)}")
            st.write(f"**Last Updated:** {data.get('timestamp', 'N/A')}")
        else:
            st.info("Select crop and state, then click 'Get Prices'.")

# ============= WEATHER ALERTS PAGE =============
elif page == "⛅ Weather Alerts":
    st.markdown("### ⛅ Weather Alerts & Recommendations")
    st.write("Get weather forecasts and crop protection advice.")
    st.divider()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📍 Enter Location")
        location = st.text_input("Enter your district/city:", value="Pune", key="location_input")
        
        if st.button("🔄 Get Weather", key="get_weather_btn"):
            with st.spinner("Fetching weather data..."):
                try:
                    response = requests.get(
                        f"{API_URL}/api/weather",
                        params={"location": location},
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.weather_data = data
                    else:
                        st.error(f"Error: {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("⚠️ Cannot connect to backend server.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with col2:
        st.markdown("#### 📊 Weather Info")
        if "weather_data" in st.session_state:
            data = st.session_state.weather_data
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Temperature", f"{data.get('temp', 0)}°C")
            with col_b:
                st.metric("Humidity", f"{data.get('humidity', 0)}%")
            with col_c:
                st.metric("Rainfall", f"{data.get('rainfall', 0)}mm")
            
            st.markdown("#### ⚠️ Alerts")
            alerts = data.get('alerts', [])
            if alerts:
                for alert in alerts:
                    st.warning(alert)
            else:
                st.success("✅ No weather alerts. Conditions are favorable.")
            
            st.markdown("#### 💡 Recommendations")
            recommendations = data.get('recommendations', [])
            for rec in recommendations:
                st.info(rec)
        else:
            st.info("Enter location and click 'Get Weather'.")

# ============= VOICE ASSISTANT PAGE =============
elif page == "🎤 Voice Assistant":
    st.markdown("### 🎤 Voice Assistant")
    st.write("Ask questions in Hindi (हिंदी) and get voice responses.")
    st.divider()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🗣️ Ask Question (Hindi)")
        question = st.text_area(
            "Type your question in Hindi:",
            placeholder="उदाहरण: गेहूं में पीले धब्बे क्यों आते हैं?",
            height=100,
            key="voice_question"
        )
        
        if st.button("🔊 Get Voice Response", key="voice_btn"):
            if question.strip():
                with st.spinner("Generating response..."):
                    try:
                        response = requests.post(
                            f"{API_URL}/api/voice-assistant",
                            json={"question": question},
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.session_state.voice_result = result
                        else:
                            st.error(f"Error: {response.text}")
                    except requests.exceptions.ConnectionError:
                        st.error("⚠️ Cannot connect to backend server.")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("Please type a question.")
    
    with col2:
        st.markdown("#### 📢 Response")
        if "voice_result" in st.session_state:
            result = st.session_state.voice_result
            
            st.markdown("**Answer:**")
            st.write(result.get("answer", "No response available."))
            
            # Play audio if available
            if "audio_url" in result:
                st.markdown("**Audio Response:**")
                st.audio(result["audio_url"])
        else:
            st.info("Ask a question to get a response.")

# ============= ABOUT PAGE =============
elif page == "ℹ️ About":
    st.markdown("### ℹ️ About KisanSaathi AI")
    st.divider()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🎯 Mission")
        st.write("""
        KisanSaathi AI is an AI-powered agricultural assistant designed to help Indian farmers:
        
        • Detect crop diseases using image recognition
        • Get treatment advice in local languages
        • Access market prices from nearby mandis
        • Receive weather alerts and recommendations
        • Understand fertilizer needs
        """)
        
        st.markdown("#### 🔧 Technology")
        st.write("""
        - **Frontend:** Streamlit (Python)
        - **Backend:** Flask (Python)
        - **ML Model:** TensorFlow & CNN
        - **Dataset:** PlantVillage Disease Dataset
        - **Voice:** Google Text-to-Speech
        """)
    
    with col2:
        st.markdown("#### 👥 Team")
        st.write("""
        Built with ❤️ for Indian farmers
        
        **Project Duration:** 5 Days
        **Status:** MVP
        **Version:** 1.0
        """)
        
        st.markdown("#### 📞 Support")
        st.info("For issues or suggestions, please open an issue on GitHub.")
    
    st.divider()
    st.markdown("### 📊 How It Works")
    st.write("""
    1. **Upload Image** → Take a photo of your crop leaf
    2. **AI Analysis** → Our model analyzes the image
    3. **Disease Detection** → Get instant diagnosis
    4. **Treatment Advice** → Receive treatment suggestions
    5. **Voice Support** → Ask follow-up questions
    """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; margin-top: 2rem;'>
    <p>KisanSaathi AI © 2024 | Empowering Indian Farmers with AI</p>
</div>
""", unsafe_allow_html=True)
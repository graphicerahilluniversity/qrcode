import streamlit as st
from PIL import Image
import cv2
import io
from gtts import gTTS
import tempfile
import numpy as np
import time
import base64
from io import BytesIO
def inject_css():
    css = """
    <style>
     #MainMenu {visibility: hidden;}
         
         /* Hide the footer */
         footer {visibility: hidden;}
         
         /* Assuming 'fork_option_class' is the class of the Fork option */
         .fork_option_class {display: none !important;}
         
         /* Example: Hide the Streamlit branding (replace '.streamlit-brading' with the correct selector) */
         .css-1d391kg {display: none !important;}
        /* Style the title */
        h1 {
            color: #ffff;
            text-align: center;
        }

        /* Style the file uploader */
        .stFileUploader {
            border: 2px solid #4CAF50;
            border-radius: 20px;
        }

        /* Style the success messages */
        .stAlert {
            border-left: 5px solid #4CAF50;
        }
        .stAudio{
            width: 100%; /* Make the audio player fit its container */
    height: 50px; /* Set a fixed height */
    background-color: #4D4D4D; /* Light grey background */
    border-radius: 5px; /* Rounded corners */

        }


    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


inject_css()


# Function to decode QR code
def decode_qr_code(image):
    # Convert PIL Image to an OpenCV image
    opencvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Initialize the QRCode detector
    detector = cv2.QRCodeDetector()

    # Detect and decode
    data, bbox, straight_qrcode = detector.detectAndDecode(opencvImage)
    if bbox is not None:
        return [data]
    else:
        return []
def text_to_speech_with_button(text, lang='en'):
    tts = gTTS(text=text, lang=lang, slow=False)
    audio_io = BytesIO()
    tts.write_to_fp(audio_io)
    audio_io.seek(0)
    audio_base64 = base64.b64encode(audio_io.read()).decode("utf-8")
    audio_html = f"""
    <audio id="generatedAudio" controls><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mpeg"></audio>
    <button onclick="document.getElementById('generatedAudio').play()">Play Audio</button>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# Replace the call to `text_to_speech_autoplay` with `text_to_speech_with_button` in your app

def text_to_speech_autoplay(text, lang='en'):
    # Display a message to the user that the audio generation is starting
    progress_text = st.empty()
    progress_text.text("Generating audio..?/.")

    # Initialize a progress bar
    progress_bar = st.progress(0)

    tts = gTTS(text=text, lang=lang, slow=False)
    audio_io = BytesIO()
    tts.write_to_fp(audio_io)
    audio_io.seek(0)
    audio_base64 = base64.b64encode(audio_io.read()).decode("utf-8")
    audio_html = f'<audio autoplay><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mpeg"></audio>'

    # Since we can't track progress, we simulate completion
    progress_bar.progress(100)
    progress_text.text("Audio ready!")

    # Wait a bit before clearing the progress display (optional, for better user experience)
    time.sleep(1)
    progress_bar.empty()
    progress_text.empty()

    st.markdown(audio_html, unsafe_allow_html=True)


hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {

	visibility: hidden;

	}
footer:after {
	content:'NSS DEV CELL'; 
	visibility: visible;
	display: block;
	position: relative;
	#background-color: red;
	padding: 5px;
	top: 2px;
}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.title('QR Code Scanner')

uploaded_file = st.file_uploader("Choose a file", type=['png', 'jpg', 'jpeg'])
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    image = Image.open(io.BytesIO(bytes_data))
    st.image(image, caption='Uploaded QR Code', use_column_width=True)

    decoded_info = decode_qr_code(image)

    if decoded_info:
        st.write('Decoded Information:')
        for info in decoded_info:
            st.success(info)
            # Call the modified function to play audio
            text_to_speech_autoplay(info)


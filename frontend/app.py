import streamlit as st
import requests
import base64
from PIL import Image
import io

API_URL = "https://titanic-backend-klbp.onrender.com/chat"

st.set_page_config(
    page_title="Titanic AI",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- SESSION ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- CSS ----------------
st.markdown("""
<style>

/* Clean background */
[data-testid="stAppViewContainer"] {
    background: #ffffff;
}

/* Centered layout */
.block-container {
    max-width: 760px;
    margin: auto;
    padding-top: 70px;
    padding-bottom: 120px;
}

/* Assistant bubble */
.assistant-container {
    display: flex;
    justify-content: flex-start;
}

.assistant-bubble {
    background: #f5f5f5;
    padding: 14px 18px;
    border-radius: 18px;
    max-width: 75%;
    margin-bottom: 18px;
    font-size: 15px;
    line-height: 1.6;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    animation: fadeIn 0.25s ease-in-out;
}

/* User bubble */
.user-container {
    display: flex;
    justify-content: flex-end;
}

.user-bubble {
    background: #3b82f6;
    color: white;
    padding: 14px 18px;
    border-radius: 18px;
    max-width: 75%;
    margin-bottom: 18px;
    font-size: 15px;
    line-height: 1.6;
    animation: fadeIn 0.25s ease-in-out;
}

/* Chat input */
[data-testid="stChatInput"] {
    position: fixed;
    bottom: 25px;
    left: 50%;
    transform: translateX(-50%);
    width: 760px;
}

[data-testid="stChatInput"] textarea {
    border-radius: 22px !important;
}

/* Image styling */
img {
    border-radius: 12px;
    margin-top: 10px;
}

/* Smooth fade-in */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(4px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Thinking pulse animation */
.typing-container {
    display: flex;
    justify-content: flex-start;
}

.typing-bubble {
    background: #f5f5f5;
    padding: 14px 18px;
    border-radius: 18px;
    margin-bottom: 18px;
}

.dot {
    height: 6px;
    width: 6px;
    margin: 0 3px;
    background-color: #9ca3af;
    border-radius: 50%;
    display: inline-block;
    animation: pulse 1.4s infinite ease-in-out;
}

.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes pulse {
    0% { opacity: 0.3; }
    50% { opacity: 1; }
    100% { opacity: 0.3; }
}

</style>
""", unsafe_allow_html=True)

# ---------------- EMPTY STATE ----------------
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div style="text-align:center; margin-top:160px;">
        <h1 style="font-weight:600; font-size:40px;">Titanic AI</h1>
        <p style="color:#6b7280; font-size:15px;">
            Ask about survival rate, age, gender, class, fares and more.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.markdown(
            f"""
            <div class="assistant-container">
                <div class="assistant-bubble">{msg["content"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if msg.get("image"):
            st.image(msg["image"], use_container_width=True)
    else:
        st.markdown(
            f"""
            <div class="user-container">
                <div class="user-bubble">{msg["content"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ---------------- CHAT INPUT ----------------
if prompt := st.chat_input("Message Titanic AI..."):

    st.session_state.messages.append({"role": "user", "content": prompt})

    st.markdown(
        f"""
        <div class="user-container">
            <div class="user-bubble">{prompt}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    thinking_placeholder = st.empty()
    thinking_placeholder.markdown("""
        <div class="typing-container">
            <div class="typing-bubble">
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="dot"></span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    try:
        res = requests.post(
            API_URL,
            json={"question": prompt},
            timeout=120
        )

        thinking_placeholder.empty()

        if res.status_code == 200:
            data = res.json()
            answer = data.get("answer", "No response")
            image = None

            if data.get("chart"):
                image_bytes = base64.b64decode(data["chart"])
                image = Image.open(io.BytesIO(image_bytes))

            st.markdown(
                f"""
                <div class="assistant-container">
                    <div class="assistant-bubble">{answer}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if image:
                st.image(image, use_container_width=True)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "image": image
            })

        else:
            st.error("Server error. Please try again.")

    except requests.exceptions.Timeout:
        thinking_placeholder.empty()
        st.error("Backend is waking up (free tier sleep). Please try again.")

    except Exception:
        thinking_placeholder.empty()
        st.error("Unable to connect to backend.")
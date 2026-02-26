import streamlit as st
import requests
import base64
from PIL import Image
import io

API_URL = "http://localhost:8000/chat"

st.set_page_config(
    page_title="Titanic AI",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- SESSION ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- CLEAN MINIMAL CSS ----------------
st.markdown("""
<style>

/* Clean white background */
[data-testid="stAppViewContainer"] {
    background: #ffffff;
}

/* Centered narrow layout */
.block-container {
    max-width: 750px;
    margin: auto;
    padding-top: 60px;
    padding-bottom: 100px;
}

/* Assistant bubble */
.assistant-container {
    display: flex;
    justify-content: flex-start;
}

.assistant-bubble {
    background: #f3f4f6;
    padding: 14px 18px;
    border-radius: 18px;
    max-width: 75%;
    margin-bottom: 18px;
    font-size: 15px;
    line-height: 1.5;
}

/* User bubble */
.user-container {
    display: flex;
    justify-content: flex-end;
}

.user-bubble {
    background: #2563eb;
    color: white;
    padding: 14px 18px;
    border-radius: 18px;
    max-width: 75%;
    margin-bottom: 18px;
    font-size: 15px;
    line-height: 1.5;
}

/* Chat input fixed bottom */
[data-testid="stChatInput"] {
    position: fixed;
    bottom: 25px;
    left: 50%;
    transform: translateX(-50%);
    width: 750px;
}

/* ChatGPT-style animated thinking bubble */
.typing-container {
    display: flex;
    justify-content: flex-start;
}

.typing-bubble {
    background: #f3f4f6;
    padding: 14px 18px;
    border-radius: 18px;
    margin-bottom: 18px;
    display: inline-block;
}

.dot {
    height: 6px;
    width: 6px;
    margin: 0 3px;
    background-color: #9ca3af;
    border-radius: 50%;
    display: inline-block;
    animation: bounce 1.4s infinite ease-in-out both;
}

.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1); }
}

</style>
""", unsafe_allow_html=True)

# ---------------- EMPTY STATE ----------------
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div style="text-align:center; margin-top:140px;">
        <h1 style="font-weight:600; font-size:38px;">Titanic AI</h1>
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

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user instantly
    st.markdown(
        f"""
        <div class="user-container">
            <div class="user-bubble">{prompt}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Thinking animation
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
        res = requests.post(API_URL, json={"question": prompt})
        thinking_placeholder.empty()

        if res.status_code == 200:
            data = res.json()
            answer = data["answer"]
            image = None

            if data.get("chart"):
                image_bytes = base64.b64decode(data["chart"])
                image = Image.open(io.BytesIO(image_bytes))

            # Display assistant response
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
            st.error("Server error")

    except Exception:
        thinking_placeholder.empty()
        st.error("Backend not running.")
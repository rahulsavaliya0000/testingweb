import streamlit as st
import time
from streamlit.components.v1 import html
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime  # Import datetime for timestamp

# --- Firebase Initialization ---
service_account_path = "portfolio-9843b-firebase-adminsdk-3n2cd-9000d279b5.json"
cred = credentials.Certificate(service_account_path)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db_firestore = firestore.client()

def store_response(question, answer):
    """
    Save the answer in the current session's Firestore document.
    If no document exists, create one with an empty 'answers' list.
    """
    # Create a new document for the session if it doesn't exist.
    if 'doc_id' not in st.session_state:
        doc_ref = db_firestore.collection("responses").document()
        doc_ref.set({"answers": []})
        st.session_state.doc_id = doc_ref.id
    else:
        doc_ref = db_firestore.collection("responses").document(st.session_state.doc_id)
    
    # Retrieve the current answers list, update it, and write it back.
    doc = doc_ref.get()
    data = doc.to_dict() or {}
    answers_list = data.get("answers", [])
    
    # Use datetime.utcnow() for a proper timestamp instead of firestore.SERVER_TIMESTAMP.
    new_answer = {
        "question": question,
        "answer": answer,
        "timestamp": datetime.utcnow()
    }
    answers_list.append(new_answer)
    doc_ref.set({"answers": answers_list}, merge=True)

# --- Streamlit UI and Assets ---
def inject_assets():
    st.markdown("""
    <style>
    :root {
        --rose: #FF1493;
        --dark-rose: #C71585;
        --bg-gradient: linear-gradient(135deg, #ffe4e1 0%, #fff0f5 100%);
    }
    body {
        color: var(--dark-rose) !important;
        background: var(--bg-gradient);
        font-family: 'Comic Sans MS', cursive !important;
    }
    @keyframes title-float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    .title-animation {
        animation: title-float 3s ease-in-out infinite;
        text-shadow: 2px 2px 4px rgba(255,20,147,0.3);
    }
    .message-bubble {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 25px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(255,20,147,0.1);
        border: 2px solid var(--rose);
    }
    .stButton>button {
        background: var(--rose) !important;
        color: white !important;
        border-radius: 25px !important;
        transition: all 0.3s ease !important;
        border: 2px solid var(--dark-rose) !important;
    }
    .stButton>button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 5px 15px rgba(255,20,147,0.4) !important;
        border-color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Floating hearts animation
    html("""
    <script>
    function createHearts() {
        const heart = document.createElement('div');
        heart.innerHTML = '💖💖💖💖💖💖';
        heart.className = 'heart';
        heart.style.left = Math.random() * 95 + '%';
        heart.style.fontSize = (20 + Math.random() * 30) + 'px';
        heart.style.animationDuration = (3 + Math.random() * 5) + 's';
        document.body.appendChild(heart);
        setTimeout(() => heart.remove(), 5000);
    }
    setInterval(createHearts, 300);
    </script>
    """)

# Initialize session state if not already set
if 'state' not in st.session_state:
    st.session_state.state = {
        'step': 0,
        'page': 'main',
    }

# Conversation steps and messages
convo = [
    {
        "message": "🌸 Hi Cutiee!! wanna play a game? 💖",
        "options": ["Always ready!", "tu puche ne hu na padu??", "obvious yrr"],
    },
    {
        "message": "What's your favorite food? 🍕",
        "options": ["Pizza🍕", "Your Lips👄", "Pasta", "Your cooking 😋"],
    },
    {
        "message": "Who's your favorite cricketer? 🏏",
        "options": ["Virat Kohli", "MS Dhoni", "Tushar", "Neighber 's DOG"],
    },
    {
        "message": "Who's your favorite actress? 🎬",
        "options": ["Rashmika", "Heer", "Alia", "ofcourse me"],
    }
]

def show_dhoni_popup():
    html("""
    <div class="popup">
        <h1 style="color: #c71585;">Doba jevi !! tari choice j kharab che!! like your Ex</h1>
        <h3 style="color: #ff1493;">😏 Mine is Dhoni! Next question ❤️</h3>
        <script>
            document.getElementById('typingSound').play();
        </script>
    </div>
    """)
    time.sleep(5)
    st.session_state.state['step'] = 3  # Move to actress question
    st.session_state.state['page'] = 'main'
    st.rerun()

def show_food_response():
    with st.empty():
        text = "AWWW, beb so sweet... mine favourite too! 💖"
        html("<script>document.getElementById('typingSound').play();</script>")
        placeholder = st.empty()
        for i in range(len(text) + 1):
            placeholder.markdown(f"""
            <div style="text-align: center;">
                <div class="typewriter" style="
                    animation: typing 2s steps({len(text)}) forwards,
                    blink-caret .75s step-end infinite;
                    width: {i}ch;
                ">{text[:i]}</div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.1)
        time.sleep(1)
        st.session_state.state['step'] = 2  # Move to cricketer question
        st.session_state.state['page'] = 'main'
        st.rerun()

def show_actress_typing():
    with st.empty():
        text = "AWWW, my favourite actress is..."
        html("<script>document.getElementById('typingSound').play();</script>")
        placeholder = st.empty()
        for i in range(len(text) + 1):
            placeholder.markdown(f"""
            <div style="text-align: center;">
                <div class="typewriter" style="
                    animation: typing 2s steps({len(text)}) forwards,
                    blink-caret .75s step-end infinite;
                    width: {i}ch;
                ">{text[:i]}</div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.1)
        time.sleep(1)
        st.session_state.state['page'] = 'final_reveal'
        st.rerun()

def show_final_reveal():
    html("<script>document.getElementById('revealSound').play();</script>")
    st.balloons()
    st.markdown("""
    <div class="popup">
        <h1 class="big-text" style="text-align: center; color: #C71585;">IT'S YOU! Baby 💖</h1>
    </div>
    """, unsafe_allow_html=True)

def main():
    inject_assets()
    st.markdown("""
    <h1 class="title-animation" style="text-align: center; color: #C71585;">
        MOST IMP Question's for Ansiii 💘
    </h1>
    <div style="height: 4px; background: linear-gradient(90deg, #FF69B4, #FF1493); margin: 10px auto 30px; width: 60%;"></div>
    """, unsafe_allow_html=True)
    
    if st.session_state.state['page'] == 'main':
        current_step = st.session_state.state['step']
        if current_step < len(convo):
            step = convo[current_step]
            st.markdown(f"""
            <div class="floating" style='
                font-size: 1.2em; 
                padding: 20px; 
                background: #c71585; 
                border-radius: 15px; 
                margin: 20px 0;
            '>{step['message']}</div>
            """, unsafe_allow_html=True)
            
            cols = st.columns(len(step['options']))
            for idx, option in enumerate(step['options']):
                with cols[idx]:
                    if st.button(option, key=f"opt{current_step}_{idx}"):
                        # Save the user's answer in the same document
                        store_response(step['message'], option)
                        
                        if current_step == 1:  # Food question
                            st.session_state.state['page'] = 'food_response'
                            st.rerun()
                        elif current_step == 2:  # Cricketer question: show Dhoni popup
                            st.session_state.state['page'] = 'dhoni_popup'
                            st.rerun()
                        elif current_step == 3:  # Actress question
                            st.session_state.state['page'] = 'actress_typing'
                            st.rerun()
                        else:
                            st.session_state.state['step'] += 1
                            st.rerun()
        else:
            st.session_state.state['page'] = 'final_reveal'
            st.rerun()
    
    elif st.session_state.state['page'] == 'dhoni_popup':
        show_dhoni_popup()
    
    elif st.session_state.state['page'] == 'food_response':
        show_food_response()
    
    elif st.session_state.state['page'] == 'actress_typing':
        show_actress_typing()
    
    elif st.session_state.state['page'] == 'final_reveal':
        show_final_reveal()
        if st.button("💖 Start Over 💖"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()

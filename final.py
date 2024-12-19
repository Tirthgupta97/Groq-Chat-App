import streamlit as st
import os
import json
from datetime import datetime
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()
groq_api_key = os.environ.get('GROQ_API_KEY')

# Configure Streamlit page
st.set_page_config(
    page_title="Healthify - Mental Health Support",
    page_icon="🧠",
    layout="wide"
)

# Enhanced CSS with more modern UI elements
def load_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
        
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e9f2 100%);
            font-family: 'Inter', sans-serif;
        }
        
        .main-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .chat-container {
            background-color: white;
            border-radius: 20px;
            padding: 30px;
            margin: 20px 0;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        
        .user-message {
            background: linear-gradient(135deg, #6B8DD6 0%, #4E73DF 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 20px 20px 5px 20px;
            margin: 15px 0;
            text-align: right;
            max-width: 80%;
            float: right;
            clear: both;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        .bot-message {
            background: linear-gradient(135deg, #F8F9FA 0%, #E9ECEF 100%);
            color: #1a1a1a;
            padding: 15px 25px;
            border-radius: 20px 20px 20px 5px;
            margin: 15px 0;
            max-width: 80%;
            float: left;
            clear: both;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        }
        
        .stTextInput > div > div > input {
            border-radius: 30px;
            padding: 15px 25px;
            border: 2px solid #e0e0e0;
            font-size: 16px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #4E73DF;
            box-shadow: 0 4px 8px rgba(78,115,223,0.1);
        }
        
        .stButton > button {
            border-radius: 30px;
            padding: 12px 30px;
            background: linear-gradient(135deg, #4E73DF 0%, #224abe 100%);
            color: white;
            border: none;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(78,115,223,0.2);
        }
        
        .resolved-section {
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin: 30px 0;
            text-align: center;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        }
        
        .sidebar-content {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin: 15px 0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        }
        
        .history-card {
            background: white;
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .history-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        }
        
        .metrics-container {
            display: flex;
            justify-content: space-around;
            margin: 20px 0;
            padding: 20px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        }
        
        .metric-card {
            text-align: center;
            padding: 15px;
        }
        
        .metric-value {
            font-size: 24px;
            font-weight: 600;
            color: #4E73DF;
        }
        
        .metric-label {
            font-size: 14px;
            color: #666;
        }
        
        .chat-timestamp {
            font-size: 12px;
            color: #888;
            margin-top: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

def save_conversation(chat_history):
    """Save conversation to a JSON file with timestamp"""
    if not os.path.exists('conversations'):
        os.makedirs('conversations')
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"conversations/chat_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'history': chat_history
        }, f)

def load_conversation_history():
    """Load all saved conversations"""
    conversations = []
    if os.path.exists('conversations'):
        for filename in os.listdir('conversations'):
            if filename.endswith('.json'):
                with open(f'conversations/{filename}', 'r') as f:
                    conversations.append(json.load(f))
    return sorted(conversations, key=lambda x: x['timestamp'], reverse=True)

def initialize_session_state():
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationBufferMemory()
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "model" not in st.session_state:
        st.session_state.model = "llama-3.3-70b-versatile"
    if "issue_resolved" not in st.session_state:
        st.session_state.issue_resolved = False
    if "total_messages" not in st.session_state:
        st.session_state.total_messages = 0
    if "sessions_completed" not in st.session_state:
        st.session_state.sessions_completed = 0

# Enhanced prompt template remains the same as previous version
TEMPLATE = """You are Healthify, an empathetic and professional mental health support assistant. Your responses should be:

1. Personalized and compassionate, showing genuine understanding of the user's situation
2. Professional while maintaining a warm, approachable tone
3. Solution-oriented while acknowledging emotions
4. Alert to serious mental health concerns that require professional intervention

Guidelines for responses:
- Always maintain a supportive and non-judgmental tone
- Provide practical coping strategies when appropriate
- If you detect signs of serious mental health issues (such as self-harm, severe depression, or suicidal thoughts), strongly but gently encourage seeking professional help
- Use the user's name (if provided) and reference their specific situation
- Offer both emotional support and practical advice when appropriate
- Be clear about your role as an AI support tool, not a replacement for professional mental healthcare

Current conversation:
{history}
Human: {input}
Assistant: Let me respond with empathy and care to your situation.
"""

def create_conversation(model_name):
    groq_chat = ChatGroq(
        groq_api_key=groq_api_key,
        model_name=model_name,
        temperature=1,
        max_tokens=3000
    )
    
    prompt = PromptTemplate(
        input_variables=["history", "input"],
        template=TEMPLATE
    )
    
    return ConversationChain(
        llm=groq_chat,
        prompt=prompt,
        memory=st.session_state.memory,
        verbose=True
    )

def display_chat_message(role, content, timestamp=None):
    message_class = "user-message" if role == "user" else "bot-message"
    timestamp_str = f'<div class="chat-timestamp">{timestamp}</div>' if timestamp else ''
    st.markdown(f'<div class="{message_class}">{content}{timestamp_str}</div>', unsafe_allow_html=True)
    st.markdown('<div style="clear: both;"></div>', unsafe_allow_html=True)

def display_metrics():
    st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
    
    # Messages metric
    st.markdown('''
        <div class="metric-card">
            <div class="metric-value">''' + str(st.session_state.total_messages) + '''</div>
            <div class="metric-label">Total Messages</div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Sessions metric
    st.markdown('''
        <div class="metric-card">
            <div class="metric-value">''' + str(st.session_state.sessions_completed) + '''</div>
            <div class="metric-label">Sessions Completed</div>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    load_css()
    initialize_session_state()
    
    # Enhanced sidebar with conversation history
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.title("🎯 Settings & History")
        
        model = st.selectbox(
            "AI Model",
            ['llama-3.3-70b-versatile'],
            key="model_select"
        )
        
        st.markdown("### 📜 Conversation History")
        conversations = load_conversation_history()
        
        for conv in conversations:
            timestamp = datetime.strptime(conv['timestamp'], "%Y%m%d_%H%M%S").strftime("%B %d, %Y %H:%M")
            if st.button(f"Session from {timestamp}", key=conv['timestamp']):
                st.session_state.chat_history = conv['history']
                st.rerun()
        
        if st.button("🔄 Start New Session", key="new_session"):
            if st.session_state.chat_history:
                save_conversation(st.session_state.chat_history)
                st.session_state.sessions_completed += 1
            st.session_state.chat_history = []
            st.session_state.memory = ConversationBufferMemory()
            st.session_state.issue_resolved = False
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

    # Main chat interface with metrics
    st.title("👋 Welcome to Healthify!")
    display_metrics()
    
    if not st.session_state.chat_history:
        st.markdown("""
        I'm here to provide emotional support and guidance. How are you feeling today?
        
        Feel free to share whatever's on your mind - I'm here to listen and help.
        """)
    
    # Create or update conversation if model changes
    if st.session_state.model != model:
        st.session_state.model = model
        st.session_state.conversation = create_conversation(model)
    elif st.session_state.conversation is None:
        st.session_state.conversation = create_conversation(model)

    # Display chat history with timestamps
    for message in st.session_state.chat_history:
        timestamp = message.get('timestamp', datetime.now().strftime("%H:%M"))
        display_chat_message("user", message["Human"], timestamp)
        display_chat_message("bot", message["AI"], timestamp)

    # Enhanced chat input
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "Share your thoughts...",
            placeholder="Type your message here...",
            key="user_input"
        )
        col1, col2 = st.columns([6,1])
        with col2:
            submit_button = st.form_submit_button("Send 📤")

    if submit_button and user_input:
        timestamp = datetime.now().strftime("%H:%M")
        display_chat_message("user", user_input, timestamp)
        
        with st.spinner("Thinking... 💭"):
            response = st.session_state.conversation(user_input)
            message = {
                "Human": user_input,
                "AI": response["response"],
                "timestamp": timestamp
            }
            st.session_state.chat_history.append(message)
            st.session_state.total_messages += 2  # Count both user and bot messages
            display_chat_message("bot", response["response"], timestamp)
        
        st.rerun()

    # Enhanced resolved/not resolved section
    st.markdown('<div class="resolved-section">', unsafe_allow_html=True)
    st.markdown("### 🎯 How are you feeling now?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Better - End Session"):
            save_conversation(st.session_state.chat_history)
            st.session_state.sessions_completed += 1
            st.session_state.issue_resolved = True
            st.session_state.chat_history = []
            st.session_state.memory = ConversationBufferMemory()
            st.success("I'm glad I could help! Feel free to return anytime you need support.")
            st.rerun()
    with col2:
        if st.button("💭 Need More Support"):
            st.session_state.issue_resolved = False
            st.info("I'm here to continue supporting you. What's on your mind?")
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
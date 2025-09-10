import streamlit as st
import time
import random
from huggingface_hub import InferenceApi

# -------------------------------
# Hugging Face API setup
# -------------------------------
api = InferenceApi(repo_id="microsoft/DialoGPT-small", token="xxxxxxxxxxxxxxxxx")

def ai_fallback(user_input):
    try:
        # Get raw response
        response = api(inputs=user_input, raw_response=True)
        # Extract the generated text
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "🤖 Sorry, I couldn't generate a response.")
        else:
            return "🤖 Sorry, I couldn't generate a response."
    except Exception as e:
        return f"🤖 Oops! I couldn’t process that. Error: {e}"


# -------------------------------
# FAQ Knowledge Base
# -------------------------------
faq_responses = {
    "programs": "🎓 **Programs Offered:**\n- Executive Leadership Mastery\n- Women in Leadership\n- Digital Leadership Transformation\n- Team Management Excellence\n- Strategic Leadership Development\n- Entrepreneurial Leadership",
    "duration": "⏱️ **Program Duration:**\n- Executive Leadership Mastery: 12 weeks\n- Women in Leadership: 8 weeks\n- Digital Leadership Transformation: 10 weeks\n- Team Management Excellence: 6 weeks\n- Strategic Leadership Development: 16 weeks\n- Entrepreneurial Leadership: 8 weeks",
    "online": "💻 Most programs are **online**, with live sessions and recorded content for flexibility.",
    "offline": "🏢 Some workshops and labs are **offline** in major cities, but most learning is online.",
    "certificate": "📜 **Certificates:** Participants receive official certificates and digital badges for LinkedIn.",
    "mentors": "👩‍🏫 **Mentors:**\n- Dr. Sarah Mitchell: Former Fortune 500 CEO\n- Maria Rodriguez: Tech entrepreneur\n- Amanda Chen: Executive Coach, Harvard Business School\n- Jennifer Thompson: Ex-McKinsey Partner",
    "cost": "💰 **Program Fees:** Varies by program. Scholarships and flexible payment options available.",
    "application": "📝 **Apply:** Visit Iron Lady's website, fill the short form, and receive instructions by email.",
    "support": "🤝 **Support:** Contact hello@ironlady.com or call +1-800-IRON-LADY.",
    "alumni": "🌟 **Alumni Network:** 10,000+ women leaders worldwide with events and networking opportunities."
}

aliases = {
    "cost": ["fees", "price", "cost"],
    "programs": ["programs", "courses"],
    "duration": ["duration", "time", "length"],
    "certificate": ["certificate", "certificates", "credibility"],
    "mentors": ["mentor", "mentors", "coach", "coaches"],
    "online": ["online", "virtual", "remote"],
    "offline": ["offline", "in-person", "classroom"],
    "application": ["apply", "application", "registration"],
    "support": ["support", "help", "contact"],
    "alumni": ["alumni", "network"]
}

# -------------------------------
# Response function
# -------------------------------
def get_response(user_input):
    user_input = user_input.lower().strip()

    # --------------------
    # FAQ matching first
    # --------------------
    for key, alias_list in aliases.items():
        if key in user_input or any(alias in user_input for alias in alias_list):
            return f"🤓 Here’s what I found about **{key}**:\n{faq_responses[key]}"
    
    # Greetings
    
    if any(word in user_input for word in ["hi", "hello", "hey", "how are you"]):
        return "👋 Hi there! I’m Iron Lady Bot. How can I help you explore our leadership programs today? 😊"
    
    # Thanks
    if user_input in ["thanks", "thank you"]:
        return "😊 You’re welcome! Happy to help you grow as a leader."
    
    # Goodbye
    if user_input in ["bye", "goodbye"]:
        return "👋 Goodbye! Keep leading with confidence and inspiration!"
    
    # AI fallback
    return "🤖 Let me think about that...\n" + ai_fallback(user_input)

# Streamlit Setup
st.set_page_config(page_title="Iron Lady Chatbot", page_icon="👩‍💼", layout="centered")

# CSS Styling
st.markdown("""
<style>
body, .stApp { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
.chat-container { background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); border-radius: 20px; padding: 2rem; box-shadow: 0 20px 40px rgba(0,0,0,0.1); margin-bottom:2rem; border:1px solid rgba(255,255,255,0.2);}
.chat-header { text-align:center; padding-bottom:1rem; }
.chat-title { background: linear-gradient(135deg, #ff6b6b, #ee5a24); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size:2rem; font-weight:700; }
.chat-subtitle { color:#333; font-size:1rem; }
.user-message { background: linear-gradient(135deg,#ff9a9e,#fecfef); color:black; padding:12px 16px; border-radius:18px; border-bottom-right-radius:4px; margin:0.5rem 0; margin-left:20%; box-shadow:0 2px 10px rgba(255,154,158,0.3);}
.bot-message { background: linear-gradient(135deg,#E6E6FA,#D8BFD8); color:black; padding:12px 16px; border-radius:18px; border-bottom-left-radius:4px; margin:0.5rem 0; margin-right:20%; box-shadow:0 2px 10px rgba(102,126,234,0.3);}

button[class*="stButton"] > div {
    color: white !important;
    background: linear-gradient(135deg,#667eea,#764ba2) !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 8px 20px !important;
    margin:4px;
    text-align:center;
}
button[class*="stButton"] > div:hover {
    background: linear-gradient(135deg,#ff6b6b,#ee5a24) !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="chat-container">
    <div class="chat-header">
        <h1 class="chat-title">🏆 Iron Lady Leadership Assistant</h1>
        <p class="chat-subtitle">AI-Powered Guide to Transform Your Leadership Journey</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# -------------------------------
# Pyramid-style quick buttons
# -------------------------------
button_rows = [
    [("📚 Programs", "programs"), ("⏱ Duration", "duration"), ("👩‍🏫 Mentors", "mentors")],
    [("💻 Online/Offline", "online"), ("📜 Certificates", "certificate"), ("💰 Fees", "cost")],
    [("📝 Apply", "application"), ("🤝 Support", "support")],
    [("🌟 Alumni", "alumni")]
]

for i, row in enumerate(button_rows):
    st_columns = st.columns(len(row) + 2)
    start_index = (len(st_columns) - len(row)) // 2
    for j, (label, key) in enumerate(row):
        if st_columns[start_index + j].button(label, key=f"{label}_{i}"):
            st.session_state["messages"].append({"role": "user", "content": f"Can you tell me about {label}?"})
            with st.spinner("🤖 Thinking..."):
                time.sleep(random.uniform(0.5, 1.2))
                response = get_response(key)
            st.session_state["messages"].append({"role": "bot", "content": response})

# -------------------------------
# Chat input
# -------------------------------
user_input = st.chat_input("Type your question here...")
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.spinner("🤖 Thinking..."):
        time.sleep(random.uniform(0.5, 1.2))
        response = get_response(user_input)
    st.session_state["messages"].append({"role": "bot", "content": response})

# -------------------------------
# Display chat
# -------------------------------
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-message">👤 {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

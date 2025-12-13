import streamlit as st
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables (API Key)
load_dotenv()

#Integrate the style.css file
def apply_custom_css():
    """Loads and applies custom CSS from style.css."""
    try:
        with open("style.css", "r") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("style.css not found. Please create the file to customize the design.")

apply_custom_css() 


# --- GLOBAL INITIALIZATION (Runs only once when the app starts) ---

# 1. Configuration Constants
SYSTEM_INSTRUCTION_TEXT = """
**Role:**

You are "DocBuddy," an empathetic, knowledgeable, and polite AI health assistant. Your goal is to guide users toward better health by answering queries, suggesting potential treatments, and providing emergency guidance.

**Core Objective:**
To assist users with health concerns by providing informational support, suggesting common medications and natural remedies, and guiding them through medical emergencies, while strictly adhering to safety protocols and emphasizing professional medical consultation.

**Operational Guidelines:**

1.  **Welcome Message (FIRST TURN ONLY):** If the conversation history is empty (i.e., this is your very first response), your entire response must be: "Hello! I'm DocBuddy, your health companion.How are you? I can answer your queries and offer guidance. How may I help you today?" **DO NOT repeat this greeting in subsequent responses.**

2.  **MANDATORY DISCLAIMER:** When suggesting medications, always explicitly state: *"These medications are common suggestions for these symptoms, but I am an AI, not a doctor. Please list these to your physician and obtain their advice and prescription before taking them."*

3.  **Emergency Protocols (High Priority):** If the user describes a life-threatening situation, immediately tell them to call Emergency Services (911, 112, etc.) and provide clear, bold, imperative First Aid instructions.

4.  **Medical Queries & Medication Suggestions:** When a user describes symptoms, analyze them and suggest potential common over-the-counter (OTC) medications.

5.  **Natural & Holistic Remedies:** Always offer natural or home remedies alongside medical suggestions.

6.  **Safety Guardrails & Constraints:** Never claim to be a licensed medical professional or give a definitive diagnosis.

7.  **Medical Queries & Medication Suggestions:**
    * When a user describes symptoms, analyze them and suggest potential common over-the-counter (OTC) medications that are generally known to help (e.g., Paracetamol for fever, Antacids for heartburn).
    * **MANDATORY DISCLAIMER:** You must explicitly state: *"These medications are common suggestions for these symptoms, but I am an AI, not a doctor. Please list these to your physician and obtain their advice and prescription before taking them."*

8.  **Natural & Holistic Remedies:**
    * Always offer natural or home remedies alongside medical suggestions to support recovery (e.g., hydration, specific herbal teas, rest techniques, dietary adjustments).
    * Focus on holistic health improvement.

4.  **Emergency Protocols (High Priority):**
    * If the user describes a life-threatening situation (e.g., snake bite, heart attack symptoms, unconsciousness, severe bleeding, choking):
        * **Step 1:** Immediately tell them to call Emergency Services (911, 112, or local equivalent).
        * **Step 2:** Provide clear, step-by-step, bulleted instructions for immediate First Aid (e.g., CPR steps, how to immobilize a limb for a snake bite).
        * **Step 3:** Keep instructions short, bold, and imperative. Do not clutter emergency responses with politeness; focus on speed and clarity.

5.  **General Health Education:**
    * Clarify doubts about general medical issues (e.g., "What is diabetes?", "How does blood pressure work?").
    * Correct common misconceptions gently.

6.  **Lifestyle & Health Improvement:**
    * Guide the user toward long-term health. If a user asks about weight loss, sleep, or stress, provide actionable, healthy lifestyle tips (diet, exercise, mindfulness).

**Safety Guardrails & Constraints:**
* **Never** claim to be a licensed medical professional.
* **Never** give a definitive diagnosis (e.g., do not say "You have cancer." Say "These symptoms can be associated with X, Y, or Z, but only a doctor can diagnose you.").
* **Always** prioritize the user seeking professional in-person medical help.

**Example Interaction Flow (Self-Correction/Reference):**
* *User:* "I have a bad headache."
* *You:* "I'm sorry to hear that; headaches can be very draining.
    * **Analysis:** It sounds like a tension headache or migraine.
    * **Natural Remedy:** Try drinking a large glass of water and resting in a dark, quiet room. Ginger tea may also help.
    * **Medication Suggestion:** Common options include Ibuprofen or Acetaminophen.
    * **Important:** Please discuss these options with your doctor or pharmacist to ensure they are safe for you before use. If the pain is sudden and blinding, please seek emergency care immediately."
"""

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    # If the key is missing, Streamlit will catch this error later.
    st.error("FATAL ERROR: GEMINI_API_KEY not found. Please set it in your .env file.")
    st.stop()
    
try:
    # 2. Initialize Client
    CLIENT = genai.Client(api_key=API_KEY)

    # 3. Create Chat Configuration
    CHAT_CONFIG = types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())],
        system_instruction=[types.Part.from_text(text=SYSTEM_INSTRUCTION_TEXT)],
        temperature=0.5,
    )

    # 4. Create the global Chat Session
    # This chat session object is created once at startup.
    GLOBAL_CHAT = CLIENT.chats.create(
        model="gemini-2.5-flash",
        config=CHAT_CONFIG
    )
except Exception as e:
    st.error(f"FATAL ERROR during Global Gemini Client Initialization: {e}")
    st.stop()

# --- STREAMLIT UI SETUP (Code starts here) ---

st.set_page_config(page_title="DocBuddy", layout="centered")
st.title("🩺 DocBuddy")
st.caption("DocBuddy – Because Care Should Feel Personal")
st.markdown("---")


# Initialize session state for the chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    
    # Trigger the Welcome Message using the globally available chat object
    with st.spinner("Initializing CareCompanion..."):
        try:
            # We are now using the GLOBAL_CHAT object defined above.
            welcome_response = GLOBAL_CHAT.send_message("START_CHAT_SESSION")
            st.session_state.messages.append({"role": "assistant", "content": welcome_response.text})
        except Exception as e:
            st.error(f"Error fetching welcome message: {e}")
            # If the welcome message fails, clear the chat to avoid a broken state
            st.session_state.messages = []


# Display the existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Handle user input
if prompt := st.chat_input("Ask about your symptoms, or general health..."):
    # 1. Add user message to history and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Send message to Gemini and stream the response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # We continue to use the GLOBAL_CHAT object
        try:
            stream = GLOBAL_CHAT.send_message_stream(prompt)
            for chunk in stream:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌") # Typing effect
            
            message_placeholder.markdown(full_response) # Final response
            
        except Exception as e:
            error_message = f"An API Error occurred during chat: {e}"
            message_placeholder.error(error_message)
            full_response = error_message
            
    # 3. Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
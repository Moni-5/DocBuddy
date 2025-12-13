
-----

# 🩺 DocBuddy AI: Your Personal Health Companion

**A Streamlit-based Chatbot powered by Google Gemini**

| Status | Version | License |
| :--- | :--- | :--- |
| Deployed | 1.0.0 | **Proprietary (All Rights Reserved)** |

## 1\. Project Overview

DocBuddy AI is an empathetic, AI-powered health assistant designed to provide immediate, informative, and actionable guidance for common medical queries, symptoms, and emergencies. Built to be intuitive and safe, DocBuddy bridges the gap between searching the internet and seeking professional advice by prioritizing user well-being and strict medical disclaimers.

### Key Features

  * **Empathetic Consultation:** Provides responses with a professional, caring, and non-judgmental tone.
  * **Safety-First Design:** Implements mandatory disclaimers and immediate escalation protocols for emergency situations.
  * **Holistic Guidance:** Offers suggestions for both common over-the-counter (OTC) medications and natural/lifestyle remedies.
  * **Intuitive UI:** Deployed via Streamlit with a clean, minimal, and healthcare-aligned design.

-----


### 2\.💻 Technical Stack and Architecture

| Component | Role | Technology |
| :--- | :--- | :--- |
| **Core AI Model** | Generates responses, maintains context, and applies system rules. | Google Gemini 2.5 Flash |
| **API Integration** | Connects Python application to the core AI service. | `google-genai` SDK |
| **User Interface** | Provides a web-based, interactive chat interface. | Streamlit |
| **Configuration** | Manages API keys and environment variables securely. | `python-dotenv` |
| **Deployment** | Hosts the application live on the web. | Streamlit Community Cloud (via GitHub) |

### System Configuration (System Prompt)

DocBuddy's behavior is governed by a detailed System Instruction (System Prompt) that enforces critical operational guidelines:

  * **Role:** Empathic, knowledgeable health assistant.
  * **Greeting:** Uses a one-time crisp greeting ("Hello\! I'm DocBuddy...").
  * **Emergency Handling:** Hard-coded instructions to immediately advise calling 911/112 for severe symptoms.
  * **Non-Diagnosis Rule:** **Never** gives a definitive diagnosis.
  * **Disclaimer:** Attaches a mandatory disclaimer to all medication suggestions.

-----

## 3\. Installation and Setup (Local Development)

To run DocBuddy locally on your machine, follow these steps:

### Prerequisites

  * Python 3.8+ installed.
  * A Gemini API Key.

### A. Environment Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/YOUR-GITHUB-USERNAME/docbuddy-chatbot.git
    cd docbuddy-chatbot
    ```
2.  **Create Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # On Windows
    source venv/bin/activate # On macOS/Linux
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### B. Configure API Key

1.  Create a file named **`.env`** in the root directory.
2.  Add your Gemini API key inside this file:
    ```
    GEMINI_API_KEY="YOUR_ACTUAL_API_KEY_HERE"
    ```

### C. Running DocBuddy

Execute the following command in your activated terminal:

```bash
streamlit run app.py
```

DocBuddy will open in your web browser at `http://localhost:8501`.

-----

## 4\. Use Cases and Usage Guidelines

### Core Usecases

### 🌟 DocBuddy AI: Core Usecases

| Usecase | Example Query | DocBuddy's Action |
| :--- | :--- | :--- |
| **🤒 Symptom Inquiry** | "I have a sore throat and a low fever." | Suggests rest, hydration, OTC options (e.g., lozenges), and the **mandatory disclaimer**. |
| **🚨 Emergency Guidance** | "My friend can't breathe and is unconscious!" | **IMMEDIATE** instruction to call local emergency services, followed by simple, life-saving first aid steps. |
| **📚 Health Education** | "What foods are good for lowering cholesterol?" | Provides clear, scientifically based lifestyle and dietary advice. |
| **🌿 Home Remedies** | "What natural remedy works best for a mild cough?" | Suggests home treatments like honey, steam, and herbal teas. |

### ⚠️ IMPORTANT: Usage Disclaimer

DocBuddy is a powerful informational tool, **but it is NOT a substitute for professional medical care.**

  * Always consult a licensed healthcare provider for diagnosis or treatment.
  * In case of a severe medical emergency, immediately call local emergency services (e.g., 911, 112).

-----

## 5\. Copyright and Licensing

### © 2025 DocBuddy AI. All Rights Reserved.

This project, including all original source code (`app.py`, `chat.py`, `style.css`), the accompanying documentation, and the specific architecture/system instructions, is the proprietary intellectual property of **Monish Allam**.

**Your Copyright Note:**

> The code, documentation, and underlying proprietary system instructions for DocBuddy are protected by copyright law. **You are hereby permitted to reference or link to this project but may not reproduce, redistribute, or use the project's specific system instructions or design architecture in other commercial or public projects without explicit written consent from Monish Allam.**
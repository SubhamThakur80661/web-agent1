# 🤖 JARVIS - AI Autonomous Shopping Agent

**JARVIS** is an intelligent web automation agent powered by **Groq/OpenAI** and **Playwright**. It autonomously navigates e-commerce websites, performs complex tasks like sorting products, adding items to the cart, and filling out checkout forms—all while talking to you in a cool sci-fi voice.

## ✨ Features

-   **🧠 AI Brain:** Uses Llama 3 (via Groq) to analyze HTML and make decisions in real-time.
-   **🗣️ Voice Feedback:** Speaks its thoughts and actions using Google Text-to-Speech (gTTS) and Pygame background audio.
-   **👁️ Cyberpunk UI:** Highlights elements with a futuristic Cyan/Green glow before interacting.
-   **⚡ Auto-Login:** Bypasses login screens automatically for faster execution.
-   **🛡️ Robust Error Handling:** Detects visual interference or API limits and retries automatically.

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

-   [Python 3.8+](https://www.python.org/downloads/)
-   [VS Code](https://code.visualstudio.com/) (Recommended)
-   A **Groq API Key** (Get it for free [here](https://console.groq.com/keys))

## 🚀 Installation

1.  **Clone the Repository**
    ```bash
    git clone (https://github.com/SubhamThakur80661/web-agent1)
    cd ai-shopping-agent
    ```

2.  **Create a Virtual Environment (Optional but Recommended)**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Playwright Browsers**
    ```bash
    playwright install
    ```

## ⚙️ Configuration

1.  Open `main.py` in your code editor.
2.  Find the line `MY_API_KEY = "PASTE_YOUR_NEW_KEY_HERE"`.
3.  Replace `PASTE_YOUR_NEW_KEY_HERE` with your actual **Groq API Key**.

> **⚠️ Important:** Never commit your actual API key to GitHub. Use environment variables for safety in production.

## 🎮 Usage

Run the agent with a single command:

```bash
python main.py

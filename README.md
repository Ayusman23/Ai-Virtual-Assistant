# J.A.R.V.I.S - Advanced AI Voice Assistant

J.A.R.V.I.S is a highly capable, professional, and real-time AI voice assistant designed to assist with a variety of tasks ranging from general inquiries to complex mathematical problem-solving and multi-modal file analysis.

## 🚀 Key Features

### 👤 Advanced Authentication
*   **Face Recognition:** Secure access using local face authentication.
*   **Face Training:** Integrated training module to improve recognition accuracy directly from the UI.

### 🧠 Intelligent Brain (Gemini 2.0 Flash)
*   **Contextual Reasoning:** Remembers the context of uploaded files or previous interactions.
*   **Multi-modal Analysis:** Understands and describes images using Vision AI.
*   **Complex Problem Solving:** Solves logic puzzles and word problems with step-by-step reasoning.
*   **Real-time Data:** Access to current time, date, weather, and news.

### 📁 Content Analysis
*   **Folder Analysis:** Upload a folder to get a technical summary of its purpose, tech stack, and structure.
*   **File Analysis:** Deep-reads text and code files to provide insights or answer specific questions.
*   **Image Interpretation:** Analyze images to extract text, identify objects, or solve visual problems.

### 🛠️ Utility & Automation
*   **Math Engine:** Combined power of Wolfram Alpha for calculations and Gemini for logic.
*   **App Control:** Open desktop applications or websites with simple voice commands.
*   **YouTube Integration:** Instantly search and play videos.
*   **Communication:** Send messages or make calls via WhatsApp or mobile.

### 🖥️ Professional Interface
*   **Siri-Wave Animation:** Smooth, interactive voice wave during speech.
*   **Text Rendering:** Real-time character-by-character text typing for responses.
*   **Stop Button:** Ability to interrupt the assistant's speech and return to the main chat instantly.

---

## 🛠️ Technology Stack

*   **Logic:** [Python 3.10+](https://www.python.org/)
*   **Frontend-Backend Bridge:** [Eel](https://github.com/python-eel/Eel)
*   **Frontend:** HTML5, Vanilla CSS, JavaScript (jQuery)
*   **AI Engine:** [Google Gemini API](https://ai.google.dev/)
*   **Voice:** Pyttsx3 (TTS), SpeechRecognition (STT), Pygame (Audio)
*   **Database:** SQLite3
*   **Computer Vision:** OpenCV, face_recognition
*   **Math API:** [Wolfram Alpha](https://www.wolframalpha.com/)
*   **Developer Tools:** ADB (Android Debug Bridge) for device integration.

---

## ⚙️ Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Ayusm23/jarvis.git
    cd jarvis
    ```

2.  **Set Up Virtual Environment:**
    ```bash
    python -m venv venv
    .\venv\Scripts\Activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure API Keys:**
    Add your keys in `engine/config.py` or directly in `engine/features.py`:
    *   `LLM_KEY` (Gemini API)
    *   `WOLFRAM_APP_ID`
    *   `OPENWEATHER_KEY`
    *   `NEWS_API_KEY`

5.  **Initialize Database:**
    ```bash
    python init_db.py
    ```

---

## 🏃 How to Run

To start the full platform (UI and Hotword listening):
```bash
python run.py
```

---

## 📄 License

This project is for educational purposes. Feel free to modify and adapt it for your needs.

---

Created with ❤️ by Ayusman

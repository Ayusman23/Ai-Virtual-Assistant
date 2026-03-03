# J.A.R.V.I.S - Advanced AI Voice Assistant

J.A.R.V.I.S is a highly capable, professional, and real-time AI voice assistant designed to assist with a variety of tasks ranging from general inquiries to complex mathematical problem-solving and multi-modal file analysis.

---

## 🚀 Key Features

### 👤 Advanced Authentication

* **Face Recognition:** Secure access using local face authentication.
* **Face Training:** Integrated training module to improve recognition accuracy directly from the UI.

### 🧠 Intelligent Brain (Gemini 2.0 Flash)

* **Contextual Reasoning:** Remembers the context of uploaded files or previous interactions.
* **Multi-modal Analysis:** Understands and describes images using Vision AI.
* **Complex Problem Solving:** Solves logic puzzles and word problems with step-by-step reasoning.

### 📁 Content Analysis & Interface

* **Folder Analysis:** Upload a folder to get a technical summary of its purpose and structure.
* **Siri-Wave Animation:** Smooth, interactive voice wave during speech.
* **Text Rendering:** Real-time character-by-character text typing for responses.

### 🛠️ Utility & Automation

* **Math Engine:** Combined power of Wolfram Alpha for calculations and Gemini for logic.
* **App Control:** Open desktop applications or websites with simple voice commands.
* **Communication:** Send messages or make calls via WhatsApp or mobile.

---

## 📸 Gallery & Development

### Conversation & Chat History

Track your interactions through a sleek, threaded chat interface.

### Assistant Settings & Backend

Customize your profile and manage system configurations directly from the dashboard.

---

## 📺 Demo Video

Experience the real-time capabilities of J.A.R.V.I.S:

---

## 🛠️ Technology Stack

* **Logic:** [Python 3.10+](https://www.python.org/)
* **Frontend-Backend Bridge:** [Eel](https://github.com/python-eel/Eel)
* **Frontend:** HTML5, Vanilla CSS, JavaScript (jQuery)
* **AI Engine:** [Google Gemini API](https://ai.google.dev/)
* **Voice:** Pyttsx3 (TTS), SpeechRecognition (STT), Pygame (Audio)
* **Database:** SQLite3
* **Computer Vision:** OpenCV, face_recognition
* **Math API:** [Wolfram Alpha](https://www.wolframalpha.com/)

---

## ⚙️ Installation & Setup

1. **Clone the Repository:**
```bash
git clone https://github.com/Ayusman23/Ai-Virtual-Assistant.git
cd Ai-Virtual-Assistant

```


2. **Set Up Virtual Environment:**
```bash
python -m venv venv
.\venv\Scripts\Activate

```


3. **Install Dependencies:**
```bash
pip install -r requirements.txt

```


4. **Configure API Keys:**
Add your keys in `engine/config.py`:
* `LLM_KEY` (Gemini API)
* `WOLFRAM_APP_ID`
* `OPENWEATHER_KEY`


5. **Initialize Database:**
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

Created with ❤️ by **Ayusman Samantaray**
Final Year B.Tech CSE Student, GCEK Bhawanipatna

---

### Final Push Instructions (CMD):

After you copy the text above into your `README.md` file, run these commands in your Windows Command Prompt to update your GitHub:

1. `git add .`
2. `git commit -m "Final README update with correct asset names and video"`
3. `git pull origin main --rebase`
4. `git push origin main`


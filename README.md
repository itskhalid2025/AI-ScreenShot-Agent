
---

# 🧠 AI Screenshot Agent

> **Capture • Analyze • Report** – An intelligent screenshot capturing and analysis tool that integrates with **Telegram** and **Google Gemini API** to analyze on-screen content such as code, questions, or images.

---

## 📘 Description

**AI Screenshot Agent** is an automation tool that allows you to take screenshots instantly, analyze them using **Google Gemini**, and receive detailed AI-generated insights directly in your **Telegram chat**.

This script is particularly useful for:

* **Students & Developers** who want instant code explanations or debugging help.
* **Educators & Trainers** who wish to analyze MCQs, coding exercises, or documents visually.
* **Professionals** who need automated screen documentation with analysis and archiving.

With simple keyboard shortcuts, the system captures multiple screenshots, sends them to your Telegram chat, and leverages **Google Gemini’s multimodal capabilities** to analyze the images — providing intelligent, structured, and contextual feedback.

---

## ⚙️ Features

✅ **Keyboard-Controlled Capture System**

* `Caps Lock`: Start/Stop screenshot collection.
* `Right Shift`: Take additional screenshots while collecting.
* `Ctrl + C`: Exit the program.

✅ **Automatic Screenshot Storage**

* Screenshots are saved locally in your specified folder (default: `C:\Users\<YourName>\Downloads\vcam\Screenshots`).
* Each file is timestamped and indexed for easy reference.

✅ **AI-Powered Screenshot Analysis**

* Uses **Google Gemini API (Gemini 1.5 Flash)** to analyze the screenshots.
* Understands **code snippets**, **MCQs**, **questions**, and **images**.
* Produces **detailed answers, improvements, and explanations**.

✅ **Seamless Telegram Integration**

* Automatically sends captured images to your **Telegram Bot** and **Chat ID**.
* AI analysis results are sent as structured text messages in your Telegram chat.
* Automatically handles message chunking for long results (over 4000 characters).

✅ **Error-Handled & Stable**

* Graceful exception handling for network, API, and file operations.
* Prevents rate limit violations via controlled message timing.
* CPU-efficient with time delays between keypress polls.

---

## 🧩 How It Works

### 1. Start the Agent

When you run the script, it initializes and displays:

* Screenshot folder path
* Telegram credentials
* Available keyboard controls
* Workflow summary

Example startup output:

```
🤖 AI Screenshot Agent Started!
📁 Screenshots folder: C:\Users\KHALID\Downloads\vcam\Screenshots
💬 Telegram Chat ID: 5855425119
🔑 Using Google Gemini API
🎮 Controls:
  Caps Lock → Start/Stop screenshot collection
  Right Shift → Take screenshot (while collecting)
  Ctrl+C → Exit
```

---

### 2. Capture Screenshots

* Press **Caps Lock** to start capturing.
* The first screenshot is automatically taken and stored.
* Press **Right Shift** to take more screenshots.
* Press **Caps Lock** again to stop capturing and start analysis.

---

### 3. Send & Analyze

Once stopped:

1. All captured images are **sent to your Telegram** chat (for record keeping).
2. Images are **encoded and sent to the Google Gemini API** for analysis.
3. Gemini analyzes the images and generates a **comprehensive textual report**, including:

   * Code explanations and suggestions.
   * Correct answers for MCQs or fill-in-the-blanks.
   * Logical analysis of any visual question.
4. The AI-generated report is **automatically delivered to your Telegram chat** in one or multiple messages (if long).

---

### 4. Example Telegram Output

**Screenshot Delivery:**

> 📸 Screenshot 1/3 – `screenshot_1728653781_1.png`

**AI Report Example:**

```
🔍 AI Analysis Results:
📊 Screenshots analyzed: 3
🕐 Analysis time: 2025-10-11 20:35:10
📁 Saved to: C:\Users\KHALID\Downloads\vcam\Screenshots

==================================================
📋 DETAILED ANALYSIS:
==================================================
Question 1: The output of the given Python code is ...
Answer: 25
Explanation: The code squares the input number, hence result is ...
```

---

## 🧠 Architecture Overview

```
+---------------------------+
|   Keyboard Event Handler  |
+-----------+---------------+
            |
            v
+---------------------------+
|     Screenshot Capture    | → Saves to Local Folder
+-----------+---------------+
            |
            v
+---------------------------+
|   Base64 Image Encoding   |
+-----------+---------------+
            |
            v
+---------------------------+
|   Telegram API (Send)     | → Sends images to your chat
+-----------+---------------+
            |
            v
+---------------------------+
|   Google Gemini API Call  |
|   (via POST request)      |
+-----------+---------------+
            |
            v
+---------------------------+
| AI Text Response Parsing  |
| → Sends structured output |
+---------------------------+
```

---

## 🧩 Installation Guide

### 🖥️ Prerequisites

Make sure you have:

* **Python 3.8+** installed.
* **PIP** package manager.
* A **Telegram Bot Token** (from [@BotFather](https://t.me/BotFather)).
* A **Telegram Chat ID** (get via [@userinfobot](https://t.me/userinfobot)).
* A **Google Gemini API key** (from [Google AI Studio](https://aistudio.google.com)).

---

### 📦 Required Libraries

Install the dependencies using:

```bash
pip install pillow requests keyboard
```



### ⚙️ Configuration

Edit the script and set your credentials:

```python
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
SCREENSHOT_FOLDER = r"C:\Path\To\Screenshots"
```

---

### ▶️ Run the Program

```bash
python ai_screenshot_agent.py
```

Once running, follow the on-screen key instructions:

* Press **Caps Lock** to start/stop capturing.
* Press **Right Shift** to take additional screenshots.
* Press **Ctrl + C** to stop the agent.

---

## 🧾 Example Use Cases

| Use Case             | Description                                                                      |
| -------------------- | -------------------------------------------------------------------------------- |
| 🧑‍💻 Code Helper    | Capture your screen while coding — get instant AI suggestions & optimizations.   |
| 📚 Quiz Solver       | Take screenshots of MCQs or handwritten questions — receive answers & reasoning. |
| 📝 Document Reviewer | Capture forms, reports, or notes — AI summarizes and explains them.              |
| 🧠 Study Assistant   | Use it during online learning to get contextual answers instantly.               |

---

## ⚠️ Important Notes

* The **Google Gemini API** may have usage limits based on your account quota.
* **Telegram Bot API** allows sending only certain file sizes (up to ~50MB per image).
* Avoid using this tool for sensitive data — screenshots are transmitted to third-party services (Telegram, Google API).
* Works only on **Windows** (as `ImageGrab` requires a display environment).

---

## 🧑‍💻 Author

**Developed by:** Mohammed Khalid
**Language:** Python 3
**Version:** 1.0
**License:** MIT

---

## ⭐ Future Enhancements

* Add cross-platform screenshot support (Linux/macOS).
* Include OCR for extracting text directly from images.
* Integrate speech-to-text and text-to-speech options.
* Real-time desktop monitoring for automatic analysis triggers.

---


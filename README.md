# Project Title

Standardize simulation-based training processes. Enhance learner competency tracking and assessment. Enable scalable integration of AI in the future

---

## 📌 Table of Contents
- Overview
- Features
- Project Structure
- Installation
- Usage
- Configuration
- Examples
- Contributing
- License
- Contact

---

## 🧠 Overview

Explain:
- The problem this project addresses  
- The main idea or solution  
- Who this project is for  

---

## ✨ Features

- Feature 1  
- Feature 2  
- Feature 3  

---

## 📂 Project Structure
```
code/
├── data/                         
│
├── source/
│   ├── __init__.py
│
│   ├── analysis/                 # analysis emotion
│   │   ├── __init__.py
│   │   └── deepface_thread.py
│
│   ├── audio/                    # handle audio
│   │   ├── __init__.py
│   │   ├── audio_module.py
│   │   └── speak_module.py
│
│   ├── video/                    # handle video / lipsync
│   │   ├── __init__.py
│   │   └── wav2lip/              # https://github.com/Rudrabha/Wav2Lip 
│
│   ├── cache/                    # cache disk / image
│   │   ├── __init__.py
│   │   ├── disk_cache.py
│   │   └── disk_image_list_cache.py
│
│   ├── llm/                      # LLM / API
│   │   ├── __init__.py
│   │   ├── key_data.py
│   │   ├── api_client.py
│   │   └── groq_ai.py
│
│   ├── ui/                       # UI for user
│   │   ├── __init__.py
│   │   ├── start_window.py
│   │   ├── setup_frame.py
│   │   ├── main_frame.py
│   │   ├── main_panel.py
│   │   ├── panel_camera.py
│   │   ├── panel_speak.py
│   │   ├── confirm_frame.py
│   │   ├── ice_phase_frame.py
│   │   ├── cream_phase_frame.py
│   │   ├── dialog_change_name.py
│   │   └── frame_prompt.py
│   └── main.py                   # entry point
│
├── requirements.txt
└── README.md
```
---

## ⚙️ Installation

### Prerequisites
- Python == 3.9
- Git

### Steps
```
git clone https://github.com/sonvi95/AI_Tool/tree/main
cd project-name  
pip install -r requirements.txt
```
---

## 🚀 Usage
```
python main.py
```
---

## 🔧 Configuration

Describe important configuration options here.
Need to download the source/video/wav2lip to run it.
Refer: https://github.com/Rudrabha/Wav2Lip
---

## 🧪 Examples

Provide sample inputs / outputs, screenshots, or demo links.

---

## 🤝 Contributing

1. Fork the repository  
2. Create a new branch  
3. Commit your changes  
4. Open a Pull Request  

---

## 📄 License

MIT License

---

## 📬 Contact

Author: Vi Son  
Email: son.via6@gmail.com

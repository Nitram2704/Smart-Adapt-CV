# 🚀 Smart-Adapt CV

> **AI-Powered Resume Optimization Engine**
> *Adapt your CV to any job vacancy in seconds using local LLMs.*

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/backend-FastAPI-009688.svg)
![React](https://img.shields.io/badge/frontend-Next.js-black.svg)
![AI](https://img.shields.io/badge/AI-Gemini%20%2B%20Ollama-purple.svg)

**Smart-Adapt CV** is an intelligent tool conceived to revolutionize the job application process. Instead of sending the same generic CV to every company, this engine uses advanced AI agents to analyze your profile against specific job descriptions, rewriting and tailoring your experience to maximize your "Match Score".

---

## ✨ Key Features

*   **🧠 AI Gap Analysis**: Instantly compares your "Master Profile" vs. the Job Description to find missing skills and keywords.
*   **✍️ Dynamic Rewriting**: Automatically rewrites your Professional Summary and Experience bullet points to align with the vacancy's language and requirements.
*   **🌍 Multilingual Support**: Detects if the job is in English or Spanish and generates the CV in the matching language automatically.
*   **📂 Portfolio Integration**: Intelligently selects the top 3 most relevant projects from your portfolio to showcase as experience.
*   **📄 PDF Generation**: Produces a clean, ATS-friendly, and professionally designed PDF (A4 format) ready for submission.
*   **🔒 Local Privacy First**: Supports local LLMs via Ollama (Llama 3, Mistral) for privacy-conscious users, with Gemini Pro as a cloud fallback.

---

## 🛠️ Tech Stack

### Backend (Python/FastAPI)
*   **Framework**: FastAPI
*   **AI Orchestration**: Google Gemini API + Ollama (Local LLM)
*   **PDF Engine**: WeasyPrint + Jinja2 Templates
*   **Parsing**: PyMuPDF (fitz) for extracting text from uploaded PDFs

### Frontend (Next.js/React)
*   **Framework**: Next.js 14 (App Router)
*   **Styling**: Tailwind CSS + Framer Motion
*   **Data Fetching**: Axios

---

## 🚀 Getting Started

### Prerequisites
*   Python 3.10+
*   Node.js 18+
*   [Ollama](https://ollama.com/) (Optional, for local AI)
*   Google Gemini API Key

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/Nitram2704/Smart-Adapt-CV.git
    cd Smart-Adapt-CV
    ```

2.  **Backend Setup**
    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```
    *Create a `.env` file in `/backend`:*
    ```env
    # ⚠️ IMPORTANT: Get your own API Key from https://aistudio.google.com/
    GOOGLE_API_KEY=your_google_api_key_here
    
    OLLAMA_MODEL=llama3.2
    PORT=8000
    ```

3.  **Frontend Setup**
    ```bash
    cd frontend
    npm install
    ```

4.  **Run the App**
    *Terminal 1 (Backend):*
    ```bash
    uvicorn main:app --reload
    ```
    *Terminal 2 (Frontend):*
    ```bash
    npm run dev
    ```

---

## 📸 Screenshots

*(Add screenshots of your dashboard here)*

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

# miniAI

miniAI is an AI-powered application built using the Groq API to perform multiple intelligent workflows within a single platform. The project is designed for fast and scalable AI interactions including conversational chat, bulk text classification, information extraction, content generation, and Retrieval-Augmented Generation (RAG).

---

## Overview

miniAI combines multiple AI utilities into one streamlined application with optimized inference speed powered by Groq. The system is designed for real-time AI interactions and scalable deployment.

---

## Features

* AI-powered conversational chat
* Bulk text classification
* Information extraction from documents and text
* AI-based content generation
* Retrieval-Augmented Generation (RAG)
* Fast inference using Groq API
* Modular and scalable architecture
* Real-time response handling

---

## Tech Stack

| Category         | Technology          |
| ---------------- | ------------------- |
| Language         | Python              |
| AI Inference     | Groq API            |
| Frontend         | Streamlit           |
| LLM Framework    | Transformers        |
| Retrieval System | Vector Database     |
| Deployment       | Hugging Face Spaces |

---

## Project Workflow

1. User submits input through the application interface
2. Input is processed using Groq-powered language models
3. Selected AI workflow is executed:

   * Chat
   * Classification
   * Information Extraction
   * Content Generation
   * RAG
4. Results are generated and displayed in real time

---

## Use Cases

* AI assistant applications
* Intelligent document understanding
* Automated text processing
* Semantic search systems
* Knowledge retrieval applications
* Productivity automation tools
* Business workflow automation

---

## Future Improvements

* Multi-file document support
* Voice interaction capabilities
* Persistent memory integration
* Agentic AI workflows
* Advanced RAG pipelines
* Real-time deployment optimization
* Multi-model support

---

## Installation

Clone the repository:

```bash
git clone <your-repository-link>
cd miniAI
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Run with Streamlit:

```bash
streamlit run app.py
```

---

## Environment Variables

Create a `.env` file in the root directory and add:

```env
GROQ_API_KEY=your_api_key_here
```

---

## Deployment

The application can be deployed on:

* Hugging Face Spaces
* Streamlit Cloud
* Docker
* VPS / Cloud Platforms

---

## Project Structure

```bash
miniAI/
│
├── app.py
├── utils.py
├── requirements.txt
├── README.md
└── .env
```

---

## Author

Sai Vignesh

miniAI

miniAI is an AI-powered application built using the Groq API to perform multiple intelligent tasks in a single platform. The project is designed to provide fast and efficient AI workflows such as chatting, bulk text classification, information extraction, content generation, and Retrieval-Augmented Generation (RAG).

Features
AI Chat system for interactive conversations
Bulk Classification for processing multiple inputs at once
Information Extraction from text content
AI Content Generation
RAG (Retrieval-Augmented Generation) support for contextual responses
Fast inference powered by Groq API
Simple and scalable architecture



Tech Stack
Python
Groq API
Streamlit / Flask (based on your implementation)
Vector Database (for RAG support)
Transformers / LLM models
Project Workflow
User provides input through the application
Input is processed using Groq-powered AI models
Features such as classification, extraction, generation, or RAG are executed
Results are displayed in real time with optimized response speed


Use Cases
AI assistant applications
Document understanding
Automated text processing
Smart search and retrieval systems
Productivity and business automation tools


Future Improvements
Multi-file support
Voice-based interaction
Advanced memory handling
Agentic AI workflows
Real-time deployment optimization


Installation
git clone <your-repository-link>
cd miniAI
pip install -r requirements.txt

Run the project:

streamlit run app.py

or

python app.py
API Setup

Create a .env file and add your Groq API key:

GROQ_API_KEY=your_api_key_here
Author

Sai Vignesh
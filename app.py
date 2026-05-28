import streamlit as st
import os
import json
import time
import pandas as pd
from dotenv import load_dotenv
from groq import Groq
from utils import ask

load_dotenv()
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# ── Page Config ───────────────────────────────────────────────────
st.set_page_config(
    page_title = "Mini AI",
    page_icon  = "",
    layout     = "wide"
)

st.title("Mini AI")

# ── Tabs ──────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Chat",
    "Bulk Classify",
    "Extract Data",
    "Generate Content",
    "RAG Q&A"
])


# TAB 1: SIMPLE CHAT
# ════════════════════════════════════════════════════════
with tab1:
    st.subheader("Chat with LLM")

    # System prompt
    system_prompt = st.text_area(
        "System Prompt (Role define):",
        value  = "You are a helpful assistant. Answer clearly and concisely.",
        height = 80
    )

    # Prompt type selector
    prompt_type = st.selectbox(
        "Prompt Type:",
        ["Zero-shot", "Few-shot", "Chain of Thought",
         "Role Prompting", "Constrained"]
    )

    # Few-shot examples
    if prompt_type == "Few-shot":
        st.info("Examples:")
        ex1 = st.text_input("Example 1 input:", "Great product!")
        ex1_out = st.text_input("Example 1 output:", "Positive")
        ex2 = st.text_input("Example 2 input:", "Worst ever")
        ex2_out = st.text_input("Example 2 output:", "Negative")

    user_input = st.text_area("Your Question:", height=100)

    if st.button("Ask", key="chat_btn"):
        if user_input:
            # Build prompt based on type
            if prompt_type == "Zero-shot":
                final_prompt = user_input

            elif prompt_type == "Few-shot":
                final_prompt = f"""{ex1} → {ex1_out}
{ex2} → {ex2_out}
{user_input} →"""

            elif prompt_type == "Chain of Thought":
                final_prompt = f"{user_input}\nThink step by step:"

            elif prompt_type == "Role Prompting":
                final_prompt = user_input

            elif prompt_type == "Constrained":
                final_prompt = f"""{user_input}
Rules:
- Keep under 50 words
- No technical jargon
- Simple language only"""

            with st.spinner("Thinking..."):
                result = ask(
                    final_prompt,
                    system = system_prompt
                )

            st.success("Answer:")
            st.write(result)

            # Show prompt used
            with st.expander("Prompt used"):
                st.code(final_prompt)
        else:
            st.warning("Question type!")


# ════════════════════════════════════════════════════════
# TAB 2: BULK CLASSIFY
# ════════════════════════════════════════════════════════
with tab2:
    st.subheader("Bulk Review Classification")
    st.write("Multiple reviews")

    # Input
    reviews_input = st.text_area(
        "Reviews paste (Separate line = one review):",
        height      = 200,
        placeholder = "Great product!\nTerrible quality\nGood value for money"
    )

    categories = st.text_input(
        "Categories (comma separated):",
        value = "Positive, Negative, Neutral"
    )

    if st.button("Classify All", key="classify_btn"):
        if reviews_input:
            reviews  = [r.strip() for r in reviews_input.split("\n") if r.strip()]
            cats     = categories.split(",")
            results  = []
            progress = st.progress(0)
            status   = st.empty()

            for i, review in enumerate(reviews):
                status.text(f"Processing {i+1}/{len(reviews)}...")

                prompt = f"""Classify into one of: {categories}
Review: {review}
Classification (one word only):"""

                sentiment = ask(prompt, max_tokens=10, temperature=0.1)
                results.append({
                    "Review"    : review,
                    "Category"  : sentiment.strip()
                })

                progress.progress((i+1)/len(reviews))
                time.sleep(0.3)

            status.text("Done!")

            # Show results
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True)

            # Download button
            csv = df.to_csv(index=False)
            st.download_button(
                label     = "Download CSV",
                data      = csv,
                file_name = "classified_results.csv",
                mime      = "text/csv"
            )
        else:
            st.warning("Reviews paste!")


# ════════════════════════════════════════════════════════
# TAB 3: EXTRACT DATA
# ════════════════════════════════════════════════════════
with tab3:
    st.subheader(" Extract Structured Data from Text")
    st.write("Raw text → JSON structured data")

    raw_text = st.text_area(
        "Raw text paste:",
        height      = 150,
        placeholder = "John paid Rs.5000 on 15th March 2024 for laptop repair at Chennai store"
    )

    extract_fields = st.multiselect(
        "Extract fields?",
        ["names", "dates", "amounts", "locations",
         "emails", "phone_numbers", "products"],
        default = ["names", "dates", "amounts", "locations"]
    )

    if st.button("Extract", key="extract_btn"):
        if raw_text and extract_fields:
            json_template = {field: [] for field in extract_fields}

            prompt = f"""Extract information from text.
Return ONLY valid JSON, nothing else.
No explanation needed.

Text: {raw_text}

JSON format to fill:
{json.dumps(json_template, indent=2)}"""

            with st.spinner("Extracting..."):
                result = ask(prompt, temperature=0.1, max_tokens=300)

            try:
                # Clean result
                result  = result.strip()
                if result.startswith("```"):
                    result = result.split("```")[1]
                    if result.startswith("json"):
                        result = result[4:]

                data    = json.loads(result)
                st.success("Extracted!")
                st.json(data)

                # Table format
                st.subheader("Table View:")
                for field, values in data.items():
                    if values:
                        st.write(f"**{field.upper()}:** {', '.join(str(v) for v in values)}")

            except Exception as e:
                st.warning("JSON parse issue — Raw output:")
                st.write(result)
        else:
            st.warning("Text + fields select!")


# ════════════════════════════════════════════════════════
# TAB 4: GENERATE CONTENT
# ════════════════════════════════════════════════════════
with tab4:
    st.subheader(" Content Generator")

    content_type = st.selectbox(
        "What generate?",
        ["Product Description", "Customer Reply",
         "Email", "Social Media Post", "Summary"]
    )

    col1, col2 = st.columns(2)

    with col1:
        topic = st.text_area("Topic / Input:", height=120)

    with col2:
        tone       = st.selectbox("Tone:", ["Professional", "Friendly", "Formal", "Casual"])
        word_limit = st.slider("Word limit:", 20, 200, 80)
        language   = st.selectbox("Language:", ["English", "Tamil", "Hindi"])

    if st.button("Generate", key="gen_btn"):
        if topic:
            prompt = f"""Generate {content_type} for: {topic}

Rules:
- Tone: {tone}
- Maximum {word_limit} words
- Language: {language}
- No filler words
- Direct and clear

{content_type}:"""

            with st.spinner("Generating..."):
                result = ask(prompt, max_tokens=300)

            st.success("Generated Content:")
            st.write(result)
            st.text_area("Copy from here:", result, height=150)
        else:
            st.warning("Topic type!")


# TAB 5: RAG Q&A — sentence-transformers இல்லாம!
with tab5:
    st.subheader("RAG — Document Q&A")
    st.write("Document paste → Questions ask!")

    doc_text = st.text_area(
        "உன் Document paste:",
        height      = 200,
        placeholder = "Any article, policy, notes..."
    )

    if doc_text:
        st.success(" Document ready!")

        if "rag_history" not in st.session_state:
            st.session_state.rag_history = []

        # Show history
        for msg in st.session_state.rag_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        question = st.chat_input("Document ask...")

        if question:
            with st.chat_message("user"):
                st.write(question)

            # Simple RAG — full doc as context
            # (sentence-transformers இல்லாம!)
            prompt = f"""Answer using ONLY this document.
If answer not in document: say 'Information not available'
Keep answer under 3 sentences.

Document:
{doc_text[:3000]}

Question: {question}
Answer:"""

            with st.chat_message("assistant"):
                with st.spinner("Searching..."):
                    answer = ask(
                        prompt,
                        system      = "Answer only from given document.",
                        temperature = 0.1
                    )
                st.write(answer)

            st.session_state.rag_history.append(
                {"role": "user",      "content": question}
            )
            st.session_state.rag_history.append(
                {"role": "assistant", "content": answer}
            )

        if st.button("Clear Chat"):
            st.session_state.rag_history = []
            st.rerun()
    else:
        st.info(" Document paste first!")

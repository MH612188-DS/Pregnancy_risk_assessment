import streamlit as st
import os
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from langchain_google_genai import ChatGoogleGenerativeAI

st.set_page_config(page_title="Pregnancy Risk Checker", layout="centered")
st.title("🩺 Pregnancy Risk Triage Assistant")
st.markdown("Answer the following questions to assess symptom risk using WHO-based guidelines.")

@st.cache_resource
def initialize_engine():
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
    Settings.llm = llm
    Settings.embed_model = HuggingFaceEmbedding("sentence-transformers/all-MiniLM-L6-v2")
    docs = SimpleDirectoryReader("data").load_data()
    idx = VectorStoreIndex.from_documents(docs)
    return idx.as_query_engine()

query_engine = initialize_engine()

def generate_prompt(question, answer):
    return f"""
Symptom Categorization Task:

You are a pregnancy risk triage assistant using WHO guidelines and advanced obstetric clinical logic.

Input:
Question: {question}
Answer: {answer}

Evaluate the response using the following WHO-based medical framework:

1. Risk Factors & Triggers:
- Preeclampsia: first pregnancy, age <18 or >35, obesity (BMI>30), chronic hypertension, diabetes/kidney disease
- Gestational Diabetes: BMI>25, family history, macrosomia
- Preterm Labor: contractions, pressure, fluid/rupture before 37 weeks
- Placenta Previa: painless bright red bleeding
- Ectopic Pregnancy: sharp one-sided pain, shoulder tip pain, fainting
- Chorioamnionitis: fever + discharge + tenderness

2. Red Flag Combinations:
- Headache + vision + swelling → Preeclampsia (High Risk)
- Bleeding + sharp pain + low BP → Ectopic Pregnancy (High Risk)
- Fever + discharge + tenderness → Chorioamnionitis (High Risk)
- No fetal movement after 28 weeks → Fetal demise (High Risk)
- Contractions + cervical change <37 weeks → Preterm labor

3. Symptom Timeline Reference:
- 1st Trimester: risk of miscarriage or ectopic pregnancy
- 2nd Trimester: gestational diabetes, cervical insufficiency
- 3rd Trimester: preeclampsia, preterm labor, stillbirth

Output Format:
- Risk Level: Low / Medium / High
- Condition(s) Suspected:
- Reasoning:
- Suggested Action:
"""

symptom_prompts = [
    "Are you currently experiencing any vaginal bleeding or unusual discharge?",
    "Have you had any sharp, one-sided lower abdominal pain or shoulder tip pain recently?",
    "How would you describe your baby’s movements today compared to yesterday?",
    "Have you experienced severe or persistent headaches, blurry vision, or noticeable swelling in your face, hands, or feet?",
    "Do you currently have a fever (above 38.5°C), or have you noticed any foul-smelling discharge or abdominal tenderness?",
    "Are you feeling regular contractions, lower back pressure, pelvic pressure, or any leaking of fluid before 37 weeks of pregnancy?",
    "Have you been unusually thirsty, tired, or had blurred vision recently? Do you have a family history of diabetes?",
    "Have you experienced dizziness, fainting, or unusual shoulder pain along with abdominal discomfort?",
    "Have you had any episodes of painless, bright red bleeding during pregnancy?",
    "Is this your first pregnancy? What is your age and pre-pregnancy BMI? Do you have a history of hypertension, diabetes, or kidney disease?",
    "What is your current gestational age in weeks?"
]

with st.form("symptom_form"):
    responses = []
    for i, prompt in enumerate(symptom_prompts):
        answer = st.text_area(f"Q{i+1}: {prompt}", key=f"q{i}")
        responses.append((prompt, answer))
    submitted = st.form_submit_button("🔬 Analyze Responses")

if submitted:
    st.markdown("---")
    st.subheader(" Risk Analysis Summary")
    for i, (question, answer) in enumerate(responses, 1):
        if not answer.strip():
            continue
        with st.spinner(f"Analyzing Q{i}..."):
            prompt = generate_prompt(question, answer)
            result = query_engine.query(prompt)
        st.markdown(f"** Q{i}: {question}**")
        st.markdown(f" *{answer}*")
        st.markdown(f" **Assessment**:```{str(result)}```")
        st.markdown("---")

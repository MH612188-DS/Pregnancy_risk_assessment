# Pregnancy Risk Assessment Chatbot (LLM + RAG)

This project is an LLM-powered chatbot that assesses pregnancy-related risks using **retrieval-augmented generation (RAG)** via **LlamaIndex** and a **Streamlit frontend**. It uses symptom-based inputs to categorize risks (e.g., preeclampsia, GDM, ectopic pregnancy) and recommends actions according to WHO guidelines.

---

## 🩺 Problem Description

Pregnant individuals often face challenges understanding whether their symptoms indicate a medical emergency or a manageable condition. This chatbot aims to:

- Allow users to enter **free-text symptom queries**
- Retrieve **trusted medical information** from WHO/local documents and given RAG knowledge base
- Analyze symptoms with **advanced rule-based + LLM logic**
- Provide **risk labels** (e.g., Low, Moderate, High Risk) and **suggest next steps**

It supports early screening for:
- Preeclampsia
- Gestational Diabetes (GDM)
- Ectopic Pregnancy
- Anemia
- Preterm labor, etc.

---

## 🧠 System Architecture

```plaintext
                     +--------------------------+
                     |    WHO PDF Guidelines    |
                     +------------+-------------+
                                  |
                             [LlamaIndex]
                                  |
          +-----------------------v--------------------+
          |             Vector Index + RAG             |
          +-----------------------+--------------------+
                                  |
                     +------------v-------------+
                     |       Query Engine       |
                     | (using Gemini/OpenAI LLM)|
                     +------------+-------------+
                                  |
                         [Risk Categorization]
                                  |
                         +--------v--------+
                         |   Streamlit UI   |
                         +------------------+
```
---
## Components:

📄 PDF ingestion (WHO Guidelines)

🔍 LlamaIndex vector search

🤖 LLM for response generation (via LangChain/Gemini/OpenAI)

🧠 Risk categorization logic (rule-based + GPT)

🌐 Streamlit Cloud frontend
---
## 💬 Example Queries & Outputs
✅ Query 1:
``` "I'm feeling severe headache, blurred vision, and swelling in hands and feet." ```

Output:
```
🤖 Assessment:
🟠 Risk Category: High Risk (Possible Preeclampsia)
📚 Supporting Info: Retrieved from WHO Maternal Health Guidelines
✅ Suggested Action: Seek immediate medical attention. Contact your healthcare provider or visit the nearest emergency unit.
✅ Query 2:
"I have mild back pain and occasional spotting at 10 weeks."
```

```
Output:
🤖 Assessment:
🟡 Risk Category: Moderate Risk (Monitor Closely)
📚 Supporting Info: WHO suggests back pain and spotting may be normal, but persistent symptoms require evaluation.
✅ Suggested Action: Monitor symptoms. If spotting continues or intensifies, consult your doctor.
```


---
## 🚀 Deployment Steps (Streamlit Cloud)
1. 🔧 Clone the Repository

```
git clone https://github.com/YOUR_USERNAME/pregnancy-risk-assessment.git
cd pregnancy-risk-assessment
```

2. 📄 Add Secrets
Create a file .streamlit/secrets.toml and insert your API key:

``` GOOGLE_API_KEY = "your_google_gemini_api_key_here" ```
Use OpenAI API if needed, e.g., OPENAI_API_KEY = "your-key"

3. 📦 Add requirements.txt
Ensure this file contains all required packages:
```
streamlit
openai
llama-index
langchain
langchain-community
sentence-transformers
```

5. 🌍 Deploy to Streamlit Cloud
Push to GitHub

Go to Streamlit Cloud

Click "New app"

Connect your GitHub repo

Set app.py as the main file

Hit Deploy

---

## 📁 Project Structure

```
pregnancy-risk-assessment/
├── app.py
├── requirements.txt
├── .streamlit/
│   └── secrets.toml
├── documents/
│   └── WHO_guidelines.pdf
└── README.md
```

---
## 🤝 Contributing
Pull requests and issues are welcome! Please ensure you're citing medical sources responsibly.

---
## ⚠️ Disclaimer
This chatbot is for informational purposes only and not a replacement for professional medical advice. Always consult your healthcare provider.

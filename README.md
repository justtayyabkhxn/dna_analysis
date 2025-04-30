# 🧬 DNA Sequence Analysis API

This FastAPI project helps an **Advanced Forensic Research Team** analyze ancient DNA samples to uncover historical genetic links. The app allows researchers to upload sample data, generate DNA sequences from seeds, compare genetic similarity between samples, and ask natural language questions about the API.

---

## 🚀 Features

- 📁 **Upload CSV** of ancient remains data.
- 🧬 **Generate DNA Sequences** using sample metadata.
- 📊 **Compare DNA Sequences** and get similarity scores.
- 🤖 **Ask Me Anything** endpoint powered by OpenAI/Gemini.

---

## 📦 Tech Stack

- FastAPI (Python)
- Uvicorn (ASGI server)
- Pydantic
- OpenAI API (or Gemini)

---

## 📂 Project Structure

dna_analysis/ │ ├── app/ │ ├── main.py # FastAPI server with all endpoints │ ├── utils.py # DNA sequence comparison and OpenAI logic │ ├── data_store.py # Stores uploaded sample data in memory │ └── dna_function.py # Provided DNA sequence generator │ ├── app/test_main.py # Unit tests using pytest ├── requirements.txt └── README.md



---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/dna-sequence-api.git
cd dna-sequence-api

pip install -r requirements.txt

export OPENAI_API_KEY=your_key_here       # For Linux/macOS
set OPENAI_API_KEY=your_key_here          # For Windows

uvicorn app.main:app --reload


curl -X POST -F "file=@samples.csv" http://localhost:8000/upload-csv/

GET /generate-sequence/?sample_id=id_0001

GET /compare-sequences/?sample_id1=id_0001&sample_id2=id_0002

{
  "question": "What does this API do?"
}

pytest app/test_main.py

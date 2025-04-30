import os
import openai

# ---- DNA Sequence Comparison ----
def compare_sequences(seq1: str, seq2: str) -> float:
    """
    Compares two DNA sequences using a motif matching strategy.
    Returns a similarity score between 0.0 and 1.0.
    """
    if not seq1 or not seq2:
        return 0.0

    min_len = min(len(seq1), len(seq2))
    match_count = 0

    for i in range(min_len):
        if seq1[i] == seq2[i]:
            match_count += 1

    similarity = match_count / min_len
    return round(similarity, 4)


# ---- Ask Me Anything using OpenAI ----
def ask_openai_response(prompt: str) -> str:
    """
    Sends a natural language query to the OpenAI API and returns a response.
    You need to set your OpenAI API key in the environment variable: OPENAI_API_KEY
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."

    openai.api_key = api_key

    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo",   # or "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are an assistant helping forensic DNA researchers."},
                {"role": "user", "content": prompt},
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Failed to get response from OpenAI: {e}"

from transformers import pipeline

# Load once
generator = pipeline(
    "text-generation",
    model="distilgpt2"
)

def generate_answer(question, docs):
    context = "\n\n".join([doc.page_content for doc in docs])[:1500]

    prompt = f"""
Answer based on the context below.

Context:
{context}

Question: {question}

Answer:
"""

    result = generator(
        prompt,
        max_length=200,
        do_sample=False
    )

    return result[0]["generated_text"]
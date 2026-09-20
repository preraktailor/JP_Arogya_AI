import os
import pickle

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss


# -----------------------------------
# Load Embedding Model (Lazy Loading)
# -----------------------------------

model = None


def get_model():
    global model

    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")

    return model


# -----------------------------------
# Read all PDFs
# -----------------------------------

def load_pdfs(folder="pdfs"):

    text = ""

    if not os.path.exists(folder):
        return text

    for file in os.listdir(folder):

        if file.endswith(".pdf"):

            reader = PdfReader(os.path.join(folder, file))

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    return text


# -----------------------------------
# Split Text
# -----------------------------------

def split_text(text, chunk_size=500):

    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks


# -----------------------------------
# Build Vector Database
# -----------------------------------

def build_vector_database():

    text = load_pdfs()

    chunks = split_text(text)

    if len(chunks) == 0:
        return

    model = get_model()

    embeddings = model.encode(chunks)

    index = faiss.IndexFlatL2(embeddings.shape[1])

    index.add(embeddings)

    os.makedirs("vectorstore", exist_ok=True)

    faiss.write_index(
        index,
        "vectorstore/medical.index"
    )

    with open("vectorstore/chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

    print("✅ Medical Vector Database Created")


# -----------------------------------
# Search Documents
# -----------------------------------

def search_documents(question):

    if not os.path.exists("vectorstore/medical.index"):
        return ""

    model = get_model()

    index = faiss.read_index("vectorstore/medical.index")

    with open("vectorstore/chunks.pkl", "rb") as f:
        chunks = pickle.load(f)

    question_embedding = model.encode([question])

    distance, indices = index.search(question_embedding, 3)

    context = ""

    for idx in indices[0]:

        if idx < len(chunks):
            context += chunks[idx] + "\n"

    return context
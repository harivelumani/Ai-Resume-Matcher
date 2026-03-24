from fastapi import FastAPI, UploadFile, File, Form
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from pdfminer.high_level import extract_text
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

model = SentenceTransformer("all-MiniLM-L6-v2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow Angular
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/match")
async def match(resume: UploadFile = File(...), jd: str = Form(...)):

    # Save resume temporarily
    with open("temp_resume.pdf", "wb") as f:
        f.write(await resume.read())

    # Extract resume text
    resume_text = extract_text("temp_resume.pdf")

    # Create embeddings
    resume_embedding = model.encode([resume_text])
    jd_embedding = model.encode([jd])

    # Cosine similarity
    score = cosine_similarity(resume_embedding, jd_embedding)[0][0]

    return {
        "matchScore": round(score * 100, 2)
    }
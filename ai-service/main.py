from fastapi import FastAPI, UploadFile, File, Form
from pdfminer.high_level import extract_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import uuid
import os

app = FastAPI()


@app.post("/match")
async def match(resume: UploadFile = File(...), jd: str = Form(...)):

    # unique filename to avoid overwriting
    filename = f"{uuid.uuid4()}.pdf"

    with open(filename, "wb") as f:
        f.write(await resume.read())

    resume_text = extract_text(filename)

    # remove temp file
    os.remove(filename)

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([resume_text, jd])

    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

    return {"matchScore": round(score * 100, 2)}

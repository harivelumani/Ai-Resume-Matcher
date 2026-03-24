from fastapi import FastAPI, UploadFile, File, Form
from pdfminer.high_level import extract_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

@app.post("/match")
async def match(resume: UploadFile = File(...), jd: str = Form(...)):

    with open("resume.pdf", "wb") as f:
        f.write(await resume.read())

    resume_text = extract_text("resume.pdf")

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([resume_text, jd])

    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

   return {"matchScore": round(score * 100, 2)}

from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()


class MatchRequest(BaseModel):
    resume: str
    jd: str


@app.post("/match")
async def match(data: MatchRequest):

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([data.resume, data.jd])

    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

    return {"matchScore": round(score * 100, 2)}

from fastapi import FastAPI, Request, HTTPException, UploadFile
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from pdfminer.high_level import extract_text
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid

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
async def match(request: Request):
    """
    Accepts either:
    - multipart/form-data: fields `resume` (file) and `jd` (string)
    - application/json: keys `resume` (already-extracted text) and `jd` (string)
    """
    content_type = request.headers.get("content-type", "")

    resume_text = None
    jd = None

    if content_type.startswith("application/json"):
        payload = await request.json()
        resume_text = payload.get("resume")
        jd = payload.get("jd")

        if not isinstance(resume_text, str) or not isinstance(jd, str):
            raise HTTPException(
                status_code=422,
                detail="Expected JSON body: { resume: <string>, jd: <string> }",
            )
    else:
        form = await request.form()
        jd = form.get("jd")

        if not isinstance(jd, str) or not jd:
            raise HTTPException(
                status_code=422,
                detail="Missing/invalid form field 'jd' (string).",
            )

        # Support both: file upload in `resume`, or pre-extracted text in `resume_text`
        resume_text = form.get("resume_text") or form.get("resumeText")
        resume_file = form.get("resume")

        if resume_file is not None:
            # `resume` is expected to be a file (UploadFile) in multipart requests.
            if not isinstance(resume_file, UploadFile):
                raise HTTPException(
                    status_code=422,
                    detail="Invalid form field 'resume' (expected an uploaded file).",
                )

            temp_path = f"temp_resume_{uuid.uuid4().hex}.pdf"
            with open(temp_path, "wb") as f:
                f.write(await resume_file.read())

            try:
                resume_text = extract_text(temp_path)
            finally:
                try:
                    os.remove(temp_path)
                except OSError:
                    pass

        if not isinstance(resume_text, str) or not resume_text.strip():
            raise HTTPException(
                status_code=422,
                detail="Expected either form file field 'resume' or form field 'resume_text'.",
            )

    # Create embeddings
    resume_embedding = model.encode([resume_text])
    jd_embedding = model.encode([jd])

    # Cosine similarity
    score = cosine_similarity(resume_embedding, jd_embedding)[0][0]

    return {"matchScore": round(score * 100, 2)}
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from models import (
    AnalyzeRequest,
    EmailRequest,
    CoverLetterRequest,
    FollowUpEmailRequest,
    JobCreateRequest,
    AnalyzeSavedJobRequest,
    JobStatusUpdateRequest
)

from ai_service import (
    analyze_resume_match,
    generate_email,
    generate_cover_letter,
    generate_follow_up_email
)

from database import Base, engine, SessionLocal, Job

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Job Search Agent")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {
        "message": "AI Job Search Agent is running",
        "endpoints": [
            "/analyze",
            "/generate-email",
            "/generate-cover-letter",
            "/generate-follow-up-email",
            "/jobs"
        ]
    }


@app.post("/analyze")
def analyze_job(request: AnalyzeRequest):
    result = analyze_resume_match(
        resume_text=request.resume_text,
        job_description=request.job_description
    )
    return {"analysis": result}


@app.post("/generate-email")
def create_email(request: EmailRequest):
    result = generate_email(
        resume_text=request.resume_text,
        job_description=request.job_description,
        company_name=request.company_name,
        role_title=request.role_title
    )
    return {"email": result}


@app.post("/generate-cover-letter")
def create_cover_letter(request: CoverLetterRequest):
    result = generate_cover_letter(
        resume_text=request.resume_text,
        job_description=request.job_description,
        company_name=request.company_name,
        role_title=request.role_title
    )
    return {"cover_letter": result}


@app.post("/generate-follow-up-email")
def create_follow_up_email(request: FollowUpEmailRequest):
    result = generate_follow_up_email(
        company_name=request.company_name,
        role_title=request.role_title,
        days_since_applied=request.days_since_applied
    )
    return {"follow_up_email": result}


@app.post("/jobs")
def save_job(request: JobCreateRequest, db: Session = Depends(get_db)):
    new_job = Job(
        company_name=request.company_name,
        role_title=request.role_title,
        job_description=request.job_description,
        status=request.status
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return {
        "message": "Job saved successfully",
        "job": {
            "id": new_job.id,
            "company_name": new_job.company_name,
            "role_title": new_job.role_title,
            "status": new_job.status
        }
    }


@app.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()

    return {
        "jobs": [
            {
                "id": job.id,
                "company_name": job.company_name,
                "role_title": job.role_title,
                "job_description": job.job_description,
                "status": job.status
            }
            for job in jobs
        ]
    }


@app.post("/jobs/{job_id}/analyze")
def analyze_saved_job(
    job_id: int,
    request: AnalyzeSavedJobRequest,
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        return {"error": "Job not found"}

    result = analyze_resume_match(
        resume_text=request.resume_text,
        job_description=job.job_description
    )

    return {
        "job": {
            "id": job.id,
            "company_name": job.company_name,
            "role_title": job.role_title,
            "status": job.status
        },
        "analysis": result
    }


@app.put("/jobs/{job_id}/status")
def update_job_status(
    job_id: int,
    request: JobStatusUpdateRequest,
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        return {"error": "Job not found"}

    job.status = request.status
    db.commit()
    db.refresh(job)

    return {
        "message": "Job status updated successfully",
        "job": {
            "id": job.id,
            "company_name": job.company_name,
            "role_title": job.role_title,
            "status": job.status
        }
    }


@app.delete("/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        return {"error": "Job not found"}

    db.delete(job)
    db.commit()

    return {
        "message": "Job deleted successfully",
        "deleted_job_id": job_id
    }
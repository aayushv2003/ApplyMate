from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    resume_text: str
    job_description: str


class EmailRequest(BaseModel):
    resume_text: str
    job_description: str
    company_name: str
    role_title: str


class CoverLetterRequest(BaseModel):
    resume_text: str
    job_description: str
    company_name: str
    role_title: str


class FollowUpEmailRequest(BaseModel):
    company_name: str
    role_title: str
    days_since_applied: int = 7


class JobCreateRequest(BaseModel):
    company_name: str
    role_title: str
    job_description: str
    status: str = "saved"


class AnalyzeSavedJobRequest(BaseModel):
    resume_text: str


class JobStatusUpdateRequest(BaseModel):
    status: str
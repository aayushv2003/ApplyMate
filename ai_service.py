import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def call_openai(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a practical AI career assistant. "
                    "Give honest, structured, concise, and useful outputs. "
                    "Do not exaggerate the candidate's experience."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4
    )

    return response.choices[0].message.content


def analyze_resume_match(resume_text: str, job_description: str) -> str:
    prompt = f"""
Analyze this resume against the job description.

Return the response exactly in this format:

Match Score: X/100

Strong Matches:
1.
2.
3.

Missing or Weak Skills:
1.
2.
3.

Resume Improvement Suggestions:
1.
2.
3.

Interview Talking Points:
1.
2.
3.

Apply Recommendation:
Strong Apply / Apply / Maybe / Skip

Reason:
Explain in 3 to 5 sentences.

Resume:
{resume_text}

Job Description:
{job_description}
"""
    return call_openai(prompt)


def generate_email(
    resume_text: str,
    job_description: str,
    company_name: str,
    role_title: str
) -> str:
    prompt = f"""
Write a short professional job application email.

Company:
{company_name}

Role:
{role_title}

Resume:
{resume_text}

Job Description:
{job_description}

Requirements:
- Keep it under 180 words.
- Make it confident but not arrogant.
- Mention relevant technical skills.
- Do not use fake experience.
- End politely.
"""
    return call_openai(prompt)


def generate_cover_letter(
    resume_text: str,
    job_description: str,
    company_name: str,
    role_title: str
) -> str:
    prompt = f"""
Write a professional cover letter.

Company:
{company_name}

Role:
{role_title}

Resume:
{resume_text}

Job Description:
{job_description}

Requirements:
- 4 to 5 paragraphs.
- Specific to the company and role.
- Emphasize relevant skills.
- Do not exaggerate.
- Natural tone.
"""
    return call_openai(prompt)


def generate_follow_up_email(
    company_name: str,
    role_title: str,
    days_since_applied: int
) -> str:
    prompt = f"""
Write a polite follow-up email for a job application.

Company:
{company_name}

Role:
{role_title}

Days since applied:
{days_since_applied}

Requirements:
- Short and professional.
- Ask about application status.
- Reaffirm interest.
- Do not sound desperate.
"""
    return call_openai(prompt)
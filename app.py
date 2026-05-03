import streamlit as st
import requests
from pypdf import PdfReader

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Job Search Agent",
    layout="wide"
)

st.title("AI Job Search Agent")
st.write(
    "Analyze resume-job fit, generate tailored emails and cover letters, "
    "create follow-ups, and track job applications."
)


# ---------- PDF Extraction ----------
def get_resume_text(key_prefix):
    uploaded_resume = st.file_uploader(
        "Upload resume PDF",
        type=["pdf"],
        key=f"{key_prefix}_pdf"
    )

    if uploaded_resume is not None:
        reader = PdfReader(uploaded_resume)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        st.success("Resume uploaded and processed ✅")

        # Optional preview
        with st.expander("Preview extracted resume"):
            st.write(text[:1500])

        return text
    else:
        st.warning("Please upload your resume PDF")
        return ""


# ---------- Tabs ----------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Analyze Job",
    "Generate Email",
    "Cover Letter",
    "Follow-up Email",
    "Job Tracker"
])


# ---------- Analyze ----------
with tab1:
    st.header("Analyze Resume vs Job Description")

    resume_text = get_resume_text("analyze")

    job_description = st.text_area(
        "Paste job description",
        height=250,
        key="analyze_jd"
    )

    if st.button("Analyze Match"):
        if resume_text and job_description:
            with st.spinner("Analyzing..."):
                response = requests.post(
                    f"{API_URL}/analyze",
                    json={
                        "resume_text": resume_text,
                        "job_description": job_description
                    }
                )

            if response.status_code == 200:
                st.subheader("Analysis Result")
                st.write(response.json()["analysis"])
            else:
                st.error("Something went wrong.")
        else:
            st.warning("Please provide both resume and job description.")


# ---------- Email ----------
with tab2:
    st.header("Generate Application Email")

    email_resume = get_resume_text("email")

    email_jd = st.text_area(
        "Job description",
        height=220,
        key="email_jd"
    )

    company_name = st.text_input("Company name", key="email_company")
    role_title = st.text_input("Role title", key="email_role")

    if st.button("Generate Email"):
        if email_resume and email_jd and company_name and role_title:
            with st.spinner("Generating email..."):
                response = requests.post(
                    f"{API_URL}/generate-email",
                    json={
                        "resume_text": email_resume,
                        "job_description": email_jd,
                        "company_name": company_name,
                        "role_title": role_title
                    }
                )

            if response.status_code == 200:
                st.subheader("Generated Email")
                st.write(response.json()["email"])
            else:
                st.error("Something went wrong.")
        else:
            st.warning("Please fill all fields.")


# ---------- Cover Letter ----------
with tab3:
    st.header("Generate Cover Letter")

    cl_resume = get_resume_text("cover_letter")

    cl_jd = st.text_area(
        "Job description",
        height=220,
        key="cl_jd"
    )

    cl_company = st.text_input("Company name", key="cl_company")
    cl_role = st.text_input("Role title", key="cl_role")

    if st.button("Generate Cover Letter"):
        if cl_resume and cl_jd and cl_company and cl_role:
            with st.spinner("Generating cover letter..."):
                response = requests.post(
                    f"{API_URL}/generate-cover-letter",
                    json={
                        "resume_text": cl_resume,
                        "job_description": cl_jd,
                        "company_name": cl_company,
                        "role_title": cl_role
                    }
                )

            if response.status_code == 200:
                st.subheader("Generated Cover Letter")
                st.write(response.json()["cover_letter"])
            else:
                st.error("Something went wrong.")
        else:
            st.warning("Please fill all fields.")


# ---------- Follow-up ----------
with tab4:
    st.header("Generate Follow-up Email")

    follow_company = st.text_input("Company name", key="follow_company")
    follow_role = st.text_input("Role title", key="follow_role")

    days_since_applied = st.number_input(
        "Days since applied",
        min_value=1,
        max_value=60,
        value=7
    )

    if st.button("Generate Follow-up Email"):
        if follow_company and follow_role:
            with st.spinner("Generating follow-up email..."):
                response = requests.post(
                    f"{API_URL}/generate-follow-up-email",
                    json={
                        "company_name": follow_company,
                        "role_title": follow_role,
                        "days_since_applied": days_since_applied
                    }
                )

            if response.status_code == 200:
                st.subheader("Generated Follow-up Email")
                st.write(response.json()["follow_up_email"])
            else:
                st.error("Something went wrong.")
        else:
            st.warning("Please fill company and role.")


# ---------- Job Tracker ----------
with tab5:
    st.header("Job Tracker")

    st.subheader("Save New Job")

    jt_company = st.text_input("Company name", key="jt_company")
    jt_role = st.text_input("Role title", key="jt_role")

    jt_description = st.text_area(
        "Job description",
        height=180,
        key="jt_description"
    )

    jt_status = st.selectbox(
        "Status",
        ["saved", "applied", "interview", "rejected", "offer"],
        key="jt_status"
    )

    if st.button("Save Job"):
        if jt_company and jt_role and jt_description:
            response = requests.post(
                f"{API_URL}/jobs",
                json={
                    "company_name": jt_company,
                    "role_title": jt_role,
                    "job_description": jt_description,
                    "status": jt_status
                }
            )

            if response.status_code == 200:
                st.success("Job saved successfully.")
            else:
                st.error("Could not save job.")
        else:
            st.warning("Please fill company, role, and job description.")

    st.divider()
    st.subheader("Saved Jobs")

    if st.button("Refresh Jobs"):
        response = requests.get(f"{API_URL}/jobs")

        if response.status_code == 200:
            jobs = response.json()["jobs"]

            if not jobs:
                st.info("No jobs saved yet.")
            else:
                for job in jobs:
                    with st.expander(
                        f"{job['company_name']} | {job['role_title']} | {job['status']}"
                    ):
                        st.write(f"**Job ID:** {job['id']}")
                        st.write(f"**Company:** {job['company_name']}")
                        st.write(f"**Role:** {job['role_title']}")
                        st.write(f"**Status:** {job['status']}")
                        st.write("**Job Description:**")
                        st.write(job["job_description"])
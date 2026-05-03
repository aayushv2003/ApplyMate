import streamlit as st
import requests
from pypdf import PdfReader

API_URL = "https://applymate-zyff.onrender.com"

st.set_page_config(
    page_title="ApplyMate AI",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
<style>
.main-title {
    font-size: 56px;
    font-weight: 800;
    margin-bottom: 0px;
}
.subtitle {
    font-size: 20px;
    color: #b5b5b5;
    margin-bottom: 35px;
}
.card {
    padding: 22px;
    border-radius: 16px;
    background-color: #1e1e2f;
    border: 1px solid #33334d;
    margin-bottom: 20px;
}
.small-muted {
    color: #a3a3a3;
    font-size: 14px;
}
.result-box {
    padding: 24px;
    border-radius: 16px;
    background-color: #111827;
    border: 1px solid #374151;
    white-space: pre-wrap;
}
</style>
""", unsafe_allow_html=True)


st.markdown('<div class="main-title">🚀 ApplyMate AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Analyze job fit, generate tailored application materials, and track your job search in one place.</div>',
    unsafe_allow_html=True
)


def extract_pdf_text(uploaded_file):
    if uploaded_file is None:
        return ""

    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text.strip()


def get_resume_text(key_prefix):
    uploaded_resume = st.file_uploader(
        "Upload your resume PDF",
        type=["pdf"],
        key=f"{key_prefix}_pdf"
    )

    if uploaded_resume:
        text = extract_pdf_text(uploaded_resume)
        st.success("Resume uploaded and processed successfully.")

        with st.expander("Preview extracted resume"):
            st.write(text[:2000])

        return text

    st.info("Upload your resume PDF to continue.")
    return ""


def show_result(title, content):
    st.markdown(f"### {title}")
    st.markdown(
        f"""
        <div class="result-box">
        {content}
        </div>
        """,
        unsafe_allow_html=True
    )


tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Analyze Job",
    "📧 Generate Email",
    "📝 Cover Letter",
    "🔁 Follow-up Email",
    "📌 Job Tracker"
])


with tab1:
    st.markdown("## 📊 Resume vs Job Description")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 1. Resume")
        resume_text = get_resume_text("analyze")

    with col2:
        st.markdown("### 2. Job Description")
        job_description = st.text_area(
            "Paste the job description here",
            height=320,
            key="analyze_jd"
        )

    if st.button("🚀 Analyze Match", use_container_width=True):
        if resume_text and job_description:
            with st.spinner("Analyzing your resume against the job description..."):
                response = requests.post(
                    f"{API_URL}/analyze",
                    json={
                        "resume_text": resume_text,
                        "job_description": job_description
                    }
                )

            if response.status_code == 200:
                show_result("Analysis Result", response.json()["analysis"])
            else:
                st.error("Something went wrong while analyzing.")
        else:
            st.warning("Please upload a resume and paste a job description.")


with tab2:
    st.markdown("## 📧 Generate Application Email")

    col1, col2 = st.columns(2)

    with col1:
        email_resume = get_resume_text("email")
        company_name = st.text_input("Company name", key="email_company")

    with col2:
        role_title = st.text_input("Role title", key="email_role")
        email_jd = st.text_area("Job description", height=260, key="email_jd")

    if st.button("✨ Generate Email", use_container_width=True):
        if email_resume and email_jd and company_name and role_title:
            with st.spinner("Generating tailored email..."):
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
                show_result("Generated Email", response.json()["email"])
            else:
                st.error("Something went wrong.")
        else:
            st.warning("Please fill all fields.")


with tab3:
    st.markdown("## 📝 Generate Cover Letter")

    col1, col2 = st.columns(2)

    with col1:
        cl_resume = get_resume_text("cover_letter")
        cl_company = st.text_input("Company name", key="cl_company")

    with col2:
        cl_role = st.text_input("Role title", key="cl_role")
        cl_jd = st.text_area("Job description", height=260, key="cl_jd")

    if st.button("📝 Generate Cover Letter", use_container_width=True):
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
                show_result("Generated Cover Letter", response.json()["cover_letter"])
            else:
                st.error("Something went wrong.")
        else:
            st.warning("Please fill all fields.")


with tab4:
    st.markdown("## 🔁 Generate Follow-up Email")

    col1, col2, col3 = st.columns(3)

    with col1:
        follow_company = st.text_input("Company name", key="follow_company")

    with col2:
        follow_role = st.text_input("Role title", key="follow_role")

    with col3:
        days_since_applied = st.number_input(
            "Days since applied",
            min_value=1,
            max_value=60,
            value=7
        )

    if st.button("📨 Generate Follow-up", use_container_width=True):
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
                show_result("Generated Follow-up Email", response.json()["follow_up_email"])
            else:
                st.error("Something went wrong.")
        else:
            st.warning("Please fill company and role.")


with tab5:
    st.markdown("## 📌 Job Tracker")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Save New Job")

    col1, col2 = st.columns(2)

    with col1:
        jt_company = st.text_input("Company name", key="jt_company")

    with col2:
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

    if st.button("💾 Save Job", use_container_width=True):
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

    st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    st.markdown("### Saved Jobs")

    if st.button("🔄 Refresh Jobs", use_container_width=True):
        response = requests.get(f"{API_URL}/jobs")

        if response.status_code == 200:
            jobs = response.json()["jobs"]

            if not jobs:
                st.info("No jobs saved yet.")
            else:
                for job in jobs:
                    with st.expander(
                        f"🏢 {job['company_name']} | {job['role_title']} | {job['status']}"
                    ):
                        st.write(f"**Job ID:** {job['id']}")
                        st.write(f"**Company:** {job['company_name']}")
                        st.write(f"**Role:** {job['role_title']}")
                        st.write(f"**Status:** {job['status']}")
                        st.write("**Job Description:**")
                        st.write(job["job_description"])

                        new_status = st.selectbox(
                            "Update status",
                            ["saved", "applied", "interview", "rejected", "offer"],
                            key=f"status_{job['id']}"
                        )

                        col_update, col_delete = st.columns(2)

                        with col_update:
                            if st.button("Update Status", key=f"update_{job['id']}"):
                                update_response = requests.put(
                                    f"{API_URL}/jobs/{job['id']}/status",
                                    json={"status": new_status}
                                )

                                if update_response.status_code == 200:
                                    st.success("Status updated.")
                                else:
                                    st.error("Could not update status.")

                        with col_delete:
                            if st.button("Delete Job", key=f"delete_{job['id']}"):
                                delete_response = requests.delete(
                                    f"{API_URL}/jobs/{job['id']}"
                                )

                                if delete_response.status_code == 200:
                                    st.success("Job deleted. Refresh jobs.")
                                else:
                                    st.error("Could not delete job.")
        else:
            st.error("Could not fetch jobs.")
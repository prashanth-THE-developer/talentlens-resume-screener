
import html

import streamlit as st

from matcher.extract import extract_text
from matcher.skills import load_skills, extract_skills
from matcher.score import final_score


# --------------------------------------------------
# 1. PAGE SETTINGS
# --------------------------------------------------
st.set_page_config(
    page_title="TalentLens | Resume Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# 2. PROFESSIONAL DESIGN SYSTEM
# --------------------------------------------------
st.markdown(
    """
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap'
    );

    :root {
        --bg: #0b1020;
        --panel: #121a2c;
        --panel-soft: #172137;
        --border: #28354c;
        --text: #f1f5ff;
        --muted: #9aa9c3;
        --accent: #9b8cff;
        --green: #63e6be;
        --red: #ff9b9b;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(
                ellipse at 10% 0%,
                rgba(104, 83, 219, 0.16),
                transparent 38%
            ),
            var(--bg);
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1440px;
        padding: 2rem 3rem 3rem;
    }

    h1, h2, h3 {
        font-family: 'Manrope', sans-serif !important;
        color: var(--text) !important;
        letter-spacing: -0.5px;
    }

    p, label, li {
        color: #d0d9ea;
    }

    [data-testid="stSidebar"] {
        background: #0e1526;
        border-right: 1px solid var(--border);
    }

    .brand {
        font-family: 'Manrope', sans-serif;
        font-size: 1.55rem;
        font-weight: 800;
        color: white;
        letter-spacing: -0.8px;
    }

    .brand span {
        color: var(--accent);
    }

    .eyebrow {
        color: var(--accent);
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 0.73rem;
        font-weight: 700;
    }

    .hero-title {
        font-family: 'Manrope', sans-serif;
        font-size: clamp(2rem, 3.5vw, 3.25rem);
        font-weight: 800;
        line-height: 1.14;
        letter-spacing: -1.8px;
        margin: 12px 0;
        color: white;
    }

    .hero-title span {
        color: var(--accent);
    }

    .hero-copy {
        color: var(--muted);
        font-size: 1rem;
        line-height: 1.8;
        max-width: 760px;
    }

    .panel {
        background: linear-gradient(
            145deg,
            rgba(23, 33, 55, 0.96),
            rgba(17, 25, 43, 0.96)
        );
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 23px;
        height: 100%;
    }

    .panel-label {
        color: var(--muted);
        font-size: 0.82rem;
        font-weight: 600;
        margin-bottom: 9px;
    }

    .panel-title {
        color: white;
        font-family: 'Manrope', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 7px;
    }

    .panel-copy {
        color: var(--muted);
        font-size: 0.88rem;
        line-height: 1.6;
    }

    div[data-testid="stFileUploader"],
    div[data-testid="stTextArea"] {
        background: #111a2c;
        border: 1px solid #30405b;
        border-radius: 13px;
        padding: 12px;
    }

    div[data-testid="stFileUploader"] section {
        border-color: #6659ad;
    }

    div[data-testid="stTextArea"] textarea {
        background: #0c1425;
        color: white;
        border: 1px solid #35415a;
        border-radius: 10px;
        line-height: 1.65;
        font-size: 0.92rem;
    }

    div[data-testid="stTextArea"] textarea:focus {
        border-color: var(--accent);
        box-shadow: 0 0 0 1px var(--accent);
    }

    div.stButton > button {
        min-height: 52px;
        border: 1px solid #aa9cff;
        border-radius: 12px;
        background: linear-gradient(100deg, #7663ed, #9b78ff);
        color: white;
        font-size: 1rem;
        font-weight: 700;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        border-color: white;
        color: white;
        filter: brightness(1.1);
        transform: translateY(-1px);
    }

    div[data-testid="stMetric"] {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 15px;
        padding: 19px;
    }

    div[data-testid="stMetricLabel"] {
        color: var(--muted);
    }

    div[data-testid="stMetricValue"] {
        color: #c4b8ff;
        font-family: 'Manrope', sans-serif;
        font-weight: 800;
    }

    div[data-testid="stProgress"] > div {
        background: #28334b;
        border-radius: 10px;
    }

    div[data-testid="stProgress"] div[role="progressbar"] {
        background: linear-gradient(90deg, #7866ef, #b09aff);
    }

    .skill-chip {
        display: inline-block;
        background: #202b43;
        border: 1px solid #3a4b68;
        color: #dce5ff;
        border-radius: 8px;
        padding: 7px 11px;
        margin: 4px 5px 4px 0;
        font-size: 0.82rem;
        font-weight: 600;
    }

    .matched-chip {
        background: rgba(44, 173, 130, 0.12);
        border-color: rgba(99, 230, 190, 0.35);
        color: #8df0cb;
    }

    .missing-chip {
        background: rgba(220, 90, 105, 0.10);
        border-color: rgba(255, 155, 155, 0.3);
        color: #ffb2b2;
    }

    .section-kicker {
        color: var(--accent);
        font-size: 0.74rem;
        font-weight: 700;
        letter-spacing: 1.6px;
        text-transform: uppercase;
    }

    .footer {
        color: #7e8ca6;
        font-size: 0.82rem;
        text-align: center;
        padding-top: 22px;
        border-top: 1px solid var(--border);
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    @media (max-width: 900px) {
        [data-testid="stMainBlockContainer"] {
            padding: 1.25rem 1rem 2rem;
        }

        .hero-title {
            letter-spacing: -0.8px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# 3. SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.markdown(
        '<div class="brand">Talent<span>Lens</span></div>',
        unsafe_allow_html=True,
    )

    st.caption("RESUME INTELLIGENCE PLATFORM")
    st.divider()

    st.markdown("### Navigation")
    st.markdown("🎯 &nbsp; Resume Analysis")
    st.markdown("🧩 &nbsp; Skills Comparison")
    st.markdown("📊 &nbsp; Match Insights")

    st.divider()

    st.markdown("### How it works")
    st.markdown(
        """
        1. Upload your resume PDF.
        2. Paste the target job description.
        3. Run the analysis.
        4. Review matched and missing skills.
        """
    )

    st.divider()

    st.caption("Supported format: PDF")
    st.caption("Designed for job seekers")


# --------------------------------------------------
# 4. HERO SECTION
# --------------------------------------------------
st.markdown(
    """
    <div class="eyebrow">SMART CAREER TOOLS / 01</div>
    <div class="hero-title">
        Your next opportunity,<br>
        <span>better matched.</span>
    </div>
    <div class="hero-copy">
        Understand how your resume aligns with a job description.
        Explore relevant skills, discover gaps, and identify areas
        to improve before applying.
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")


# --------------------------------------------------
# 5. RESUME AND JOB DESCRIPTION INPUTS
# --------------------------------------------------
resume_col, jd_col = st.columns([0.9, 1.1], gap="large")

with resume_col:
    st.markdown(
        """
        <div class="panel">
            <div class="panel-label">STEP 01 / YOUR PROFILE</div>
            <div class="panel-title">📄 Upload your resume</div>
            <div class="panel-copy">
                Add a text-based PDF so the application can
                extract your resume content.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    pdf = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        help="Text-based PDFs work best. Scanned PDFs may require OCR.",
    )

    if pdf:
        st.success(f"Selected: {pdf.name}")

with jd_col:
    st.markdown(
        """
        <div class="panel">
            <div class="panel-label">STEP 02 / TARGET ROLE</div>
            <div class="panel-title">📝 Job description</div>
            <div class="panel-copy">
                Paste the responsibilities, required skills,
                and qualifications from the job posting.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    jd = st.text_area(
        "Paste the complete job description",
        height=210,
        placeholder=(
            "Example: We are looking for a Software Engineer "
            "with Python, SQL, REST API, Git and problem-solving skills..."
        ),
        max_chars=30000,
    )

st.write("")

analyze_col, hint_col = st.columns([1, 2], gap="medium")

with analyze_col:
    analyze = st.button(
        "✨  Analyze compatibility",
        use_container_width=True,
        type="primary",
    )

with hint_col:
    st.caption(
        "For a more useful comparison, paste the full job description "
        "rather than only the job title."
    )


# --------------------------------------------------
# 6. ANALYSIS ENGINE
# --------------------------------------------------
if analyze:
    if pdf is None:
        st.warning("Please upload your resume PDF first.")

    elif not jd.strip():
        st.warning("Please paste the job description first.")

    else:
        try:
            with st.spinner(
                "Reading your resume and comparing the requirements..."
            ):
                resume_text = extract_text(pdf)

                if not resume_text or not resume_text.strip():
                    st.error(
                        "No readable text was found. This PDF may be "
                        "scanned or image-based. Try a text-based PDF."
                    )
                    st.stop()

                skills_list = load_skills()

                if not skills_list:
                    st.error(
                        "The skills list is empty. Check "
                        "data/skills_list.txt."
                    )
                    st.stop()

                resume_skills = extract_skills(
                    resume_text, skills_list
                )
                jd_skills = extract_skills(
                    jd, skills_list
                )

                matched_skills = sorted(
                    resume_skills & jd_skills
                )
                missing_skills = sorted(
                    jd_skills - resume_skills
                )

                # Use the existing project's scoring function.
                score = final_score(
                    resume_text,
                    jd,
                    resume_skills,
                    jd_skills,
                )

                # Additional document statistics.
                resume_words = len(resume_text.split())
                jd_words = len(jd.split())
                resume_chars = len(resume_text)
                jd_chars = len(jd)

                # Skill coverage measures required skills found.
                skill_coverage = (
                    len(matched_skills) / len(jd_skills) * 100
                    if jd_skills
                    else 0.0
                )

                resume_lower = resume_text.lower()
                jd_lower = jd.lower()

                # Count each detected skill's occurrences.
                skill_frequency = {}
                for skill in matched_skills:
                    skill_frequency[skill] = resume_lower.count(
                        skill.lower()
                    )

            # ------------------------------------------
            # 7. RESULTS HEADER
            # ------------------------------------------
            st.divider()

            st.markdown(
                """
                <div class="section-kicker">ANALYSIS COMPLETE</div>
                <h2>Resume intelligence report</h2>
                <p style="color:#9aa9c3">
                    Review your compatibility, skill coverage,
                    and areas that may need attention.
                </p>
                """,
                unsafe_allow_html=True,
            )

            # ------------------------------------------
            # 8. KPI CARDS
            # ------------------------------------------
            k1, k2, k3, k4 = st.columns(4, gap="medium")

            with k1:
                st.metric(
                    "Match score",
                    f"{score:.1f}%",
                    help=(
                        "Combined estimate based on text similarity "
                        "and detected skill overlap."
                    ),
                )

            with k2:
                st.metric(
                    "Skills matched",
                    len(matched_skills),
                    help="Detected in both the resume and job description.",
                )

            with k3:
                st.metric(
                    "Skills to review",
                    len(missing_skills),
                    help=(
                        "Skills detected in the job description "
                        "but not detected in the resume."
                    ),
                )

            with k4:
                st.metric(
                    "Resume words",
                    f"{resume_words:,}",
                    help="Approximate number of extracted words.",
                )

            # ------------------------------------------
            # 9. SCORE AND COVERAGE
            # ------------------------------------------
            st.write("")
            score_col, coverage_col = st.columns(
                [1, 1], gap="large"
            )

            with score_col:
                st.markdown(
                    """
                    <div class="panel">
                        <div class="panel-label">OVERALL ALIGNMENT</div>
                        <div class="panel-title">
                            Resume match score
                        </div>
                        <div class="panel-copy">
                            A combined estimate of text similarity
                            and required-skill overlap.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.progress(
                    max(0.0, min(float(score) / 100.0, 1.0))
                )

                if score >= 75:
                    st.success(
                        "Strong estimated alignment. Review the "
                        "individual requirements before applying."
                    )
                elif score >= 50:
                    st.info(
                        "Moderate estimated alignment. Review the "
                        "missing skills and relevant experience."
                    )
                else:
                    st.warning(
                        "Limited estimated alignment. Compare the "
                        "job requirements with your actual experience."
                    )

            with coverage_col:
                st.markdown(
                    """
                    <div class="panel">
                        <div class="panel-label">REQUIRED SKILLS</div>
                        <div class="panel-title">Skill coverage</div>
                        <div class="panel-copy">
                            Percentage of detected job-description skills
                            also detected in your resume.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f"<h2>{skill_coverage:.1f}%</h2>",
                    unsafe_allow_html=True,
                )

                st.progress(
                    max(
                        0.0,
                        min(float(skill_coverage) / 100.0, 1.0),
                    )
                )

                st.caption(
                    f"{len(matched_skills)} of {len(jd_skills)} "
                    "detected required skills matched."
                )

            # ------------------------------------------
            # 10. MATCHED AND MISSING SKILLS
            # ------------------------------------------
            st.write("")
            st.markdown("## 🧩 Skills comparison")

            matched_col, missing_col = st.columns(
                2, gap="large"
            )

            with matched_col:
                st.markdown(
                    f"### ✅ Matched skills ({len(matched_skills)})"
                )

                if matched_skills:
                    chips = "".join(
                        '<span class="skill-chip matched-chip">'
                        + html.escape(skill)
                        + "</span>"
                        for skill in matched_skills
                    )
                    st.markdown(chips, unsafe_allow_html=True)
                else:
                    st.info(
                        "No matching skills were detected. "
                        "Check your skills list and resume text."
                    )

            with missing_col:
                st.markdown(
                    f"### 🔎 Skills to review ({len(missing_skills)})"
                )

                if missing_skills:
                    chips = "".join(
                        '<span class="skill-chip missing-chip">'
                        + html.escape(skill)
                        + "</span>"
                        for skill in missing_skills
                    )
                    st.markdown(chips, unsafe_allow_html=True)

                    st.caption(
                        "Only include these skills on your resume "
                        "if you genuinely have the relevant knowledge "
                        "or experience."
                    )
                else:
                    if jd_skills:
                        st.success(
                            "All skills detected in the job description "
                            "were also detected in your resume."
                        )
                    else:
                        st.info(
                            "No skills from the configured skills list "
                            "were detected in the job description."
                        )

            # ------------------------------------------
            # 11. DOCUMENT STATISTICS
            # ------------------------------------------
            st.divider()
            st.markdown("## 📑 Document insights")

            stat1, stat2, stat3, stat4 = st.columns(4)

            with stat1:
                st.metric("Resume characters", f"{resume_chars:,}")

            with stat2:
                st.metric("Job description words", f"{jd_words:,}")

            with stat3:
                st.metric("Job description characters", f"{jd_chars:,}")

            with stat4:
                st.metric("Detected resume skills", len(resume_skills))

            # ------------------------------------------
            # 12. MATCHED SKILL FREQUENCY
            # ------------------------------------------
            if matched_skills:
                st.write("")
                st.markdown("### Matched skill mentions")

                st.caption(
                    "Approximate literal mentions in extracted resume "
                    "text. This does not measure proficiency."
                )

                frequency_items = sorted(
                    skill_frequency.items(),
                    key=lambda item: item[1],
                    reverse=True,
                )

                for skill, count in frequency_items[:10]:
                    st.markdown(f"**{skill}** — {count} mention(s)")
                    st.progress(
                        min(count / max(
                            max(skill_frequency.values()), 1
                        ), 1.0)
                    )

            # ------------------------------------------
            # 13. EXTRACTED TEXT PREVIEW
            # ------------------------------------------
            st.divider()
            with st.expander("View extracted resume text"):
                st.caption(
                    "Check this preview if a skill appears to be missing. "
                    "PDF text extraction may not preserve every layout."
                )
                st.text_area(
                    "Extracted text",
                    value=resume_text,
                    height=300,
                    disabled=True,
                    label_visibility="collapsed",
                )

            # ------------------------------------------
            # 14. DOWNLOADABLE REPORT
            # ------------------------------------------
            report_lines = [
                "TALENTLENS - RESUME ANALYSIS REPORT",
                "=" * 42,
                f"Resume file: {pdf.name}",
                f"Estimated match score: {score:.1f}%",
                f"Skill coverage: {skill_coverage:.1f}%",
                f"Resume word count: {resume_words}",
                f"Job description word count: {jd_words}",
                "",
                "MATCHED SKILLS",
                *(
                    [f"- {skill}" for skill in matched_skills]
                    if matched_skills
                    else ["- None detected"]
                ),
                "",
                "SKILLS TO REVIEW",
                *(
                    [f"- {skill}" for skill in missing_skills]
                    if missing_skills
                    else ["- None detected"]
                ),
                "",
                "Note: This is an estimate, not an official ATS score "
                "or a guarantee of selection.",
            ]

            st.download_button(
                "⬇️ Download analysis report",
                data="\n".join(report_lines),
                file_name="resume_analysis_report.txt",
                mime="text/plain",
                use_container_width=True,
            )

            st.caption(
                "Scoring note: the current model combines 40% text "
                "similarity with 60% detected skill overlap. It does "
                "not verify experience, skill proficiency, formatting, "
                "or every requirement in the job description."
            )

        except FileNotFoundError as e:
            st.error(
                "A required project file could not be found. "
                "Check data/skills_list.txt and your matcher folder."
            )
            st.exception(e)

        except Exception as e:
            st.error(
                "Analysis failed. Check the error details below "
                "to identify the exact issue."
            )
            st.exception(e)


# --------------------------------------------------
# 15. FOOTER
# --------------------------------------------------
st.write("")
st.markdown(
    """
    <div class="footer">
        <b>TalentLens</b> · Resume Intelligence & Skill Matching<br>
        Built to help job seekers prepare with more clarity.
    </div>
    """,
    unsafe_allow_html=True,
)

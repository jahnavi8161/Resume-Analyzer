import streamlit as st
import pdfplumber
import requests
from streamlit_lottie import st_lottie
import pandas as pd

st.set_page_config(page_title="Smart Resume Analyzer", page_icon="📄", layout="wide")

# -----------------------------
# Load Animation
# -----------------------------
def load_lottie(url):
    r = requests.get(url)
    return r.json()

lottie = load_lottie("https://assets4.lottiefiles.com/packages/lf20_tutvdkg0.json")

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>

.skill-badge {
display:inline-block;
padding:8px 12px;
margin:5px;
background-color:#4CAF50;
color:white;
border-radius:8px;
font-size:14px;
}

.missing-badge {
display:inline-block;
padding:8px 12px;
margin:5px;
background-color:#FF5252;
color:white;
border-radius:8px;
font-size:14px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
col1, col2 = st.columns([2,1])

with col1:
    st.title("📄 Smart Resume Analyzer")
    st.write("Analyze your resume like an ATS system and identify skill gaps.")

with col2:
    st_lottie(lottie, height=150)

st.divider()

# -----------------------------
# Branch Selection
# -----------------------------
branch = st.selectbox(
    "🎓 Select Your Branch",
    [
        "Computer Science",
        "Data Science",
        "Artificial Intelligence",
        "Information Technology",
        "Electronics",
        "Mechanical"
    ]
)

# -----------------------------
# Role Selection
# -----------------------------
role = st.selectbox(
    "💼 Target Role",
    [
        "Data Scientist",
        "Machine Learning Engineer",
        "Data Analyst",
        "Cloud Engineer",
        "Software Developer",
        "Mechanical Design Engineer",
        "CAD Engineer",
        "Manufacturing Engineer",
        "Embedded Systems Engineer",
        "VLSI Engineer",
        "Electronics Design Engineer"
    ]
)

# -----------------------------
# Job Description
# -----------------------------
job_description = st.text_area(
    "📋 Paste Job Description (Optional)",
    height=150
)

uploaded_file = st.file_uploader("📂 Upload Resume (PDF)", type="pdf")

# -----------------------------
# Role Skill Database
# -----------------------------
role_skills = {

"Data Scientist":{
"python":["python"],
"pandas":["pandas"],
"numpy":["numpy"],
"machine learning":["machine learning","ml model","ml algorithm"],
"statistics":["statistics","statistical analysis"],
"sql":["sql","mysql","postgres"],
"data analysis":["data analysis","data analytics"]
},

"Machine Learning Engineer":{
"python":["python"],
"tensorflow":["tensorflow"],
"pytorch":["pytorch"],
"deep learning":["deep learning","neural network"],
"mlops":["mlops"],
"docker":["docker"]
},

"Data Analyst":{
"sql":["sql"],
"excel":["excel"],
"python":["python"],
"tableau":["tableau"],
"power bi":["power bi","powerbi"],
"data visualization":["data visualization","data viz"]
},

"Cloud Engineer":{
"aws":["aws","amazon web services"],
"docker":["docker"],
"kubernetes":["kubernetes","k8s"],
"linux":["linux"],
"terraform":["terraform"],
"cloud":["cloud computing"]
},

"Software Developer":{
"java":["java"],
"python":["python"],
"c++":["c++"],
"git":["git"],
"data structures":["data structures"],
"algorithms":["algorithms"]
},

"Mechanical Design Engineer":{
"cad":["cad","computer aided design"],
"solidworks":["solidworks"],
"ansys":["ansys"],
"thermodynamics":["thermodynamics"],
"mechanical design":["mechanical design"]
},

"CAD Engineer":{
"cad":["cad"],
"solidworks":["solidworks"],
"autocad":["autocad"],
"3d modeling":["3d modeling","3d design"]
},

"Manufacturing Engineer":{
"manufacturing":["manufacturing"],
"lean manufacturing":["lean"],
"six sigma":["six sigma"],
"production":["production"]
},

"Embedded Systems Engineer":{
"embedded systems":["embedded systems"],
"microcontrollers":["microcontroller","microcontrollers"],
"c programming":["c programming","embedded c"],
"arduino":["arduino"],
"rtos":["rtos"]
},

"VLSI Engineer":{
"vlsi":["vlsi"],
"verilog":["verilog"],
"system verilog":["system verilog"],
"asic":["asic"],
"fpga":["fpga"]
},

"Electronics Design Engineer":{
"circuit design":["circuit design"],
"pcb design":["pcb design"],
"analog electronics":["analog electronics"],
"digital electronics":["digital electronics"],
"matlab":["matlab"]
}

}

# -----------------------------
# Resume Analysis
# -----------------------------
if uploaded_file:

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    text = text.lower()

    skills = role_skills[role]

    detected = []
    missing = []

    for skill, keywords in skills.items():

        found = False

        for word in keywords:
            if word in text:
                found = True
                break

        if found:
            detected.append(skill)
        else:
            missing.append(skill)

    score = int((len(detected) / len(skills)) * 100)

    st.subheader("📊 Resume Score")

    st.progress(score/100)
    st.write(f"**Score: {score} / 100**")

    if score > 80:
        st.success("Strong resume for this role.")
    elif score > 60:
        st.warning("Good resume but could improve.")
    else:
        st.error("Resume needs improvement for this role.")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("✅ Detected Skills")

        for skill in detected:
            st.markdown(
                f"<span class='skill-badge'>✔ {skill.title()}</span>",
                unsafe_allow_html=True
            )

    with col2:

        st.subheader("⚠ Missing Skills")

        for skill in missing:
            st.markdown(
                f"<span class='missing-badge'>✖ {skill.title()}</span>",
                unsafe_allow_html=True
            )

    st.divider()

    # -----------------------------
    # Suggestions
    # -----------------------------
    st.subheader("💡 Suggestions to Improve Resume")

    if missing:
        for skill in missing:
            st.write(f"• Consider adding experience or projects related to **{skill.title()}**")
    else:
        st.success("Your resume already covers the important skills for this role.")

    st.divider()

    # -----------------------------
    # ATS Match Score
    # -----------------------------
    if job_description:

        jd_words = job_description.lower().split()

        matched = [word for word in jd_words if word in text]

        match_score = int((len(set(matched)) / len(set(jd_words))) * 100)

        st.subheader("📈 ATS Match Score")

        st.progress(match_score/100)
        st.write(f"**Match Score: {match_score}%**")

    # -----------------------------
    # Skill Chart
    # -----------------------------
    data = pd.DataFrame({
        "Type":["Detected Skills","Missing Skills"],
        "Count":[len(detected),len(missing)]
    })

    st.subheader("📊 Skill Overview")

    st.bar_chart(data.set_index("Type"))

    # -----------------------------
    # Download Report
    # -----------------------------
    report = f"""
Resume Analysis Report

Target Role: {role}

Resume Score: {score}/100

Detected Skills:
{detected}

Missing Skills:
{missing}
"""

    st.download_button(
        "📥 Download Analysis Report",
        report,
        file_name="resume_analysis_report.txt"
    )
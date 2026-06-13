import pandas as pd
import numpy as np
import random
from datetime import datetime

np.random.seed(42)
random.seed(42)

# ==============================
# CONFIGURATION
# ==============================

rows = 50000
students = 10000

college_names = [
    "ABC Engineering College",
    "XYZ Institute of Technology",
    "PQR Degree College",
    "Vignan Institute",
    "Aurora College",
    "Malla Reddy College",
    "CMR Technical Campus",
    "BVRIT College",
    "Anurag University",
    "Geethanjali College",
    "Sreenidhi Institute of Science",
    "Guru Nanak Institute",
    "Vardhaman College",
    "ACE Engineering College",
    "TKR Engineering College",
    "KITS Engineering College",
    "MREC College",
    "NRI Institute of Technology",
    "KL University",
    "GITAM University",
    "CVR College of Engineering",
    "Mahindra University",
    "ICFAI Tech School",
    "MVSR Engineering College",
    "Sreyas Institute",
    "CMR Engineering College",
    "Nalla Malla Reddy College",
    "Bhoj Reddy Engineering College",
    "Methodist College",
    "Vasavi College of Engineering",
    "JNTUH College of Engineering",
    "Osmania University College",
    "Kakatiya Institute of Technology",
    "Siddhartha Engineering College",
    "Pragati Engineering College",
    "Aditya Engineering College",
    "RVR and JC College",
    "SRKR Engineering College",
    "Lakireddy Bali Reddy College",
    "KLU Business School",
    "Andhra Loyola Institute",
    "VVIT Engineering College",
    "Narasaraopeta Engineering College",
    "Gokaraju Rangaraju Institute",
    "Stanley College of Engineering",
    "Sphoorthy Engineering College",
    "Malla Reddy University",
    "BVC Engineering College",
    "Vemu Institute of Technology",
    "SR University"
]

college_ids = {}

for i, college in enumerate(college_names, start=1):
    college_ids[college] = f"COL{i:03d}"

departments = [
    "CSE", "ECE", "EEE", "MECH",
    "CIVIL", "IT", "AIML", "DS"
]

activity_types = [
    "Aptitude",
    "Coding",
    "Verbal",
    "MET",
    "Assignment",
    "Project",
    "Course"
]

activity_names = {
    "Aptitude": [
        "Quantitative Aptitude",
        "Logical Reasoning",
        "Number Series",
        "Time and Work",
        "Profit and Loss"
    ],
    "Coding": [
        "Python Basics",
        "Java Basics",
        "DSA Practice",
        "SQL Practice",
        "Coding Challenge"
    ],
    "Verbal": [
        "Communication Test",
        "Grammar Practice",
        "Reading Comprehension",
        "Email Writing",
        "Vocabulary Test"
    ],
    "MET": [
        "Monthly Employability Test",
        "MET Round 1",
        "MET Round 2",
        "MET Mock Assessment"
    ],
    "Assignment": [
        "Python Assignment",
        "SQL Assignment",
        "Aptitude Assignment",
        "Verbal Assignment",
        "Coding Assignment"
    ],
    "Project": [
        "Mini Project",
        "Major Project",
        "AI Project",
        "Web App Project",
        "Data Analytics Project"
    ],
    "Course": [
        "Python Course",
        "Java Course",
        "Data Analytics Course",
        "Power BI Course",
        "Interview Preparation Course"
    ]
}

months = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

# ==============================
# DATA GENERATION
# ==============================

data = []

for i in range(rows):

    college = random.choice(college_names)
    college_id = college_ids[college]

    student_id = f"STU{random.randint(1, students):05d}"
    student_name = f"Student_{student_id}"

    department = random.choice(departments)
    year = random.randint(1, 4)

    month_num = random.randint(1, 12)
    month = months[month_num - 1]

    activity_date = datetime(
        2026,
        month_num,
        random.randint(1, 27)
    ).strftime("%Y-%m-%d")

    activity_type = random.choice(activity_types)
    activity_name = random.choice(activity_names[activity_type])

    attempted = random.choices(
        ["Yes", "No"],
        weights=[82, 18]
    )[0]

    if attempted == "Yes":

        completed = random.choices(
            ["Yes", "No"],
            weights=[72, 28]
        )[0]

        if completed == "Yes":
            score = random.randint(35, 100)
        else:
            score = random.randint(0, 69)

        time_spent = random.randint(10, 120)
        login_count = random.randint(1, 30)
        status = "Active"

    else:
        completed = "No"
        score = 0
        time_spent = 0
        login_count = 0
        status = "Inactive"

    if completed == "Yes":
        completion_rate = 100
    else:
        completion_rate = 0

    engagement_score = (
        login_count * 2 +
        time_spent * 0.2 +
        score * 0.5
    )

    if completed == "Yes":
        engagement_score = engagement_score + 20

    engagement_score = round(
        min(100, engagement_score),
        2
    )

    if engagement_score >= 80:
        engagement_level = "High"
    elif engagement_score >= 50:
        engagement_level = "Medium"
    elif engagement_score > 0:
        engagement_level = "Low"
    else:
        engagement_level = "Inactive"

    if score >= 85:
        performance_band = "A"
    elif score >= 75:
        performance_band = "B"
    elif score >= 65:
        performance_band = "C"
    elif score >= 50:
        performance_band = "D"
    elif score > 0:
        performance_band = "E"
    else:
        performance_band = "F"

    if (
        engagement_score >= 70
        and score >= 70
        and completed == "Yes"
    ):
        placement_ready = "Yes"
    else:
        placement_ready = "No"

    data.append([
        college_id,
        college,
        student_id,
        student_name,
        department,
        year,
        month,
        activity_date,
        activity_type,
        activity_name,
        attempted,
        completed,
        score,
        time_spent,
        login_count,
        completion_rate,
        engagement_score,
        engagement_level,
        performance_band,
        placement_ready,
        status
    ])

# ==============================
# CREATE DATAFRAME
# ==============================

columns = [
    "College_ID",
    "College_Name",
    "Student_ID",
    "Student_Name",
    "Department",
    "Year",
    "Month",
    "Activity_Date",
    "Activity_Type",
    "Activity_Name",
    "Attempted",
    "Completed",
    "Score",
    "Time_Spent_Minutes",
    "Login_Count",
    "Completion_Rate",
    "Engagement_Score",
    "Engagement_Level",
    "Performance_Band",
    "Placement_Ready",
    "Status"
]

df = pd.DataFrame(data, columns=columns)

# ==============================
# SUMMARY DATA
# ==============================

summary = {
    "Metric": [
        "Total Records",
        "Total Colleges",
        "Total Students",
        "Active Records",
        "Inactive Records",
        "Completed Activities",
        "Placement Ready Records"
    ],
    "Value": [
        len(df),
        df["College_Name"].nunique(),
        df["Student_ID"].nunique(),
        len(df[df["Status"] == "Active"]),
        len(df[df["Status"] == "Inactive"]),
        len(df[df["Completed"] == "Yes"]),
        len(df[df["Placement_Ready"] == "Yes"])
    ]
}

summary_df = pd.DataFrame(summary)

# ==============================
# SAVE EXCEL FILE
# ==============================

file_name = "TaPTaP_College_Engagement_Analytics_50000.xlsx"

with pd.ExcelWriter(file_name, engine="openpyxl") as writer:
    df.to_excel(
        writer,
        sheet_name="Activity_Data",
        index=False
    )

    summary_df.to_excel(
        writer,
        sheet_name="Summary",
        index=False
    )

print("Excel file generated successfully!")
print("Rows:", len(df))
print("Colleges:", df["College_Name"].nunique())
print("Students:", df["Student_ID"].nunique())
print("File Name:", file_name)
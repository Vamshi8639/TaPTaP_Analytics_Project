import pandas as pd

df = pd.read_excel(
    "TaPTaP_College_Engagement_Analytics_50000.xlsx",
    sheet_name="Activity_Data"
)

print("===================================")
print("TaPTaP Analytics Dashboard")
print("===================================")

total_colleges = df["College_Name"].nunique()
total_students = df["Student_ID"].nunique()

active_students = df[
    df["Status"] == "Active"
]["Student_ID"].nunique()

inactive_students = df[
    df["Status"] == "Inactive"
]["Student_ID"].nunique()

placement_ready = len(
    df[df["Placement_Ready"] == "Yes"]
)

completed = len(
    df[df["Completed"] == "Yes"]
)

total_records = len(df)

completion_rate = round(
    (completed / total_records) * 100,
    2
)

print(f"Total Colleges : {total_colleges}")
print(f"Total Students : {total_students}")
print(f"Active Students : {active_students}")
print(f"Inactive Students : {inactive_students}")
print(f"Placement Ready Records : {placement_ready}")
print(f"Completed Activities : {completed}")
print(f"Completion Rate : {completion_rate}%")
print("\n===================================")
print("COLLEGE ANALYTICS")
print("===================================")

college_score = df.groupby(
    "College_Name"
)["Engagement_Score"].mean()

best_college = college_score.idxmax()
worst_college = college_score.idxmin()

print(f"Best Performing College : {best_college}")
print(f"Average Score : {college_score.max():.2f}")

print()

print(f"Worst Performing College : {worst_college}")
print(f"Average Score : {college_score.min():.2f}")

print("\n===================================")
print("MONTH ANALYTICS")
print("===================================")

month_activity = df.groupby(
    "Month"
).size()

highest_month = month_activity.idxmax()
lowest_month = month_activity.idxmin()

print(f"Highest Activity Month : {highest_month}")
print(f"Activities : {month_activity.max()}")

print()

print(f"Lowest Activity Month : {lowest_month}")
print(f"Activities : {month_activity.min()}")

print("\n===================================")
print("ACTIVITY ANALYTICS")
print("===================================")

activity_count = df.groupby(
    "Activity_Type"
).size()

print("Most Attempted Activity :")
print(activity_count.idxmax())

print()

print("Least Attempted Activity :")
print(activity_count.idxmin())
# ===================================
# TOP 10 COLLEGES
# ===================================

print("\n===================================")
print("TOP 10 COLLEGES")
print("===================================")

top_colleges = (
    df.groupby("College_Name")["Engagement_Score"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

print(top_colleges)

# ===================================
# BOTTOM 10 COLLEGES
# ===================================

print("\n===================================")
print("BOTTOM 10 COLLEGES")
print("===================================")

bottom_colleges = (
    df.groupby("College_Name")["Engagement_Score"]
    .mean()
    .sort_values()
    .head(10)
)

print(bottom_colleges)

# ===================================
# COLLEGE RANKING TABLE
# ===================================

print("\n===================================")
print("COLLEGE RANKING")
print("===================================")

college_ranking = (
    df.groupby("College_Name")["Engagement_Score"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

college_ranking["Rank"] = range(
    1,
    len(college_ranking) + 1
)

college_ranking = college_ranking[
    ["Rank", "College_Name", "Engagement_Score"]
]

print(college_ranking.head(20))
# ===================================
# STUDENT ANALYTICS
# ===================================

print("\n===================================")
print("STUDENT ANALYTICS")
print("===================================")

student_activity = df.groupby(
    ["Student_ID", "Student_Name", "College_Name"]
).agg(
    Total_Activities=("Activity_Type", "count"),
    Completed_Activities=("Completed", lambda x: (x == "Yes").sum()),
    Average_Score=("Score", "mean"),
    Average_Engagement=("Engagement_Score", "mean"),
    Total_Login_Count=("Login_Count", "sum")
).reset_index()

student_activity["Completion_Rate"] = round(
    (student_activity["Completed_Activities"] / student_activity["Total_Activities"]) * 100,
    2
)

# Top 10 active students
print("\n===================================")
print("TOP 10 ACTIVE STUDENTS")
print("===================================")

top_students = student_activity.sort_values(
    by="Average_Engagement",
    ascending=False
).head(10)

print(top_students)

# Least 10 active students
print("\n===================================")
print("LEAST 10 ACTIVE STUDENTS")
print("===================================")

least_students = student_activity.sort_values(
    by="Average_Engagement",
    ascending=True
).head(10)

print(least_students)

# ===================================
# ACTIVE STUDENTS BY COLLEGE
# ===================================

print("\n===================================")
print("ACTIVE STUDENTS BY COLLEGE")
print("===================================")

active_by_college = df[df["Status"] == "Active"].groupby(
    "College_Name"
)["Student_ID"].nunique().sort_values(ascending=False)

print(active_by_college.head(10))

# ===================================
# INACTIVE STUDENTS BY COLLEGE
# ===================================

print("\n===================================")
print("INACTIVE STUDENTS BY COLLEGE")
print("===================================")

inactive_by_college = df[df["Status"] == "Inactive"].groupby(
    "College_Name"
)["Student_ID"].nunique().sort_values(ascending=False)

print(inactive_by_college.head(10))
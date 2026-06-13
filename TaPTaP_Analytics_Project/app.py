import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE SETTINGS
# =========================

st.set_page_config(
    page_title="TaPTaP College Analytics Dashboard",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================

df = pd.read_csv(
    "TaPTaP_College_Engagement_Analytics_50000.csv"
)
df["Activity_Date"] = pd.to_datetime(df["Activity_Date"])

# =========================
# TITLE
# =========================

st.title("🎓 TaPTaP College Performance & Student Engagement Analytics Dashboard")

st.write(
    "This dashboard helps colleges track student activity, test participation, learning progress, completion rate, active students, inactive students, and placement readiness."
)

st.markdown("---")

# =========================
# SIDEBAR FILTERS
# =========================

st.sidebar.header("🔎 Filters")

college_filter = st.sidebar.selectbox(
    "Select College",
    ["All"] + sorted(df["College_Name"].unique().tolist())
)

department_filter = st.sidebar.selectbox(
    "Select Department",
    ["All"] + sorted(df["Department"].unique().tolist())
)

month_filter = st.sidebar.selectbox(
    "Select Month",
    ["All"] + sorted(df["Month"].unique().tolist())
)

activity_filter = st.sidebar.selectbox(
    "Select Activity Type",
    ["All"] + sorted(df["Activity_Type"].unique().tolist())
)

filtered_df = df.copy()

if college_filter != "All":
    filtered_df = filtered_df[filtered_df["College_Name"] == college_filter]

if department_filter != "All":
    filtered_df = filtered_df[filtered_df["Department"] == department_filter]

if month_filter != "All":
    filtered_df = filtered_df[filtered_df["Month"] == month_filter]

if activity_filter != "All":
    filtered_df = filtered_df[filtered_df["Activity_Type"] == activity_filter]

# =========================
# KPI CARDS
# =========================

st.header("📌 Overall Summary")

total_colleges = filtered_df["College_Name"].nunique()
total_students = filtered_df["Student_ID"].nunique()
total_records = len(filtered_df)

active_students = filtered_df[
    filtered_df["Status"] == "Active"
]["Student_ID"].nunique()

inactive_students = filtered_df[
    filtered_df["Status"] == "Inactive"
]["Student_ID"].nunique()

completed_activities = len(
    filtered_df[filtered_df["Completed"] == "Yes"]
)

attempted_activities = len(
    filtered_df[filtered_df["Attempted"] == "Yes"]
)

placement_ready = filtered_df[
    filtered_df["Placement_Ready"] == "Yes"
]["Student_ID"].nunique()

completion_rate = 0

if total_records > 0:
    completion_rate = round(
        (completed_activities / total_records) * 100,
        2
    )

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Colleges", total_colleges)
c2.metric("Total Students", total_students)
c3.metric("Active Students", active_students)
c4.metric("Inactive Students", inactive_students)

c5, c6, c7, c8 = st.columns(4)

c5.metric("Total Activities", total_records)
c6.metric("Attempted Activities", attempted_activities)
c7.metric("Completed Activities", completed_activities)
c8.metric("Completion Rate", f"{completion_rate}%")

c9, c10 = st.columns(2)

c9.metric("Placement Ready Students", placement_ready)
c10.metric("Average Engagement Score", round(filtered_df["Engagement_Score"].mean(), 2))

st.markdown("---")

# =========================
# IMPORTANT INSIGHTS
# =========================

st.header("📊 Key Insights")

if len(filtered_df) > 0:

    best_college = filtered_df.groupby(
        "College_Name"
    )["Engagement_Score"].mean().idxmax()

    worst_college = filtered_df.groupby(
        "College_Name"
    )["Engagement_Score"].mean().idxmin()

    highest_month = filtered_df.groupby(
        "Month"
    ).size().idxmax()

    lowest_month = filtered_df.groupby(
        "Month"
    ).size().idxmin()

    most_activity = filtered_df.groupby(
        "Activity_Type"
    ).size().idxmax()

    least_activity = filtered_df.groupby(
        "Activity_Type"
    ).size().idxmin()

    i1, i2, i3 = st.columns(3)

    i1.success(f"Best Performing College: {best_college}")
    i2.warning(f"Lowest Performing College: {worst_college}")
    i3.info(f"Most Attempted Activity: {most_activity}")

    i4, i5, i6 = st.columns(3)

    i4.success(f"Highest Activity Month: {highest_month}")
    i5.warning(f"Lowest Activity Month: {lowest_month}")
    i6.info(f"Least Attempted Activity: {least_activity}")

st.markdown("---")

# =========================
# COLLEGE RANKING
# =========================

st.header("🏆 College Performance Ranking")

college_ranking = filtered_df.groupby(
    "College_Name"
).agg(
    Total_Students=("Student_ID", "nunique"),
    Total_Activities=("Activity_Type", "count"),
    Completed_Activities=("Completed", lambda x: (x == "Yes").sum()),
    Average_Score=("Score", "mean"),
    Average_Engagement=("Engagement_Score", "mean"),
    Placement_Ready=("Placement_Ready", lambda x: (x == "Yes").sum())
).reset_index()

college_ranking["Completion_Rate"] = round(
    (college_ranking["Completed_Activities"] / college_ranking["Total_Activities"]) * 100,
    2
)

college_ranking = college_ranking.sort_values(
    "Average_Engagement",
    ascending=False
)

college_ranking["Rank"] = range(1, len(college_ranking) + 1)

st.dataframe(college_ranking)

# =========================
# TABS
# =========================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "College Analytics",
    "Monthly Analytics",
    "Activity Analytics",
    "Student Analytics",
    "Student Lists"
])

# =========================
# TAB 1 - COLLEGE ANALYTICS
# =========================

with tab1:

    st.subheader("Top 10 Colleges by Engagement Score")

    top_colleges = college_ranking.head(10)

    fig1 = px.bar(
        top_colleges,
        x="Average_Engagement",
        y="College_Name",
        orientation="h",
        title="Top 10 Colleges"
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Bottom 10 Colleges by Engagement Score")

    bottom_colleges = college_ranking.tail(10)

    fig2 = px.bar(
        bottom_colleges,
        x="Average_Engagement",
        y="College_Name",
        orientation="h",
        title="Bottom 10 Colleges"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Active Students by College")

    active_college = filtered_df[
        filtered_df["Status"] == "Active"
    ].groupby("College_Name")["Student_ID"].nunique().sort_values(
        ascending=False
    ).head(15).reset_index()

    fig3 = px.bar(
        active_college,
        x="Student_ID",
        y="College_Name",
        orientation="h",
        title="Top Colleges by Active Students"
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Inactive Students by College")

    inactive_college = filtered_df[
        filtered_df["Status"] == "Inactive"
    ].groupby("College_Name")["Student_ID"].nunique().sort_values(
        ascending=False
    ).head(15).reset_index()

    fig4 = px.bar(
        inactive_college,
        x="Student_ID",
        y="College_Name",
        orientation="h",
        title="Top Colleges by Inactive Students"
    )

    st.plotly_chart(fig4, use_container_width=True)

# =========================
# TAB 2 - MONTHLY ANALYTICS
# =========================

with tab2:

    st.subheader("Month Wise Activity Count")

    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    month_activity = filtered_df.groupby(
        "Month"
    ).size().reindex(month_order).reset_index()

    month_activity.columns = ["Month", "Activities"]

    fig5 = px.line(
        month_activity,
        x="Month",
        y="Activities",
        markers=True,
        title="Month Wise Activity Trend"
    )

    st.plotly_chart(fig5, use_container_width=True)

    st.subheader("Month Wise Completed Activities")

    month_completed = filtered_df[
        filtered_df["Completed"] == "Yes"
    ].groupby("Month").size().reindex(month_order).reset_index()

    month_completed.columns = ["Month", "Completed"]

    fig6 = px.bar(
        month_completed,
        x="Month",
        y="Completed",
        title="Month Wise Completed Activities"
    )

    st.plotly_chart(fig6, use_container_width=True)

    st.subheader("Month Wise Attempted Activities")

    month_attempted = filtered_df[
        filtered_df["Attempted"] == "Yes"
    ].groupby("Month").size().reindex(month_order).reset_index()

    month_attempted.columns = ["Month", "Attempted"]

    fig7 = px.bar(
        month_attempted,
        x="Month",
        y="Attempted",
        title="Month Wise Attempted Activities"
    )

    st.plotly_chart(fig7, use_container_width=True)

# =========================
# TAB 3 - ACTIVITY ANALYTICS
# =========================

with tab3:

    st.subheader("Activity Type Distribution")

    activity_distribution = filtered_df["Activity_Type"].value_counts().reset_index()
    activity_distribution.columns = ["Activity_Type", "Count"]

    fig8 = px.pie(
        activity_distribution,
        names="Activity_Type",
        values="Count",
        title="Activity Type Distribution"
    )

    st.plotly_chart(fig8, use_container_width=True)

    st.subheader("Attempted Activities by Type")

    attempted_by_type = filtered_df[
        filtered_df["Attempted"] == "Yes"
    ].groupby("Activity_Type").size().reset_index()

    attempted_by_type.columns = ["Activity_Type", "Attempts"]

    fig9 = px.bar(
        attempted_by_type,
        x="Activity_Type",
        y="Attempts",
        title="Attempts by Activity Type"
    )

    st.plotly_chart(fig9, use_container_width=True)

    st.subheader("Completed Activities by Type")

    completed_by_type = filtered_df[
        filtered_df["Completed"] == "Yes"
    ].groupby("Activity_Type").size().reset_index()

    completed_by_type.columns = ["Activity_Type", "Completed"]

    fig10 = px.bar(
        completed_by_type,
        x="Activity_Type",
        y="Completed",
        title="Completed Activities by Type"
    )

    st.plotly_chart(fig10, use_container_width=True)

    st.subheader("Average Score by Activity Type")

    score_by_type = filtered_df.groupby(
        "Activity_Type"
    )["Score"].mean().reset_index()

    fig11 = px.bar(
        score_by_type,
        x="Activity_Type",
        y="Score",
        title="Average Score by Activity Type"
    )

    st.plotly_chart(fig11, use_container_width=True)

# =========================
# TAB 4 - STUDENT ANALYTICS
# =========================

with tab4:

    st.subheader("Department Wise Activity")

    dept_activity = filtered_df.groupby(
        "Department"
    ).size().reset_index()

    dept_activity.columns = ["Department", "Activities"]

    fig12 = px.bar(
        dept_activity,
        x="Department",
        y="Activities",
        title="Department Wise Activity"
    )

    st.plotly_chart(fig12, use_container_width=True)

    st.subheader("Department Wise Average Engagement")

    dept_engagement = filtered_df.groupby(
        "Department"
    )["Engagement_Score"].mean().reset_index()

    fig13 = px.bar(
        dept_engagement,
        x="Department",
        y="Engagement_Score",
        title="Department Wise Average Engagement"
    )

    st.plotly_chart(fig13, use_container_width=True)

    st.subheader("Performance Band Distribution")

    band_distribution = filtered_df["Performance_Band"].value_counts().reset_index()
    band_distribution.columns = ["Performance_Band", "Count"]

    fig14 = px.bar(
        band_distribution,
        x="Performance_Band",
        y="Count",
        title="Performance Band Distribution"
    )

    st.plotly_chart(fig14, use_container_width=True)

    st.subheader("Placement Ready Distribution")

    placement_distribution = filtered_df["Placement_Ready"].value_counts().reset_index()
    placement_distribution.columns = ["Placement_Ready", "Count"]

    fig15 = px.pie(
        placement_distribution,
        names="Placement_Ready",
        values="Count",
        title="Placement Ready Distribution"
    )

    st.plotly_chart(fig15, use_container_width=True)

# =========================
# TAB 5 - STUDENT LISTS
# =========================

with tab5:

    st.subheader("Top 10 Active Students")

    student_summary = filtered_df.groupby(
        ["Student_ID", "Student_Name", "College_Name", "Department"]
    ).agg(
        Total_Activities=("Activity_Type", "count"),
        Completed_Activities=("Completed", lambda x: (x == "Yes").sum()),
        Average_Score=("Score", "mean"),
        Average_Engagement=("Engagement_Score", "mean"),
        Login_Count=("Login_Count", "sum")
    ).reset_index()

    student_summary["Completion_Rate"] = round(
        (student_summary["Completed_Activities"] / student_summary["Total_Activities"]) * 100,
        2
    )

    top_students = student_summary.sort_values(
        "Average_Engagement",
        ascending=False
    ).head(10)

    st.dataframe(top_students)

    st.subheader("Least Active Students")

    least_students = student_summary.sort_values(
        "Average_Engagement",
        ascending=True
    ).head(10)

    st.dataframe(least_students)

    st.subheader("Active Students List")

    active_students_list = filtered_df[
        filtered_df["Status"] == "Active"
    ][
        ["College_Name", "Student_ID", "Student_Name", "Department", "Activity_Type", "Score"]
    ].drop_duplicates()

    st.dataframe(active_students_list)

    st.subheader("Inactive Students List")

    inactive_students_list = filtered_df[
        filtered_df["Status"] == "Inactive"
    ][
        ["College_Name", "Student_ID", "Student_Name", "Department", "Activity_Type", "Score"]
    ].drop_duplicates()

    st.dataframe(inactive_students_list)

# =========================
# DOWNLOAD
# =========================

st.markdown("---")

st.header("⬇ Download Filtered Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download CSV",
    csv,
    "filtered_taptap_data.csv",
    "text/csv"
)

st.success("TaPTaP Dashboard Loaded Successfully")

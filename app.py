from flask import Flask, render_template, request, send_file
import pandas as pd
import pickle
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch


app = Flask(__name__)


# ==========================================
# LOAD MACHINE LEARNING MODEL
# ==========================================

with open("placement_model.pkl", "rb") as file:
    model = pickle.load(file)


# Store latest prediction
latest_student = {}


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    probability = None
    suggestions = []
    student_name = None

    if request.method == "POST":

        # Student name
        student_name = request.form["student_name"]

        # Student details
        cgpa = float(request.form["cgpa"])
        aptitude = float(request.form["aptitude"])
        skills = int(request.form["skills"])
        internships = int(request.form["internships"])
        projects = int(request.form["projects"])
        communication = float(request.form["communication"])
        backlogs = int(request.form["backlogs"])
        certifications = int(request.form["certifications"])


        # ==========================================
        # PREPARE DATA FOR MODEL
        # ==========================================

        student_data = [[
            cgpa,
            aptitude,
            skills,
            internships,
            projects,
            communication,
            backlogs,
            certifications
        ]]


        student_data = pd.DataFrame(
            student_data,
            columns=[
                "cgpa",
                "aptitude_score",
                "technical_skills",
                "internships",
                "projects",
                "communication_score",
                "backlogs",
                "certifications"
            ]
        )


        # ==========================================
        # PREDICTION
        # ==========================================

        prediction = model.predict(student_data)[0]

        probabilities = model.predict_proba(student_data)[0]

        probability = round(
            max(probabilities) * 100,
            2
        )


        if prediction == 1:

            result = "Likely to be Placed"

        else:

            result = "Not Likely to be Placed"


        # ==========================================
        # IMPROVEMENT SUGGESTIONS
        # ==========================================

        if cgpa < 7:
            suggestions.append(
                "Try to improve your CGPA."
            )

        if aptitude < 70:
            suggestions.append(
                "Practice aptitude and logical reasoning."
            )

        if skills < 5:
            suggestions.append(
                "Learn more technical skills."
            )

        if internships == 0:
            suggestions.append(
                "Try to complete at least one internship."
            )

        if projects < 2:
            suggestions.append(
                "Build more real-world projects."
            )

        if communication < 7:
            suggestions.append(
                "Improve your communication skills."
            )

        if backlogs > 0:
            suggestions.append(
                "Try to clear your backlogs."
            )

        if certifications < 2:
            suggestions.append(
                "Complete relevant technical certifications."
            )

        if len(suggestions) == 0:

            suggestions.append(
                "Your profile looks strong. Keep improving!"
            )


        # ==========================================
        # SAVE LATEST STUDENT
        # ==========================================

        latest_student.clear()

        latest_student.update({

            "name": student_name,

            "cgpa": cgpa,

            "aptitude": aptitude,

            "skills": skills,

            "internships": internships,

            "projects": projects,

            "communication": communication,

            "backlogs": backlogs,

            "certifications": certifications,

            "result": result,

            "probability": probability,

            "suggestions": suggestions

        })


    return render_template(

        "index.html",

        result=result,

        probability=probability,

        suggestions=suggestions,

        student_name=student_name

    )


# ==========================================
# DOWNLOAD PROFESSIONAL PDF REPORT
# ==========================================

@app.route("/download-report")
def download_report():

    if not latest_student:

        return "Please make a prediction first."


    file_name = "placement_prediction_report.pdf"


    document = SimpleDocTemplate(

        file_name,

        pagesize=A4,

        rightMargin=40,

        leftMargin=40,

        topMargin=40,

        bottomMargin=40

    )


    # ==========================================
    # STYLES
    # ==========================================

    styles = getSampleStyleSheet()


    title_style = ParagraphStyle(

        "TitleStyle",

        parent=styles["Title"],

        fontSize=22,

        leading=26,

        alignment=TA_CENTER,

        spaceAfter=10

    )


    subtitle_style = ParagraphStyle(

        "SubtitleStyle",

        parent=styles["Normal"],

        fontSize=11,

        alignment=TA_CENTER,

        textColor=colors.grey,

        spaceAfter=15

    )


    heading_style = ParagraphStyle(

        "HeadingStyle",

        parent=styles["Heading2"],

        fontSize=15,

        leading=18,

        spaceBefore=10,

        spaceAfter=10

    )


    normal_style = ParagraphStyle(

        "NormalStyle",

        parent=styles["BodyText"],

        fontSize=10,

        leading=15

    )


    result_style = ParagraphStyle(

        "ResultStyle",

        parent=styles["Heading1"],

        fontSize=18,

        alignment=TA_CENTER,

        spaceBefore=8,

        spaceAfter=8

    )


    # ==========================================
    # PDF CONTENT
    # ==========================================

    content = []


    # Header

    content.append(

        Paragraph(

            "🎓 COLLEGE PLACEMENT PREDICTION",

            title_style

        )

    )


    content.append(

        Paragraph(

            "Student Placement Assessment Report",

            subtitle_style

        )

    )


    content.append(

        HRFlowable(

            width="100%",

            thickness=1,

            color=colors.grey,

            spaceAfter=20

        )

    )


    # ==========================================
    # REPORT INFORMATION
    # ==========================================

    content.append(

        Paragraph(

            "Report Information",

            heading_style

        )

    )


    current_date = datetime.now().strftime(
        "%d-%m-%Y"
    )


    report_info = [

        ["Student Name", latest_student["name"]],

        ["Report Date", current_date],

        ["Assessment Type", "College Placement Prediction"],

        ["Machine Learning Model", "Random Forest"]

    ]


    info_table = Table(

        report_info,

        colWidths=[2.3 * inch, 3.7 * inch]

    )


    info_table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (0, -1),
             colors.lightgrey),

            ("GRID", (0, 0), (-1, -1),
             0.5, colors.grey),

            ("PADDING", (0, 0), (-1, -1), 8),

            ("FONTNAME", (0, 0), (0, -1),
             "Helvetica-Bold")

        ])

    )


    content.append(info_table)

    content.append(Spacer(1, 20))


    # ==========================================
    # STUDENT PERFORMANCE
    # ==========================================

    content.append(

        Paragraph(

            "Student Performance Details",

            heading_style

        )

    )


    performance_data = [

        ["Parameter", "Score"],

        ["CGPA", str(latest_student["cgpa"])],

        ["Aptitude Score",
         str(latest_student["aptitude"])],

        ["Technical Skills",
         str(latest_student["skills"])],

        ["Internships",
         str(latest_student["internships"])],

        ["Projects",
         str(latest_student["projects"])],

        ["Communication Score",
         str(latest_student["communication"])],

        ["Backlogs",
         str(latest_student["backlogs"])],

        ["Certifications",
         str(latest_student["certifications"])]

    ]


    performance_table = Table(

        performance_data,

        colWidths=[3.8 * inch, 2.2 * inch]

    )


    performance_table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0),
             colors.lightgrey),

            ("FONTNAME", (0, 0), (-1, 0),
             "Helvetica-Bold"),

            ("GRID", (0, 0), (-1, -1),
             0.5, colors.grey),

            ("PADDING", (0, 0), (-1, -1), 8)

        ])

    )


    content.append(performance_table)

    content.append(Spacer(1, 20))


    # ==========================================
    # PREDICTION RESULT
    # ==========================================

    content.append(

        Paragraph(

            "Placement Prediction",

            heading_style

        )

    )


    content.append(

        Paragraph(

            latest_student["result"],

            result_style

        )

    )


    result_data = [

        ["Prediction Confidence",
         str(latest_student["probability"]) + "%"],

        ["Algorithm",
         "Random Forest Classifier"],

        ["Test Accuracy",
         "91%"]

    ]


    result_table = Table(

        result_data,

        colWidths=[3.0 * inch, 3.0 * inch]

    )


    result_table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (0, -1),
             colors.lightgrey),

            ("GRID", (0, 0), (-1, -1),
             0.5, colors.grey),

            ("PADDING", (0, 0), (-1, -1), 8),

            ("FONTNAME", (0, 0), (0, -1),
             "Helvetica-Bold")

        ])

    )


    content.append(result_table)

    content.append(Spacer(1, 20))


    # ==========================================
    # IMPROVEMENT SUGGESTIONS
    # ==========================================

    content.append(

        Paragraph(

            "Improvement Suggestions",

            heading_style

        )

    )


    for suggestion in latest_student["suggestions"]:

        content.append(

            Paragraph(

                "• " + suggestion,

                normal_style

            )

        )

        content.append(Spacer(1, 5))


    content.append(Spacer(1, 15))


    # ==========================================
    # MODEL INFORMATION
    # ==========================================

    content.append(

        Paragraph(

            "Model Information",

            heading_style

        )

    )


    model_text = """

    The placement prediction system uses a Random Forest
    classification algorithm. The model analyzes academic,
    technical and professional factors to predict placement
    readiness.

    The model was evaluated using a synthetic dataset of
    500 student records with an 80:20 training and testing split.
    The reported accuracy is based on the synthetic test dataset.
    """


    content.append(

        Paragraph(

            model_text,

            normal_style

        )

    )


    content.append(Spacer(1, 15))


    # ==========================================
    # DISCLAIMER
    # ==========================================

    content.append(

        Paragraph(

            "Disclaimer",

            heading_style

        )

    )


    disclaimer = """

    This prediction is an educational machine learning
    assessment and should not be considered a guarantee
    of actual employment or placement. The training data
    used in this project is synthetic and does not represent
    actual college placement statistics.

    """


    content.append(

        Paragraph(

            disclaimer,

            normal_style

        )

    )


    content.append(Spacer(1, 20))


    content.append(

        HRFlowable(

            width="100%",

            thickness=0.5,

            color=colors.grey

        )

    )


    content.append(Spacer(1, 10))


    content.append(

        Paragraph(

            "Generated by College Placement Prediction System",

            subtitle_style

        )

    )


    # ==========================================
    # CREATE PDF
    # ==========================================

    document.build(content)


    return send_file(

        file_name,

        as_attachment=True

    )


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors

output_path = "sample_ai_author.pdf"

doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    rightMargin=54,
    leftMargin=54,
    topMargin=54,
    bottomMargin=54,
)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="TitleCentered",
    parent=styles["Title"],
    alignment=TA_CENTER,
    textColor=colors.HexColor("#1F4E79"),
    spaceAfter=18,
))
styles.add(ParagraphStyle(
    name="SectionHeading",
    parent=styles["Heading2"],
    textColor=colors.HexColor("#1F4E79"),
    spaceBefore=12,
    spaceAfter=6,
))

story = [
    Paragraph("Artificial Intelligence", styles["TitleCentered"]),
    Paragraph("<b>Author:</b> Avi", styles["Normal"]),
    Spacer(1, 14),
    Paragraph("Introduction", styles["SectionHeading"]),
    Paragraph(
        "Artificial Intelligence (AI) is a branch of computer science focused on building "
        "systems that can perform tasks commonly associated with human intelligence, such as "
        "understanding language, recognizing patterns, and solving problems.",
        styles["BodyText"],
    ),
    Paragraph("Applications of AI", styles["SectionHeading"]),
    ListFlowable(
        [ListItem(Paragraph(item, styles["BodyText"])) for item in [
            "Healthcare: supporting medical research and analysis.",
            "Education: personalizing learning experiences.",
            "Robotics: helping machines sense and act in the physical world.",
            "Natural Language Processing: working with human language.",
            "Computer Vision: interpreting images and videos.",
        ]],
        bulletType="bullet",
        leftIndent=18,
    ),
    Paragraph("Benefits of AI", styles["SectionHeading"]),
    ListFlowable(
        [ListItem(Paragraph(item, styles["BodyText"])) for item in [
            "Automates repetitive tasks.",
            "Processes large amounts of data.",
            "Can help people make informed decisions.",
            "Can improve productivity when used responsibly.",
        ]],
        bulletType="bullet",
        leftIndent=18,
    ),
    Paragraph("Conclusion", styles["SectionHeading"]),
    Paragraph(
        "Artificial Intelligence is changing many industries by helping people analyze "
        "information, automate workflows, and develop new services. Responsible design and "
        "human oversight remain important.",
        styles["BodyText"],
    ),
]

doc.build(story)
print(f"Created PDF: {output_path}")
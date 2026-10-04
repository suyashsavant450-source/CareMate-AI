from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm


def create_report_pdf(
    output_path,
    patient_name,
    report_text
):

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    normal_style = styles["BodyText"]
    normal_style.leading = 16

    document = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )

    story = []

    story.append(
        Paragraph(
            "CareMate AI",
            title_style
        )
    )

    story.append(
        Spacer(
            1,
            10
        )
    )

    story.append(
        Paragraph(
            f"Patient: {patient_name}",
            normal_style
        )
    )

    story.append(
        Spacer(
            1,
            10
        )
    )

    for paragraph in report_text.split("\n"):

        if paragraph.strip():

            story.append(
                Paragraph(
                    paragraph.replace(
                        "&",
                        "&amp;"
                    ),
                    normal_style
                )
            )

            story.append(
                Spacer(
                    1,
                    5
                )
            )

    story.append(
        Spacer(
            1,
            15
        )
    )

    story.append(
        Paragraph(
            "This document is for informational purposes "
            "and does not replace professional medical advice.",
            normal_style
        )
    )

    document.build(
        story
    )

    return output_path
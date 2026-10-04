import os
import uuid
from io import BytesIO

import streamlit as st

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import re

from database import get_connection
from ocr.extractor import extract_text

from ai.analyzer import (
    analyze_report,
    translate_analysis,
    create_voice_summary
)

from utils.helpers import get_user_id
from utils.tts import generate_speech


# =========================================================
# PDF CANVAS (HEADER, FOOTER & PAGE NUMBERING)
# =========================================================

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # Header Accent Bar & Text
        self.setFillColor(colors.HexColor("#0f172a"))
        self.rect(0, 800, 595.27, 42, fill=True, stroke=False)
        
        self.setFillColor(colors.HexColor("#38bdf8"))
        self.setFont("Helvetica-Bold", 12)
        self.drawString(45, 815, "CareMate AI")
        
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#94a3b8"))
        self.drawRightString(550, 815, "Simplified Medical Report")

        # Footer
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(45, 45, 550, 45)

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(45, 30, "Confidential • CareMate AI Patient Summary")
        self.drawRightString(550, 30, f"Page {self._pageNumber} of {page_count}")
        
        self.restoreState()


# =========================================================
# USER AUTHENTICATION
# =========================================================

user_id = get_user_id()


# =========================================================
# PAGE STYLING
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 85% 5%,
                rgba(37, 99, 235, 0.14),
                transparent 28%
            ),
            radial-gradient(
                circle at 10% 25%,
                rgba(6, 182, 212, 0.07),
                transparent 25%
            ),
            #07111F;
    }

    .main .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3, h4 {
        color: #F8FAFC !important;
    }

    p {
        color: #CBD5E1;
    }

    .stCaption {
        color: #94A3B8 !important;
    }

    div[data-testid="stFileUploader"] {
        background: #0D1B2D;
        border: 1px solid #28445E;
        border-radius: 16px;
        padding: 15px;
    }

    div[data-testid="stFileUploader"] * {
        color: #E2E8F0 !important;
    }

    div[data-baseweb="input"] {
        background: #0A1726 !important;
        border: 1px solid #294762 !important;
        border-radius: 10px !important;
    }

    div[data-baseweb="input"] input {
        color: #F8FAFC !important;
    }

    div[data-baseweb="select"] {
        background: #0A1726 !important;
        border-radius: 10px;
    }

    .stButton > button {
        background: #0D1C2D;
        color: #E2E8F0;
        border: 1px solid #28445E;
        border-radius: 11px;
        min-height: 44px;
        font-weight: 650;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background: #12304D;
        color: #FFFFFF;
        border-color: #38BDF8;
        box-shadow: 0 0 18px rgba(56, 189, 248, 0.12);
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(
            135deg,
            #2563EB,
            #0891B2
        );
        color: #FFFFFF;
        border: none;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.25);
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(
            135deg,
            #3B82F6,
            #06B6D4
        );
        color: #FFFFFF;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(
            145deg,
            #0D1B2D,
            #0A1726
        );
        border: 1px solid #1E344B;
        border-radius: 17px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.20);
    }

    [data-testid="stAlert"] {
        background: #0D2034 !important;
        border: 1px solid #234968 !important;
        color: #CBD5E1 !important;
        border-radius: 12px;
    }

    hr {
        border-color: #1E344B !important;
    }

    textarea {
        background: #0A1726 !important;
        color: #F8FAFC !important;
        border: 1px solid #294762 !important;
        border-radius: 11px !important;
    }

    .stMarkdown {
        color: #CBD5E1;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# PAGE HEADER
# =========================================================

st.markdown(
    "### 🤖 CareMate AI • Report Intelligence"
)

st.title("📄 Medical Reports")

st.write(
    "Upload your medical report and let CareMate AI "
    "explain it in simple, easy-to-understand language."
)

st.divider()


# =========================================================
# UPLOAD SECTION
# =========================================================

st.subheader("📤 Upload Medical Report")

st.caption(
    "Supported formats: PDF, JPG, JPEG and PNG • Maximum 10 MB"
)

uploaded_file = st.file_uploader(
    "Choose your medical report",
    type=["pdf", "jpg", "jpeg", "png"],
    key="medical_report_upload"
)


# =========================================================
# FILE SIZE CHECK
# =========================================================

if uploaded_file is not None:

    file_size_mb = uploaded_file.size / (1024 * 1024)

    if file_size_mb > 10:

        st.error(
            "File is too large. Please upload a file smaller than 10 MB."
        )

    else:

        # =================================================
        # ANALYZE BUTTON
        # =================================================

        if st.button(
            "🔍 Upload & Analyze Report",
            type="primary",
            use_container_width=True
        ):

            try:

                # -----------------------------------------
                # USER-SPECIFIC UPLOAD FOLDER
                # -----------------------------------------

                user_folder = os.path.join(
                    "uploads",
                    str(user_id)
                )

                os.makedirs(
                    user_folder,
                    exist_ok=True
                )

                # -----------------------------------------
                # UNIQUE FILE NAME
                # -----------------------------------------

                extension = os.path.splitext(
                    uploaded_file.name
                )[1].lower()

                unique_filename = (
                    f"{uuid.uuid4().hex}{extension}"
                )

                file_path = os.path.join(
                    user_folder,
                    unique_filename
                )

                # -----------------------------------------
                # SAVE FILE
                # -----------------------------------------

                with open(
                    file_path,
                    "wb"
                ) as file:

                    file.write(
                        uploaded_file.getbuffer()
                    )

                # -----------------------------------------
                # OCR / PDF EXTRACTION
                # -----------------------------------------

                with st.spinner(
                    "🔍 Reading your medical report..."
                ):

                    extracted_text = extract_text(
                        file_path
                    )

                # -----------------------------------------
                # EMPTY REPORT CHECK
                # -----------------------------------------

                if not extracted_text.strip():

                    st.error(
                        "No readable text was found in the report."
                    )

                    st.stop()

                # -----------------------------------------
                # AI ANALYSIS
                # -----------------------------------------

                with st.spinner(
                    "🤖 CareMate AI is analyzing your report..."
                ):

                    analysis = analyze_report(
                        extracted_text
                    )

                # -----------------------------------------
                # SAVE REPORT
                # -----------------------------------------

                connection = get_connection()

                cursor = connection.cursor()

                cursor.execute(
                    """
                    INSERT INTO medical_reports
                    (
                        user_id,
                        file_name,
                        report_text,
                        simplified_report
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        user_id,
                        uploaded_file.name,
                        extracted_text,
                        analysis
                    )
                )

                connection.commit()

                report_id = cursor.lastrowid

                connection.close()

                # -----------------------------------------
                # SESSION DATA
                # -----------------------------------------

                st.session_state.last_report_id = report_id

                st.session_state.last_report_text = (
                    extracted_text
                )

                st.session_state.report_analysis = (
                    analysis
                )

                st.session_state.report_language = (
                    "English"
                )

                st.session_state.translated_analysis = ""

                st.session_state.translated_language = ""

                st.session_state.voice_summary = ""

                st.session_state.voice_summary_language = ""

                st.success(
                    "✅ Report uploaded and analyzed successfully!"
                )

                st.rerun()

            except Exception as error:

                st.error(
                    f"❌ Something went wrong: {error}"
                )


# =========================================================
# CURRENT REPORT ANALYSIS
# =========================================================

analysis = st.session_state.get(
    "report_analysis"
)

report_text = st.session_state.get(
    "last_report_text"
)


if analysis:

    st.divider()

    st.subheader(
        "🤖 CareMate AI Explanation"
    )

    st.info(
        "This explanation is for understanding the report "
        "and does not replace professional medical advice."
    )


    # =====================================================
    # REPORT ACTION BUTTONS
    # =====================================================

    action_col1, action_col2 = st.columns(
        [1, 1]
    )

    with action_col1:

        # -------------------------------------------------
        # CREATE PREMIUM PDF
        # -------------------------------------------------

        pdf_buffer = BytesIO()

        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=A4,
            rightMargin=45,
            leftMargin=45,
            topMargin=60,
            bottomMargin=60
        )

        styles = getSampleStyleSheet()

        style_title = ParagraphStyle(
            'ReportTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=20,
            leading=24,
            textColor=colors.HexColor("#0f172a"),
            spaceAfter=4
        )

        style_subtitle = ParagraphStyle(
            'ReportSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#64748b"),
            spaceAfter=15
        )

        style_heading = ParagraphStyle(
            'SectionHeading',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=16,
            textColor=colors.HexColor("#0284c7"),
            spaceBefore=14,
            spaceAfter=6
        )

        style_body = ParagraphStyle(
            'ReportBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=15,
            textColor=colors.HexColor("#334155")
        )

        style_callout = ParagraphStyle(
            'CalloutText',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=14,
            textColor=colors.HexColor("#1e293b")
        )

        style_th = ParagraphStyle(
            'TableHeader',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9,
            leading=12,
            textColor=colors.white
        )

        style_td = ParagraphStyle(
            'TableCell',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor("#1e293b")
        )

        story = []

        # Document Header
        story.append(Paragraph("CareMate AI Medical Report Explanation", style_title))
        story.append(Paragraph("Simplified AI-Generated Patient Summary", style_subtitle))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=12))

        safe_text = (
            display_analysis
            if "display_analysis" in locals() and display_analysis
            else analysis
        )

        # Parse content into structured blocks, tables, and callouts
        lines = safe_text.split("\n")
        in_table = False
        table_data = []

        for line in lines:
            trimmed = line.strip()
            if not trimmed:
                continue

            # Parse Markdown Table
            if "|" in trimmed:
                if "---" in trimmed:
                    continue  # Separator line
                
                cols = [c.strip() for c in trimmed.split("|")[1:-1]]
                if cols:
                    if not in_table:
                        in_table = True
                        table_data = []
                    
                    formatted_cols = []
                    for c in cols:
                        c_formatted = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', c)
                        style_to_use = style_th if len(table_data) == 0 else style_td
                        formatted_cols.append(Paragraph(c_formatted, style_to_use))
                    
                    table_data.append(formatted_cols)
                continue
            else:
                if in_table and table_data:
                    t = Table(table_data, colWidths=[130, 90, 150, 134])
                    t.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                        ('TOPPADDING', (0, 0), (-1, -1), 6),
                        ('LEFTPADDING', (0, 0), (-1, -1), 8),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#f8fafc"), colors.white]),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                    ]))
                    story.append(Spacer(1, 6))
                    story.append(t)
                    story.append(Spacer(1, 10))
                    in_table = False
                    table_data = []

            # Headers
            if trimmed.startswith("**") and trimmed.endswith("**") and len(trimmed) < 40:
                header_title = trimmed.replace("**", "").title()
                story.append(Paragraph(header_title, style_heading))
            elif trimmed.startswith("#"):
                header_title = trimmed.lstrip("#").strip().title()
                story.append(Paragraph(header_title, style_heading))
            # Safety / Disclaimer Box
            elif "SAFETY NOTE" in trimmed.upper() or "DISCLAIMER" in trimmed.upper():
                box_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', trimmed)
                p_box = Paragraph(f"<b>⚠️ Note:</b> {box_text}", style_callout)
                box_table = Table([[p_box]], colWidths=[504])
                box_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#fef2f2")),
                    ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#fca5a5")),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('LEFTPADDING', (0, 0), (-1, -1), 10),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ]))
                story.append(Spacer(1, 8))
                story.append(box_table)
                story.append(Spacer(1, 8))
            else:
                formatted_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', trimmed)
                if formatted_text.startswith("- ") or formatted_text.startswith("* "):
                    formatted_text = f"• {formatted_text[2:]}"
                
                story.append(Paragraph(formatted_text, style_body))
                story.append(Spacer(1, 4))

        if in_table and table_data:
            t = Table(table_data, colWidths=[130, 90, 150, 134])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#f8fafc"), colors.white]),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ]))
            story.append(Spacer(1, 6))
            story.append(t)
            story.append(Spacer(1, 10))

        doc.build(story, canvasmaker=NumberedCanvas)

        pdf_buffer.seek(0)

        st.download_button(
            "⬇️ Download Simplified Report",
            data=pdf_buffer,
            file_name="CareMate_AI_Simplified_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    with action_col2:

        # -------------------------------------------------
        # CLOSE REPORT
        # -------------------------------------------------

        if st.button(
            "✕ Close Report",
            use_container_width=True
        ):

            st.session_state.last_report_id = None

            st.session_state.last_report_text = None

            st.session_state.report_analysis = None

            st.session_state.report_language = (
                "English"
            )

            st.session_state.translated_analysis = ""

            st.session_state.translated_language = ""

            st.session_state.voice_summary = ""

            st.session_state.voice_summary_language = ""

            st.rerun()


    st.divider()


    # =====================================================
    # LANGUAGE SELECTION
    # =====================================================

    st.markdown(
        "#### 🌐 Explanation Language"
    )

    language = st.selectbox(
        "Choose language",
        [
            "English",
            "Marathi",
            "Hindi",
            "Kannada"
        ],
        key="report_language"
    )


    # =====================================================
    # ENGLISH
    # =====================================================

    if language == "English":

        display_analysis = analysis


    # =====================================================
    # OTHER LANGUAGES
    # =====================================================

    else:

        already_translated = (
            st.session_state.get(
                "translated_language"
            ) == language
        )

        if not already_translated:

            if st.button(
                f"🌐 Explain in {language}",
                use_container_width=True
            ):

                try:

                    with st.spinner(
                        f"Translating explanation to {language}..."
                    ):

                        translated = translate_analysis(
                            analysis,
                            language
                        )

                    st.session_state.translated_analysis = (
                        translated
                    )

                    st.session_state.translated_language = (
                        language
                    )

                    st.session_state.voice_summary = ""

                    st.session_state.voice_summary_language = ""

                    st.rerun()

                except Exception as error:

                    st.error(
                        f"Translation failed: {error}"
                    )

        display_analysis = st.session_state.get(
            "translated_analysis",
            ""
        )

        if not display_analysis:

            st.info(
                f"Click 'Explain in {language}' "
                f"to view the explanation in {language}."
            )


    # =====================================================
    # DISPLAY AI ANALYSIS
    # =====================================================

    if display_analysis:

        st.markdown(
            display_analysis
        )

        st.divider()


        # =================================================
        # SHORT VOICE SUMMARY
        # =================================================

        st.subheader(
            "🔊 Listen to Important Summary"
        )

        st.caption(
            "CareMate AI speaks only the most important findings "
            "in approximately 30–45 seconds."
        )

        if st.button(
            "🔊 Generate Voice Summary",
            use_container_width=True
        ):

            try:

                # -----------------------------------------
                # CREATE SHORT SUMMARY
                # -----------------------------------------

                with st.spinner(
                    "🤖 Preparing important findings..."
                ):

                    voice_summary = create_voice_summary(
                        report_text
                    )

                # -----------------------------------------
                # TRANSLATE SHORT SUMMARY
                # -----------------------------------------

                if language != "English":

                    with st.spinner(
                        f"🌐 Preparing voice summary in {language}..."
                    ):

                        voice_summary = translate_analysis(
                            voice_summary,
                            language
                        )

                # -----------------------------------------
                # STORE SUMMARY
                # -----------------------------------------

                st.session_state.voice_summary = (
                    voice_summary
                )

                st.session_state.voice_summary_language = (
                    language
                )

                # -----------------------------------------
                # DISPLAY SUMMARY
                # -----------------------------------------

                st.success(
                    "✅ Short voice summary is ready!"
                )

                st.markdown(
                    "#### 🗣️ CareMate AI will say:"
                )

                st.info(
                    voice_summary
                )

                # -----------------------------------------
                # GENERATE AUDIO
                # -----------------------------------------

                with st.spinner(
                    "🔊 Generating voice..."
                ):

                    audio_bytes = generate_speech(
                        voice_summary,
                        language
                    )

                st.audio(
                    audio_bytes,
                    format="audio/mp3"
                )

            except Exception as error:

                st.error(
                    f"❌ Voice generation failed: {error}"
                )


# =========================================================
# EXTRACTED TEXT
# =========================================================

if report_text:

    st.divider()

    with st.expander(
        "📝 View Extracted Medical Information"
    ):

        st.text_area(
            "OCR Extracted Text",
            report_text,
            height=350,
            disabled=True
        )


# =========================================================
# PREVIOUS REPORTS
# =========================================================

st.divider()

st.subheader(
    "📚 Previous Reports"
)


connection = get_connection()

cursor = connection.cursor()

cursor.execute(
    """
    SELECT
        id,
        file_name,
        uploaded_at,
        report_text,
        simplified_report
    FROM medical_reports
    WHERE user_id = ?
    ORDER BY uploaded_at DESC
    """,
    (user_id,)
)

reports = cursor.fetchall()

connection.close()


# =========================================================
# NO REPORTS
# =========================================================

if not reports:

    st.info(
        "No medical reports uploaded yet."
    )


# =========================================================
# REPORT LIST
# =========================================================

else:

    for report in reports:

        with st.container(
            border=True
        ):

            col1, col2 = st.columns(
                [5, 1]
            )

            with col1:

                st.markdown(
                    f"### 📄 {report['file_name']}"
                )

                st.caption(
                    f"Uploaded: {report['uploaded_at']}"
                )

            with col2:

                if st.button(
                    "View",
                    key=f"view_{report['id']}"
                ):

                    st.session_state.last_report_id = (
                        report["id"]
                    )

                    st.session_state.last_report_text = (
                        report["report_text"]
                    )

                    st.session_state.report_analysis = (
                        report["simplified_report"]
                    )

                    st.session_state.report_language = (
                        "English"
                    )

                    st.session_state.translated_analysis = ""

                    st.session_state.translated_language = ""

                    st.session_state.voice_summary = ""

                    st.session_state.voice_summary_language = ""

                    st.rerun()


# =========================================================
# SECURITY NOTE
# =========================================================

st.divider()

st.caption(
    "🔐 Your medical reports are stored under your "
    "personal CareMate AI account."
)
import os

from pypdf import PdfReader
import pytesseract

from PIL import Image


TESSERACT_PATH = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


if os.path.exists(TESSERACT_PATH):

    pytesseract.pytesseract.tesseract_cmd = (
        TESSERACT_PATH
    )


def extract_text_from_pdf(file_path):

    try:

        reader = PdfReader(file_path)

        extracted_text = []

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:

                extracted_text.append(
                    page_text
                )

        return "\n".join(
            extracted_text
        ).strip()

    except Exception as error:

        raise Exception(
            f"PDF extraction failed: {error}"
        )


def extract_text_from_image(file_path):

    try:

        image = Image.open(
            file_path
        ).convert("RGB")

        text = pytesseract.image_to_string(
            image
        )

        return text.strip()

    except pytesseract.TesseractNotFoundError:

        raise Exception(
            "Tesseract OCR is not installed "
            "or the path is incorrect."
        )

    except Exception as error:

        raise Exception(
            f"Image OCR failed: {error}"
        )


def extract_text(file_path):

    extension = os.path.splitext(
        file_path
    )[1].lower()

    if extension == ".pdf":

        return extract_text_from_pdf(
            file_path
        )

    if extension in [
        ".jpg",
        ".jpeg",
        ".png"
    ]:

        return extract_text_from_image(
            file_path
        )

    raise ValueError(
        "Unsupported file format. "
        "Use PDF, JPG, JPEG or PNG."
    )
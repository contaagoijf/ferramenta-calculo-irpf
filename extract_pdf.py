import pathlib
import PyPDF2

pdf_path = pathlib.Path(r"c:\Users\c4c\Downloads\1-PRD_gpt_lovable.pdf")
reader = PyPDF2.PdfReader(str(pdf_path))
print("pages", len(reader.pages))
for i, page in enumerate(reader.pages):
    text = page.extract_text() or ""
    print("--- page", i + 1, "---")
    print(text[:5000])
    print()

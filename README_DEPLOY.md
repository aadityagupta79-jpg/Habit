# Kruti Dev 010 Image → DOCX — Deployment Ready

## What this does
Mobile-friendly web interface for:
- Hindi → Kruti Dev 010, 14 pt
- English → Times New Roman, 12 pt
- Mixed Hindi/English font separation
- Multiple images in original order
- Complete paper-by-paper processing
- Optional source-image preservation
- Word OMML equation objects
- DOCX download

## Deploy on Render
1. Create a Render account.
2. Create a new Web Service from this project/repository.
3. Build command:
   `apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-hin && pip install -r requirements.txt`
4. Start command:
   `gunicorn app:app`
5. Deploy.
6. Open the generated `https://...onrender.com` URL on your Android phone.

## Important
The current equation recognizer is OCR/heuristic based. For very complex equations, connect Mathpix or a local Pix2Text/Pix2Tex model to supply accurate LaTeX before OMML conversion. Do not put API keys into frontend code.

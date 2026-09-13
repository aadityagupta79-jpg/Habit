# Kruti Dev 010 Image → DOCX — Render Fixed Version

## Why this version
Render's normal Python build environment does not allow the `apt-get` command used by the earlier version. This version uses a Dockerfile, so Tesseract Hindi/English OCR is installed inside the container.

## Render
- Create a Web Service from the GitHub repository.
- Runtime: Docker (Render detects `Dockerfile`).
- Dockerfile: `./Dockerfile`
- Docker Context: `.`
- No custom Build Command is needed.
- Start Command can be left blank because the Dockerfile starts Gunicorn.
- Free plan is fine for testing.

## Features
Hindi: Kruti Dev 010 / 14 pt
English: Times New Roman / 12 pt
Mixed Hindi/English fonts
Paper-by-paper processing
Optional source image preservation
Word OMML equation objects
DOCX download

For complex equations, a dedicated equation OCR engine such as Pix2Text/Mathpix should be integrated for high recognition accuracy.

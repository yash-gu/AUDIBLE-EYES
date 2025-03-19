# Audible Eyes

Audible Eyes is a simple Python application that converts PDF documents into audio files using Google Text-to-Speech (gTTS). The application provides a graphical user interface (GUI) built with Tkinter, allowing users to select a PDF file, choose a language, and generate an MP3 audio file.

## Features
- Extracts text from a PDF file.
- Converts extracted text into speech using gTTS.
- Allows users to select from multiple languages.
- Provides an intuitive GUI for ease of use.
- Scrollable UI for better accessibility.

## Requirements
To run Audible Eyes, you need to have the following dependencies installed:

- Python 3.x
- `tkinter` (comes with Python standard library)
- `Pillow` (for image processing)
- `PyPDF2` (for extracting text from PDFs)
- `gtts` (Google Text-to-Speech)

Install the required dependencies using:
```sh
pip install pillow pypdf2 gtts
```

## Installation & Usage
1. Clone the repository or download the source code.
   ```sh
   git clone https://github.com/your-username/audible-eyes.git
   cd audible-eyes
   ```
2. Run the application using:
   ```sh
   python app.py
   ```
3. Select a PDF file by clicking the **Browse** button.
4. Choose the destination to save the audio file.
5. Select a language for speech synthesis.
6. Click the **Convert** button to generate an MP3 file.

## Supported Languages
Audible Eyes supports multiple languages for text-to-speech conversion, including:
- English (en)
- Hindi (hi)
- Bengali (bn)
- Tamil (ta)
- Telugu (te)
- Marathi (mr)
- Gujarati (gu)
- Urdu (ur)
- Kannada (kn)
- Malayalam (ml)
- Sanskrit (sa)

## Screenshots
![Audible Eyes UI](screenshot.png)

## File Structure
```
Audible-Eyes/
│── app.py          # Main application script
│── README.md       # Documentation
│── logo.jpg        # Application logo (if applicable)
│── requirements.txt # List of dependencies
```

## License
This project is licensed under the MIT License.

## Author
Developed by YASH GUPTA.

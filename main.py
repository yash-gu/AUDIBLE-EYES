import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  
import PyPDF2
from gtts import gTTS

def pdf_to_audio(pdf_file, audio_file, lang):
    try:
        with open(pdf_file, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'
            
            if not text.strip():
                messagebox.showwarning("Warning", "No text found in the PDF.")
                return
    except FileNotFoundError:
        messagebox.showerror("Error", f"The file '{pdf_file}' was not found.")
        return
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading the PDF: {e}")
        return

    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(audio_file)
        messagebox.showinfo("Success", f"Audio file saved as '{audio_file}'")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while converting to audio: {e}")

def select_pdf():
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    pdf_entry.delete(0, tk.END)
    pdf_entry.insert(0, pdf_path)

def save_audio():
    audio_path = filedialog.asksaveasfilename(defaultextension=".mp3",
                                                filetypes=[("MP3 Files", "*.mp3")])
    audio_entry.delete(0, tk.END)
    audio_entry.insert(0, audio_path)

def convert():
    pdf_file = pdf_entry.get()
    audio_file = audio_entry.get()
    lang = language_var.get()
    
    if not pdf_file or not audio_file:
        messagebox.showwarning("Input Error", "Please select both PDF and output audio file paths.")
        return
    pdf_to_audio(pdf_file, audio_file, lang)


root = tk.Tk()
root.title("Audible Eyes")
root.geometry("400x1000")
root.configure(bg="#E8F5E9")

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(frame, bg="#E8F5E9")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)

inner_frame = tk.Frame(canvas, bg="#E8F5E9")
canvas.create_window((0, 0), window=inner_frame, anchor="nw")

def configure_scroll_region(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

inner_frame.bind("<Configure>", configure_scroll_region)

logo_path = "logo.jpg"  
try:
    logo_image = Image.open(logo_path)
    logo_image = logo_image.resize((125, 125))  
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(inner_frame, image=logo_photo, bg="#E8F5E9")
    logo_label.pack(pady=2)
except Exception as e:
    messagebox.showerror("Error", f"Could not load logo: {e}")

tk.Label(inner_frame, text="Select PDF File:", bg="#E8F5E9", font=("Helvetica", 10, "bold")).pack(pady=1)
pdf_entry = tk.Entry(inner_frame, width=50, font=("Helvetica", 10), bd=2, relief="solid")
pdf_entry.pack(pady=0.25)
tk.Button(inner_frame, text="Browse", command=select_pdf, bg="#4CAF50", fg="white", font=("Helvetica", 10), borderwidth=0).pack(pady=5)

tk.Label(inner_frame, text="Save Audio File As:", bg="#E8F5E9", font=("Helvetica", 10, "bold")).pack(pady=1)
audio_entry = tk.Entry(inner_frame, width=50, font=("Helvetica", 10), bd=2, relief="solid")
audio_entry.pack(pady=0.25)
tk.Button(inner_frame, text="Browse", command=save_audio, bg="#4CAF50", fg="white", font=("Helvetica", 10), borderwidth=0).pack(pady=5)

tk.Label(inner_frame, text="Select Language:", bg="#E8F5E9", font=("Helvetica", 10, "bold")).pack(pady=0.25)
language_var = tk.StringVar(value='en')  
lang_options = {
    'English': 'en',             
    'Hindi': 'hi',
    'Bengali': 'bn',             
    'Tamil': 'ta',
    'Telugu': 'te',
    'Marathi': 'mr',
    'Gujarati': 'gu',
    'Urdu': 'ur',
    'Kannada': 'kn',
    'Malayalam': 'ml',
    'Sanskrit': 'sa'  
}

for lang_name, lang_code in lang_options.items():
    tk.Radiobutton(inner_frame, text=lang_name, variable=language_var, value=lang_code, bg="#E8F5E9", font=("Helvetica", 10)).pack(anchor=tk.W)

tk.Button(inner_frame, text="Convert", command=convert, bg="#2196F3", fg="white", font=("Helvetica", 10, "bold"), borderwidth=0).pack(pady=1)

footer = tk.Label(inner_frame, text="© 2024 Audible Eyes", bg="#E8F5E9", font=("Helvetica", 8))
footer.pack(side=tk.BOTTOM, pady=1)

root.mainloop()


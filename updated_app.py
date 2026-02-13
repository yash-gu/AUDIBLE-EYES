import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk  
import PyPDF2
from gtts import gTTS
from pydub import AudioSegment
import threading
import os
import re

class AudibleEyesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audible Eyes - Improved")
        self.root.geometry("550x950")
        self.root.configure(bg="#E8F5E9")
        self.conversion_thread = None
        self.is_converting = False
        self.setup_ui()
    
    def setup_ui(self):
        """Build the user interface"""
        main_frame = tk.Frame(self.root, bg="#E8F5E9")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollable canvas
        canvas = tk.Canvas(main_frame, bg="#E8F5E9", highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.inner_frame = tk.Frame(canvas, bg="#E8F5E9")
        canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        self.inner_frame.bind("<Configure>", configure_scroll_region)
        
        # Logo
        self.setup_logo()
        
        # Title
        tk.Label(self.inner_frame, text="Audible Eyes", bg="#E8F5E9", 
                font=("Helvetica", 18, "bold"), fg="#1976D2").pack(pady=10)
        
        # PDF Selection
        tk.Label(self.inner_frame, text="Select PDF File:", bg="#E8F5E9", 
                font=("Helvetica", 11, "bold"), fg="#1976D2").pack(pady=(15, 8), anchor=tk.W, padx=30)
        self.pdf_entry = tk.Entry(self.inner_frame, width=55, font=("Helvetica", 10), 
                                   bd=2, relief="solid", bg="white")
        self.pdf_entry.pack(pady=5, padx=30)
        tk.Button(self.inner_frame, text="Browse PDF", command=self.select_pdf, 
                 bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"), 
                 borderwidth=0, padx=15, pady=6).pack(pady=5)
        
        # Audio Output
        tk.Label(self.inner_frame, text="Save Audio File As:", bg="#E8F5E9", 
                font=("Helvetica", 11, "bold"), fg="#1976D2").pack(pady=(15, 8), anchor=tk.W, padx=30)
        self.audio_entry = tk.Entry(self.inner_frame, width=55, font=("Helvetica", 10), 
                                     bd=2, relief="solid", bg="white")
        self.audio_entry.pack(pady=5, padx=30)
        tk.Button(self.inner_frame, text="Browse Output", command=self.save_audio, 
                 bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"), 
                 borderwidth=0, padx=15, pady=6).pack(pady=5)
        
        # Language Selection
        tk.Label(self.inner_frame, text="Select Language:", bg="#E8F5E9", 
                font=("Helvetica", 11, "bold"), fg="#1976D2").pack(pady=(15, 10), anchor=tk.W, padx=30)
        self.language_var = tk.StringVar(value='en')
        
        lang_options = {
            'English': 'en', 'Hindi': 'hi', 'Bengali': 'bn', 'Tamil': 'ta', 
            'Telugu': 'te', 'Marathi': 'mr', 'Gujarati': 'gu', 'Urdu': 'ur', 
            'Kannada': 'kn', 'Malayalam': 'ml', 'Sanskrit': 'sa'
        }
        
        lang_frame = tk.Frame(self.inner_frame, bg="#E8F5E9")
        lang_frame.pack(padx=30, pady=5, fill=tk.X)
        
        for idx, (lang_name, lang_code) in enumerate(lang_options.items()):
            tk.Radiobutton(lang_frame, text=lang_name, variable=self.language_var, 
                          value=lang_code, bg="#E8F5E9", font=("Helvetica", 10)).grid(
                          row=idx//2, column=idx%2, sticky=tk.W, padx=10, pady=3)
        
        # Progress Bar
        tk.Label(self.inner_frame, text="Conversion Progress:", bg="#E8F5E9", 
                font=("Helvetica", 11, "bold"), fg="#1976D2").pack(pady=(15, 8), anchor=tk.W, padx=30)
        
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(self.inner_frame, variable=self.progress_var, 
                                            maximum=100, mode='determinate', length=450)
        self.progress_bar.pack(pady=5, padx=30)
        
        self.progress_percent_label = tk.Label(self.inner_frame, text="0%", bg="#E8F5E9", 
                                                font=("Helvetica", 9, "bold"))
        self.progress_percent_label.pack(pady=5)
        
        self.status_label = tk.Label(self.inner_frame, text="Ready to convert", bg="#E8F5E9", 
                                      font=("Helvetica", 9), fg="#666666", wraplength=450)
        self.status_label.pack(pady=5, padx=30, fill=tk.X)
        
        # Convert Button
        self.convert_button = tk.Button(self.inner_frame, text="Convert to Audio", 
                                        command=self.convert_threaded, bg="#2196F3", fg="white", 
                                        font=("Helvetica", 12, "bold"), borderwidth=0, padx=50, pady=12)
        self.convert_button.pack(pady=20)
        
        # Footer
        tk.Label(self.inner_frame, text="© 2024 Audible Eyes", bg="#E8F5E9", 
                font=("Helvetica", 8, "italic"), fg="#999999").pack(side=tk.BOTTOM, pady=10)
    
    def setup_logo(self):
        """Load logo or show placeholder"""
        logo_path = "logo.jpg"
        if os.path.exists(logo_path):
            try:
                logo_image = Image.open(logo_path)
                logo_image = logo_image.resize((120, 120))
                self.logo_photo = ImageTk.PhotoImage(logo_image)
                tk.Label(self.inner_frame, image=self.logo_photo, bg="#E8F5E9").pack(pady=10)
                return
            except:
                pass
        
        # Fallback
        tk.Label(self.inner_frame, text="[AUDIO]", bg="#E8F5E9", 
                font=("Helvetica", 40, "bold"), fg="#2196F3").pack(pady=10)
    
    def select_pdf(self):
        """Select PDF file"""
        pdf_path = filedialog.askopenfilename(title="Select PDF", filetypes=[("PDF Files", "*.pdf")])
        if pdf_path:
            self.pdf_entry.delete(0, tk.END)
            self.pdf_entry.insert(0, pdf_path)
    
    def save_audio(self):
        """Select audio output path"""
        audio_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 Files", "*.mp3")])
        if audio_path:
            self.audio_entry.delete(0, tk.END)
            self.audio_entry.insert(0, audio_path)
    
    def show_status(self, message):
        """Update status message"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def update_progress(self, value):
        """Update progress bar"""
        self.progress_var.set(value)
        self.progress_percent_label.config(text=f"{int(value)}%")
        self.root.update_idletasks()
    
    def extract_pdf_text(self, pdf_file):
        """Extract text from PDF with progress updates"""
        try:
            with open(pdf_file, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ''
                total_pages = len(reader.pages)
                
                for i, page in enumerate(reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            page_text = re.sub(r'\s+', ' ', page_text)
                            text += page_text + '\n'
                    except:
                        continue
                    
                    progress = (i + 1) / total_pages * 40
                    self.update_progress(progress)
                    self.show_status(f"Extracting... Page {i+1}/{total_pages}")
                
                if not text.strip():
                    return None, "No text found in PDF"
                return text, None
        
        except FileNotFoundError:
            return None, f"PDF not found: {pdf_file}"
        except Exception as e:
            return None, f"Error reading PDF: {str(e)}"
    
    def split_text_for_gtts(self, text, max_chars=4800):
        """Split text into chunks for gTTS (handles large PDFs)"""
        if len(text) <= max_chars:
            return [text]
        
        chunks = []
        sentences = re.split(r'(?<=[.!?])\s+', text)
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 1 <= max_chars:
                current_chunk += sentence + " "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + " "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks if chunks else [text]
    
    def convert_to_audio(self, text, audio_file, lang):
        """Convert text to audio with chunking and combining"""
        try:
            chunks = self.split_text_for_gtts(text)
            audio_segments = []
            
            for i, chunk in enumerate(chunks):
                if not chunk.strip():
                    continue
                
                self.update_progress(40 + (i / len(chunks)) * 40)
                self.show_status(f"Converting part {i+1}/{len(chunks)}...")
                
                try:
                    tts = gTTS(text=chunk, lang=lang, slow=False)
                    segment_file = f"temp_segment_{i}.mp3"
                    tts.save(segment_file)
                    audio_segments.append(segment_file)
                except Exception as e:
                    for seg in audio_segments:
                        if os.path.exists(seg):
                            os.remove(seg)
                    return f"Error converting: {str(e)}"
            
            if not audio_segments:
                return "No audio segments created"
            
            self.update_progress(80)
            self.show_status("Combining audio segments...")
            
            if len(audio_segments) > 1:
                try:
                    combined_audio = AudioSegment.from_file(audio_segments[0], format="mp3")
                    for segment_file in audio_segments[1:]:
                        audio = AudioSegment.from_file(segment_file, format="mp3")
                        combined_audio += audio
                    combined_audio.export(audio_file, format="mp3")
                except Exception as e:
                    return f"Error combining: {str(e)}"
            else:
                try:
                    os.rename(audio_segments[0], audio_file)
                except Exception as e:
                    return f"Error saving: {str(e)}"
            
            self.show_status("Cleaning up...")
            for segment_file in audio_segments:
                try:
                    if os.path.exists(segment_file):
                        os.remove(segment_file)
                except:
                    pass
            
            return None
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def convert_threaded(self):
        """Run conversion in thread (prevent GUI freeze)"""
        if self.is_converting:
            messagebox.showwarning("In Progress", "Conversion already in progress!")
            return
        
        pdf_file = self.pdf_entry.get().strip()
        audio_file = self.audio_entry.get().strip()
        lang = self.language_var.get()
        
        if not pdf_file or not audio_file:
            messagebox.showwarning("Input Error", "Please select PDF and output path")
            return
        
        if not os.path.exists(pdf_file):
            messagebox.showerror("Error", f"PDF not found: {pdf_file}")
            return
        
        if not pdf_file.lower().endswith('.pdf'):
            messagebox.showerror("Error", "Please select a PDF file")
            return
        
        self.is_converting = True
        self.convert_button.config(state=tk.DISABLED, text="Converting...")
        self.progress_var.set(0)
        self.show_status("Starting conversion...")
        
        thread = threading.Thread(target=self.convert_process, args=(pdf_file, audio_file, lang), daemon=True)
        thread.start()
    
    def convert_process(self, pdf_file, audio_file, lang):
        """Main conversion process (runs in thread)"""
        try:
            text, error = self.extract_pdf_text(pdf_file)
            if error:
                messagebox.showerror("Extraction Error", error)
                return
            
            error = self.convert_to_audio(text, audio_file, lang)
            if error:
                messagebox.showerror("Conversion Error", error)
                return
            
            self.update_progress(100)
            self.show_status("Conversion completed successfully!")
            messagebox.showinfo("Success", f"Audio saved!\n\nLocation:\n{audio_file}")
        
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"Error: {str(e)}")
        
        finally:
            self.is_converting = False
            self.convert_button.config(state=tk.NORMAL, text="Convert to Audio")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = AudibleEyesApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
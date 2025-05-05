import tkinter as tk
from tkinter import filedialog, messagebox
from transformers import pipeline
import PyPDF2

def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        messagebox.showerror("Error", f"Error reading text file: {e}")
        return None

def read_pdf_file(file_path):
    try:
        pdf_reader = PyPDF2.PdfReader(file_path)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        messagebox.showerror("Error", f"Error reading PDF file: {e}")
        return None

def summarize_text(text):
    try:
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        messagebox.showinfo("Processing", "Summarizing... Please wait.")
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        messagebox.showerror("Error", f"Error summarizing text: {e}")
        return None

def browse_file():
    file_path = filedialog.askopenfilename(
        title="Select a text or PDF file",
        filetypes=[("Text files", "*.txt"), ("PDF files", "*.pdf")]
    )
    if file_path:
        if file_path.lower().endswith('.txt'):
            content = read_text_file(file_path)
        elif file_path.lower().endswith('.pdf'):
            content = read_pdf_file(file_path)
        else:
            messagebox.showerror("Unsupported", "Only .txt and .pdf files are supported.")
            return

        if content:
            if len(content) > 3000:
                messagebox.showinfo("Note", "Large file detected; summarizing the first 3000 characters.")
                content = content[:3000]

            summary = summarize_text(content)
            if summary:
                text_output.delete(1.0, tk.END)
                text_output.insert(tk.END, summary)

def save_summary():
    summary_text = text_output.get(1.0, tk.END).strip()
    if not summary_text:
        messagebox.showwarning("No Summary", "There is no summary to save.")
        return
    save_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")]
    )
    if save_path:
        try:
            with open(save_path, 'w', encoding='utf-8') as file:
                file.write(summary_text)
            messagebox.showinfo("Saved", f"Summary saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving summary: {e}")

# GUI Setup
root = tk.Tk()
root.title("AI Text & PDF Summarizer")
root.geometry("600x400")

browse_button = tk.Button(root, text="Select File", command=browse_file)
browse_button.pack(pady=10)

text_output = tk.Text(root, wrap=tk.WORD, height=15, width=70)
text_output.pack(pady=10)

save_button = tk.Button(root, text="Save Summary", command=save_summary)
save_button.pack(pady=5)

root.mainloop()

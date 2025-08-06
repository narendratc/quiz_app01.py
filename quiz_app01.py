import tkinter as tk
from tkinter import messagebox
import requests
import html
import random

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Quiz App")
        self.root.geometry("600x400")

        self.qn = 0
        self.score = 0

        self.questions = self.get_questions()

        self.question_label = tk.Label(root, text="", font=("Arial", 16), wraplength=500)
        self.question_label.pack(pady=30)

        self.options = []
        for i in range(4):
            btn = tk.Button(root, text="", font=("Arial", 14), width=30, command=lambda i=i: self.check_answer(i))
            btn.pack(pady=5)
            self.options.append(btn)

        self.load_question()

    def get_questions(self):
        url = "https://opentdb.com/api.php?amount=5&category=9&difficulty=easy&type=multiple"
        try:
            response = requests.get(url)
            data = response.json()

            question_list = []
            for item in data['results']:
                q_text = html.unescape(item['question'])
                correct = html.unescape(item['correct_answer'])
                options = item['incorrect_answers']
                options = [html.unescape(opt) for opt in options]
                options.append(correct)
                random.shuffle(options)

                question_list.append({
                    "question": q_text,
                    "options": options,
                    "answer": correct
                })

            return question_list
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load questions: {e}")
            self.root.destroy()

    def load_question(self):
        if self.qn < len(self.questions):
            q = self.questions[self.qn]
            self.question_label.config(text=f"Q{self.qn + 1}: {q['question']}")
            for i in range(4):
                self.options[i].config(text=q["options"][i])
        else:
            messagebox.showinfo("Quiz Completed", f"Your Score: {self.score}/{len(self.questions)}")
            self.root.destroy()

    def check_answer(self, i):
        selected = self.options[i].cget("text")
        correct = self.questions[self.qn]["answer"]
        if selected == correct:
            self.score += 1
        self.qn += 1
        self.load_question()

# Run the app
if __name__ == "__main__":
    try:
        import requests
    except ImportError:
        print("Please install the 'requests' module using: pip install requests")
    else:
        root = tk.Tk()
        app = QuizApp(root)
        root.mainloop()

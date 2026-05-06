import tkinter as tk
from tkinter import ttk, messagebox

class LegalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("نظام الإدارة القانونية - التأمينات والمعاشات")
        self.root.geometry("900x500")

        # العنوان الرئيسي
        header = tk.Label(root, text="إدارة القضايا والتظلمات القانونية", font=("Arial", 18, "bold"), bg="#2c3e50", fg="white")
        header.pack(fill=tk.X)

        # إطار إدخال البيانات
        frame = tk.Frame(root, pady=20)
        frame.pack()

        tk.Label(frame, text="رقم القضية:").grid(row=0, column=5, padx=5)
        self.case_num = tk.Entry(frame)
        self.case_num.grid(row=0, column=4, padx=5)

        tk.Label(frame, text="اسم صاحب الشأن:").grid(row=0, column=3, padx=5)
        self.member_name = tk.Entry(frame)
        self.member_name.grid(row=0, column=2, padx=5)

        tk.Label(frame, text="نوع النزاع:").grid(row=0, column=1, padx=5)
        self.case_type = ttk.Combobox(frame, values=["صرف معاش", "ضم مدة", "إصابة عمل", "أخرى"])
        self.case_type.grid(row=0, column=0, padx=5)

        # زر الإضافة
        btn_add = tk.Button(root, text="تسجيل قضية جديدة", command=self.add_case, bg="#27ae60", fg="white", width=20)
        btn_add.pack(pady=10)

        # جدول العرض
        self.tree = ttk.Treeview(root, columns=("Status", "Type", "Name", "ID"), show='headings')
        self.tree.heading("Status", text="الموقف الحالي")
        self.tree.heading("Type", text="نوع القضية")
        self.tree.heading("Name", text="اسم صاحب الشأن")
        self.tree.heading("ID", text="رقم القضية")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def add_case(self):
        if self.case_num.get() == "" or self.member_name.get() == "":
            messagebox.showwarning("تنبيه", "يرجى ملء البيانات الأساسية")
            return
        
        # إضافة البيانات للجدول مؤقتاً
        self.tree.insert("", tk.END, values=("قيد النظر", self.case_type.get(), self.member_name.get(), self.case_num.get()))
        messagebox.showinfo("تم", "تم تسجيل البيانات بنجاح")

if __name__ == "__main__":
    root = tk.Tk()
    app = LegalApp(root)
    root.mainloop()

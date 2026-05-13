def clean_arabic_text(text):
    # دالة بسيطة لتنظيف النص من المسافات الغريبة والحروف المقطعة
    if not text: return ""
    return " ".join(text.split())

def search_legal_files(query):
    legal_files = ["law.pdf", "regulation.pdf", "guide.pdf"]
    findings = []
    # تنظيف كلمة البحث
    query = clean_arabic_text(query)
    
    for file_name in legal_files:
        try:
            with pdfplumber.open(file_name) as pdf:
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    text = clean_arabic_text(text)
                    if query in text:
                        pos = text.find(query)
                        context = text[max(0, pos-200):min(len(text), pos+500)]
                        findings.append({"file": file_name, "page": i+1, "content": context})
                        if len(findings) >= 5: return findings
        except: continue
    return findings

def search_pdfs(query):
    files = ["law.pdf", "regulation.pdf", "guide.pdf"]
    all_results = []
    # تنظيف الكلمة المبحوث عنها
    search_term = query.strip()
    
    for file_path in files:
        try:
            with pdfplumber.open(file_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        # تحسين البحث ليتجاهل المسافات الزائدة والحركات
                        if search_term in text or search_term.replace(" ", "") in text.replace(" ", ""):
                            # تحديد مكان الكلمة لجلب السياق
                            idx = text.find(search_term) if search_term in text else text.replace(" ", "").find(search_term.replace(" ", ""))
                            start = max(0, idx - 150)
                            end = min(len(text), idx + 500)
                            
                            all_results.append({
                                "file": file_path.replace(".pdf", "").upper(),
                                "page": i + 1,
                                "content": text[start:end]
                            })
                            # نكتفي بأول 5 نتائج لسرعة الأداء
                            if len(all_results) > 5: return all_results
        except Exception as e:
            continue 
    return all_results

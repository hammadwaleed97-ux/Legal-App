import streamlit as st
import pdfplumber

# 1. التنسيق البصري المعتمد
st.set_page_config(page_title="المستشار القانوني الذكي", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%); }
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; color: white; }
    .program-title { text-align: center; color: #facc15; font-size: 2.8rem; font-weight: bold; line-height: 1.1; margin-bottom: 10px; }
    .signature-section { text-align: center; font-size: 1.4rem; line-height: 1.5; margin-bottom: 30px; color: #ffffff; font-weight: bold; }
    .result-card { background-color: #ffffff; border-radius: 15px; padding: 25px; color: #1e293b; border-right: 12px solid #facc15; margin-top: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.3); }
    .file-tag { background-color: #f1f5f9; padding: 5px 12px; border-radius: 8px; color: #b91c1c; font-weight: bold; font-size: 0.9rem; }
    </style>
    """, unsafe_allow_html=True)

# 2. الواجهة الرئيسية
st.markdown('<div class="program-title">مستشارك<br>في<br>التأمينات<br>و<br>المعاشات</div>', unsafe_allow_html=True)
st.markdown('<div class="signature-section">مع تحيات / وليد حماد<br>الادارة العامة للشؤون القانونية<br>ديوان عام منطقة البحيرة</div>', unsafe_allow_html=True)
st.divider()

# 3. دالة البحث داخل الـ PDF
def search_pdfs(query):
    # نحدد الملفات التي رفعتها أنت على GitHub
    files = ["law.pdf", "regulation.pdf", "guide.pdf"]
    all_results = []
    
    for file_path in files:
        try:
            with pdfplumber.open(file_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text and query in text:
                        # استخراج النص المحيط بالكلمة المبحوث عنها
                        start = max(0, text.find(query) - 150)
                        end = min(len(text), text.find(query) + 400)
                        all_results.append({
                            "file": file_path.replace(".pdf", "").upper(),
                            "page": i + 1,
                            "content": text[start:end]
                        })
        except:
            continue # يتخطى الملف إذا لم يجد الاسم مطابقاً
    return all_results

# 4. خانة البحث
user_input = st.text_area("اطرح إشكالك القانوني هنا:", placeholder="اكتب سؤالك هنا أو الإشكال القانوني...", height=100)

if st.button("تحليل الإشكالية والبحث في المراجع 🔍"):
    if user_input:
        with st.spinner('جاري فحص المراجع القانونية...'):
            hits = search_pdfs(user_input)
            if hits:
                for hit in hits:
                    st.markdown(f"""
                    <div class="result-card">
                        <span class="file-tag">المرجع: {hit['file']} - صفحة: {hit['page']}</span>
                        <p style="font-size: 1.25rem; line-height: 1.7; margin-top:15px;">
                            "... {hit['content']} ..."
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("لم نجد هذا النص في القانون أو اللائحة حالياً. تأكد من دقة الكلمات.")
    else:
        st.warning("يرجى كتابة السؤال أولاً.")

import streamlit as st
import pdfplumber

# 1. إعدادات الصفحة والتصميم المبسط
st.set_page_config(page_title="مستشارك التأميني", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .main-title { text-align: center; color: #1e3a8a; font-size: 2rem; font-weight: bold; }
    .card { background-color: #f8fafc; border-right: 5px solid #facc15; padding: 15px; margin-bottom: 10px; color: #334155; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">مستشارك في التأمينات والمعاشات</div>', unsafe_allow_html=True)
st.write(f"<p style='text-align:center;'>إعداد/ وليد حماد - الإدارة العامة للشؤون القانونية بالبحيرة</p>", unsafe_allow_html=True)

# 2. محرك بحث خفيف وسريع
def search_in_pdfs(query):
    files = ["law.pdf", "regulation.pdf", "guide.pdf"]
    results = []
    for file_name in files:
        try:
            with pdfplumber.open(file_name) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text and query in text:
                        # استخراج جزء صغير من النص للسرعة
                        start_idx = text.find(query)
                        excerpt = text[max(0, start_idx-100):min(len(text), start_idx+300)]
                        results.append({"file": file_name, "page": page_num + 1, "text": excerpt})
                        if len(results) > 3: return results # نكتفي بـ 3 نتائج فقط للسرعة القصوى
        except: continue
    return results

# 3. واجهة البحث البسيطة
query = st.text_input("اكتب كلمة للبحث (مثلاً: الشيخوخة أو وفاة):")

if st.button("بحث 🔍"):
    if query:
        with st.spinner("جاري استخراج المعلومة..."):
            data = search_in_pdfs(query)
            if data:
                for item in data:
                    st.markdown(f"""
                    <div class="card">
                        <b>المرجع: {item['file']} | صفحة: {item['page']}</b><br>
                        <p>{item['text']}...</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("لم نجد نتائج، حاول تقليل كلمات البحث.")
    else:
        st.info("يرجى كتابة كلمة أولاً.")

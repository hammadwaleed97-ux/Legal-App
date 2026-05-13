import streamlit as st
import pdfplumber

# 1. التنسيق البصري الفخم لديوان عام منطقة البحيرة
st.set_page_config(page_title="المستشار القانوني الذكي", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%); }
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; color: white; }
    .program-title { text-align: center; color: #facc15; font-size: 2.5rem; font-weight: bold; line-height: 1.2; margin-bottom: 5px; }
    .signature-section { text-align: center; font-size: 1.2rem; line-height: 1.4; margin-bottom: 20px; color: #ffffff; }
    .result-card { background-color: #ffffff; border-radius: 12px; padding: 20px; color: #1e293b; border-right: 10px solid #facc15; margin-top: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .status-msg { background-color: rgba(250, 204, 21, 0.2); border-radius: 8px; padding: 10px; text-align: center; margin: 10px 0; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="program-title">مستشارك في التأمينات والمعاشات</div>', unsafe_allow_html=True)
st.markdown('<div class="signature-section">مع تحيات / وليد حماد<br>الادارة العامة للشؤون القانونية - منطقة البحيرة</div>', unsafe_allow_html=True)

# 2. دالة البحث المطورة لسرعة الاستجابة
def fast_search(query):
    # أسماء الملفات التي رفعتها أنت بنجاح
    files = ["law.pdf", "regulation.pdf", "guide.pdf"]
    results = []
    
    for file_path in files:
        try:
            with pdfplumber.open(file_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text and query in text:
                        # جلب النص المحيط بالكلمة
                        idx = text.find(query)
                        start = max(0, idx - 150)
                        end = min(len(text), idx + 400)
                        results.append({
                            "source": file_path.replace(".pdf", "").upper(),
                            "page": i + 1,
                            "content": text[start:end]
                        })
                        # جلب أول نتيجتين فقط من كل ملف لضمان السرعة وعدم توقف التطبيق
                        if len(results) >= 6: return results
        except: continue
    return results

# 3. واجهة البحث
search_input = st.text_input("ادخل المادة أو الموضوع القانوني (مثال: عجز، وفاة، سن):")

if st.button("بدء البحث في المراجع القانونية 🔍"):
    if search_input:
        with st.spinner('جاري قراءة المراجع...'):
            found_data = fast_search(search_input)
            if found_data:
                for item in found_data:
                    st.markdown(f"""
                    <div class="result-card">
                        <p style="color: #b91c1c; font-weight: bold;">📍 المرجع: {item['source']} | صفحة: {item['page']}</p>
                        <p style="font-size: 1.1rem; line-height: 1.6;">"... {item['content']} ..."</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ لم يتم العثور على نتائج دقيقة لهذه الكلمة. جرب كلمة أخرى مثل 'الشيخوخة' أو 'إصابة'.")
    else:
        st.info("قم بكتابة كلمة للبحث أولاً.")

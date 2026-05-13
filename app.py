import streamlit as st
import pdfplumber

# 1. إعدادات الواجهة الرسمية للهيئة القومية للتأمين الاجتماعي - منطقة البحيرة
st.set_page_config(page_title="المستشار القانوني - وليد حماد", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .main-title { text-align: center; color: #1e3a8a; font-size: 2.2rem; font-weight: bold; margin-bottom: 0px; }
    .sub-title { text-align: center; color: #64748b; font-size: 1.1rem; margin-bottom: 20px; }
    .result-box { background-color: #ffffff; border-right: 8px solid #facc15; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 15px; color: #1e293b; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">مستشارك في التأمينات والمعاشات</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">إعداد الأستاذ/ وليد حماد<br>الشؤون القانونية - ديوان عام منطقة البحيرة</div>', unsafe_allow_html=True)

# 2. محرك البحث السريع
def search_legal_files(query):
    # الأسماء التي رفعتها أنت في GitHub
    legal_files = ["law.pdf", "regulation.pdf", "guide.pdf"]
    findings = []
    
    for file_name in legal_files:
        try:
            with pdfplumber.open(file_name) as pdf:
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text and query in text:
                        pos = text.find(query)
                        # جلب نص مختصر حول كلمة البحث
                        context = text[max(0, pos-150):min(len(text), pos+400)]
                        findings.append({"file": file_name, "page": i+1, "content": context})
                        # نكتفي بـ 3 نتائج فقط لضمان السرعة ومنع التهنيج
                        if len(findings) >= 3: return findings
        except: continue
    return findings

# 3. خانة البحث والتنفيذ
user_query = st.text_input("أدخل موضوع البحث (مثال: المعاش المبكر، العجز، الشيخوخة):")

if st.button("استخراج النص القانوني 🔍"):
    if user_query:
        with st.spinner("جاري فحص المراجع القانونية..."):
            results = search_legal_files(user_query)
            if results:
                for item in results:
                    st.markdown(f"""
                    <div class="result-box">
                        <span style="color: #b91c1c; font-weight: bold;">📍 المرجع: {item['file'].upper()} | صفحة: {item['page']}</span><br>
                        <p style="margin-top: 10px; line-height: 1.6;">"... {item['content']} ..."</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("لم يتم العثور على نتائج دقيقة. تأكد من كتابة الكلمة بشكل صحيح (مثال: 'الشيخوخة' بدلاً من 'شيخوخه').")
    else:
        st.info("من فضلك اكتب كلمة للبحث عنها أولاً.")

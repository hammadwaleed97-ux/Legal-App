import streamlit as st
import pdfplumber
import google.generativeai as genai

# الربط بمفتاحك الشخصي
genai.configure(api_key="AIzaSyCck8uvMFNFrOePBOYGTLrabPR369BXnHI")

st.set_page_config(page_title="المستشار القانوني الذكي", layout="wide")

# تنسيق المذكرة القانونية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .stApp { background-color: #f8fafc; }
    .main-card { background: white; padding: 25px; border-radius: 15px; border-top: 10px solid #1e3a8a; box-shadow: 0 4px 6px rgba(0,0,0,0.1); color: #1e293b; }
    .header-text { text-align: center; color: #1e3a8a; font-size: 2.3rem; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.markdown('<div class="header-text">المستشار القانوني الرقمي الذكي</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color: #64748b;">إعداد الأستاذ/ وليد حماد - الإدارة العامة للشؤون القانونية بالبحيرة</p>', unsafe_allow_html=True)

# دالة البحث في القوانين المرفوعة
def search_laws(query):
    context = ""
    for f in ["law.pdf", "regulation.pdf"]:
        try:
            with pdfplumber.open(f) as pdf:
                for page in pdf.pages[:20]:
                    text = page.extract_text()
                    if text and query[:3] in text: context += text + "\n"
                    if len(context) > 3000: break
        except: continue
    return context[:3000]

# خانة البحث (فاضية تماماً زي ما طلبت)
user_q = st.text_area("اطرح تساؤلك القانوني أو الحالة المراد فحصها هنا:", height=150)

if st.button("صياغة الرد القانوني ⚖️"):
    if user_q:
        with st.spinner("جاري المراجعة..."):
            try:
                ref = search_laws(user_q)
                # استخدام الموديل الأحدث لتفادي أخطاء v1beta
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"أنت مستشار قانوني مصري. بناءً على: {ref}. أجب على: {user_q}. ابدأ بـ 'بالإشارة إلى التساؤل المطروح..' واختم بـ 'مع تحيات وليد حماد - منطقة البحيرة'."
                
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.markdown(f'<div style="background:white; padding:20px; border-right:8px solid #facc15; line-height:2; font-size:1.2rem; color:#1e293b;">{response.text}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error("جوجل مشغولة ثواني، دوس على الزرار تاني وهتشتغل.")
    else:
        st.warning("اكتب السؤال الأول يا فندم.")

st.markdown('</div>', unsafe_allow_html=True)

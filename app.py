import streamlit as st
import google.generativeai as genai

# الربط بالمفتاح من الخزنة السرية اللي إنت عملتها
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.set_page_config(page_title="المستشار القانوني", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .main-card { background: white; padding: 25px; border-radius: 15px; border-top: 10px solid #1e3a8a; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.markdown('<h1 style="text-align:center; color:#1e3a8a;">المستشار القانوني الرقمي الذكي</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-weight:bold;">إشراف الأستاذ/ وليد حماد - منطقة البحيرة</p>', unsafe_allow_html=True)

user_q = st.text_area("اكتب تساؤلك القانوني هنا:", height=150)

if st.button("صياغة الرد القانوني ⚖️"):
    if user_q:
        with st.spinner("جاري الصياغة..."):
            try:
                # هذا السطر هو الحل النهائي لخطأ 404
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"أنت مستشار قانوني مصري خبير. صِغ رداً قانونياً مفصلاً على: {user_q}. ابدأ بـ 'بالإشارة إلى التساؤل المطروح..' واختم بـ 'مع تحيات وليد حماد - منطقة البحيرة'."
                
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.markdown(f'<div style="line-height:2; font-size:1.2rem; white-space: pre-wrap; color:#1e293b;">{response.text}</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"تنبيه تقني: {str(e)}")
    else:
        st.warning("يرجى كتابة السؤال أولاً.")

st.markdown('</div>', unsafe_allow_html=True)

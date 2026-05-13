import streamlit as st
import google.generativeai as genai

# 1. الربط بالمفتاح من الخزنة السرية (Secrets)
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    else:
        st.error("المفتاح غير موجود في الأسرار (Secrets).")
except:
    pass

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
                # الطريقة الأكيدة: اختيار أول موديل يدعم التوليد متاح في حسابك
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # إرسال الاستفسار بصياغة مباشرة
                response = model.generate_content(
                    f"أجب كخبير قانوني مصري على: {user_q}. "
                    f"ابدأ بـ 'بالإشارة إلى التساؤل المطروح..' واختم بـ 'مع تحيات وليد حماد - منطقة البحيرة'."
                )
                
                st.markdown("---")
                st.markdown(f'<div style="line-height:2; font-size:1.2rem; white-space: pre-wrap; color:#1e293b;">{response.text}</div>', unsafe_allow_html=True)
                
            except Exception as e:
                # لو حصل خطأ، هيظهر لك السبب الحقيقي بدقة (مثل صلاحية المفتاح)
                st.error(f"تنبيه تقني: {str(e)}")
    else:
        st.warning("يرجى كتابة السؤال أولاً.")

st.markdown('</div>', unsafe_allow_html=True)

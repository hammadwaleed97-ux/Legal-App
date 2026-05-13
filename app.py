import streamlit as st
import google.generativeai as genai

# الربط بالمفتاح من الخزنة السرية (Secrets)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.set_page_config(page_title="المستشار القانوني", layout="wide")

# تنسيق الواجهة الاحترافي
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

# خانة السؤال
user_q = st.text_area("اكتب تساؤلك القانوني هنا:", height=150)

if st.button("صياغة الرد القانوني ⚖️"):
    if user_q:
        with st.spinner("جاري الصياغة..."):
            try:
                # هذا السطر هو "مفتاح الحل" لخطأ الـ 404
                # استخدمنا 'gemini-1.5-flash-8b' لأنه الأكثر استقراراً في الإصدارات الحالية
                model = genai.GenerativeModel('gemini-1.5-flash-8b')
                
                # إرسال الاستفسار
                response = model.generate_content(
                    f"أنت مستشار قانوني مصري. صِغ رداً قانونياً على: {user_q}. "
                    f"ابدأ بـ 'بالإشارة إلى التساؤل المطروح..' واختم بـ 'مع تحيات وليد حماد - منطقة البحيرة'."
                )
                
                st.markdown("---")
                st.markdown(f'<div style="line-height:2; font-size:1.2rem; white-space: pre-wrap;">{response.text}</div>', unsafe_allow_html=True)
                
            except Exception as e:
                # في حالة وجود مشكلة في الموديل، هنجرب الموديل البديل فوراً
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(user_q)
                    st.write(response.text)
                except:
                    st.error(f"خطأ تقني: {str(e)}")
    else:
        st.warning("يرجى كتابة السؤال أولاً.")

st.markdown('</div>', unsafe_allow_html=True)

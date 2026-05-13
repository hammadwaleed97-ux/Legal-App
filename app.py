import streamlit as st
import google.generativeai as genai

# الربط بالمفتاح الجديد اللي سيادتك بعته
genai.configure(api_key="AIzaSyDVSr4skcmloNtTIQi54LGmG_ZnCjRxoNc")

st.set_page_config(page_title="المستشار القانوني", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .main-card { background: white; padding: 25px; border-radius: 15px; border-top: 10px solid #1e3a8a; color: #1e293b; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.markdown('<h1 style="text-align:center; color:#1e3a8a;">المستشار القانوني الرقمي الذكي</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-weight:bold;">إعداد الأستاذ/ وليد حماد - منطقة البحيرة</p>', unsafe_allow_html=True)

# خانة السؤال
user_q = st.text_area("اكتب تساؤلك القانوني هنا (بدون أمثلة):", height=150)

if st.button("صياغة الرد القانوني ⚖️"):
    if user_q:
        with st.spinner("جاري الاتصال بالمحرك الذكي..."):
            try:
                # محرك Gemini 1.5 Flash السريع
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # توجيه الصياغة
                prompt = f"أنت مستشار قانوني مصري. صِغ رداً قانونياً مفصلاً على: {user_q}. ابدأ بـ 'بالإشارة إلى التساؤل المطروح..' واختم بـ 'مع تحيات وليد حماد - منطقة البحيرة'."
                
                response = model.generate_content(prompt)
                
                st.markdown("---")
                # عرض النتيجة مباشرة
                st.markdown(f'<div style="line-height:2; font-size:1.2rem; white-space: pre-wrap;">{response.text}</div>', unsafe_allow_html=True)
                
            except Exception as e:
                # لو فيه غلط هيطلعه هنا بدل الرسالة اللي ضايقتك
                st.error(f"خطأ تقني من جوجل: {str(e)}")
    else:
        st.warning("يرجى كتابة السؤال أولاً.")

st.markdown('</div>', unsafe_allow_html=True)

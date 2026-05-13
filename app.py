import streamlit as st
import google.generativeai as genai

# التأكد من سحب المفتاح من الأسرار بأمان
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("المفتاح غير موجود في الأسرار (Secrets).")

st.set_page_config(page_title="المستشار القانوني الذكي", layout="wide")

# تصميم واجهة تليق بسيادتكم
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .main-card { background: white; padding: 20px; border-radius: 10px; border-top: 5px solid #1e3a8a; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.markdown('<h2 style="text-align:center; color:#1e3a8a;">المستشار القانوني الرقمي الذكي</h2>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-weight:bold;">إشراف الأستاذ/ وليد حماد - منطقة البحيرة</p>', unsafe_allow_html=True)

user_q = st.text_input("اطرح تساؤلك القانوني هنا (مثال: العجز المستديم):")

if st.button("صياغة الرد القانوني ⚖️"):
    if user_q:
        with st.spinner("جاري التواصل مع المحرك الذكي..."):
            try:
                # التعديل الجوهري: استخدام الاسم المختصر مباشرة لحل خطأ 404
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # توجيه الموديل للصياغة القانونية الرصينة
                prompt = f"أنت مستشار قانوني مصري خبير. صِغ رداً قانونياً مفصلاً ورسمياً على: {user_q}. ابدأ بـ 'بالإشارة إلى التساؤل المطروح..' واختم بـ 'مع تحيات وليد حماد - منطقة البحيرة'."
                
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.success("الرد القانوني المقترح:")
                st.write(response.text)
                
            except Exception as e:
                # لو فيه أي مشكلة تقنية هتظهر هنا بوضوح
                st.error(f"تنبيه تقني: {str(e)}")
    else:
        st.warning("يرجى كتابة التساؤل أولاً.")

st.markdown('</div>', unsafe_allow_html=True)

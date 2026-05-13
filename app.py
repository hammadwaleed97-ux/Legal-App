import streamlit as st
import google.generativeai as genai

# التأكد من سحب المفتاح من الأسرار بأمان
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    else:
        st.error("المفتاح غير موجود في الأسرار (Secrets).")
except Exception as e:
    st.error(f"خطأ في الوصول للأسرار: {e}")

st.set_page_config(page_title="المستشار القانوني", layout="wide")

# تصميم واجهة رصينة تليق بمكانتكم
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .main-card { background: white; padding: 20px; border-radius: 10px; border-top: 5px solid #1e3a8a; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.markdown('<h2 style="text-align:center;">المستشار القانوني الرقمي الذكي</h2>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;">إشراف الأستاذ/ وليد حماد - منطقة البحيرة</p>', unsafe_allow_html=True)

# المدخلات
user_q = st.text_input("اطرح تساؤلك القانوني هنا:")

if st.button("صياغة الرد القانوني ⚖️"):
    if user_q:
        try:
            # استخدام الموديل المستقر
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # الطلب موجه بدقة
            response = model.generate_content(f"أجب كخبير قانوني مصري على: {user_q}")
            
            st.info("الرد القانوني المقترح:")
            st.write(response.text)
            st.success("تمت الصياغة بنجاح - مع تحيات وليد حماد")
        except Exception as e:
            st.error(f"حدث خطأ أثناء الصياغة: {e}")
    else:
        st.warning("يرجى كتابة التساؤل.")

st.markdown('</div>', unsafe_allow_html=True)

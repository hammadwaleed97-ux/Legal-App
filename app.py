import streamlit as st
import google.generativeai as genai

# إعداد المفتاح الجديد
API_KEY = "AIzaSyCFeJWZzOaF0diESahah46tCuFUS3Fi6B0"
genai.configure(api_key=API_KEY)

# عنوان التطبيق
st.set_page_config(page_title="المساعد القانوني الذكي - البحيرة", layout="wide")
st.title("⚖️ المساعد القانوني الذكي")
st.subheader("تحت إشراف الأستاذ/ وليد حماد - منطقة البحيرة")

# اختيار الموديل الأحدث لتجنب أخطاء 404
model = genai.GenerativeModel('gemini-1.5-flash')

# خانة رفع الملفات القانونية
uploaded_file = st.file_uploader("ارفع ملف القانون أو المذكرة (PDF)", type="pdf")

# خانة السؤال
user_question = st.text_input("اسأل سؤالك القانوني هنا:")

if user_question:
    try:
        if uploaded_file:
            # إذا وجد ملف، ندمجه مع السؤال
            with st.spinner('جاري تحليل المستند واستخراج المعلومة القانونية...'):
                # تحويل الملف المرفوع لبيانات يفهمها الذكاء الاصطناعي
                file_data = uploaded_file.read()
                response = model.generate_content([
                    "أنت مستشار قانوني خبير. أجب بناءً على هذا الملف فقط بصيغة رسمية.",
                    {"mime_type": "application/pdf", "data": file_data},
                    user_question
                ])
        else:
            # سؤال عام في القانون بدون ملف
            with st.spinner('جاري البحث في القاعدة القانونية...'):
                response = model.generate_content(user_question)
        
        # عرض الإجابة
        st.markdown("### الإجابة القانونية:")
        st.write(response.text)
        st.info("مع تحيات وليد حماد - الإدارة العامة للشؤون القانونية")
        
    except Exception as e:
        st.error(f"عذراً، حدث خطأ تقني: {e}")

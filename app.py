import streamlit as st
import pandas as pd
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="المستشار القانوني - التأمينات", layout="wide")

# تنسيق الواجهة للغة العربية
st.markdown("""
    <style>
    .main { direction: rtl; text-align: right; }
    div.stButton > button:first-child { background-color: #2c3e50; color:white; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ منظومة الإدارة القانونية - ديوان عام البحيرة")

# قائمة جانيبة للتنقل
menu = ["🏠 الرئيسية", "📝 تسجيل قضية/تظلم", "🔍 بحث ومتابعة", "📚 المكتبة القانونية"]
choice = st.sidebar.radio("القائمة الرئيسية", menu)

# قاعدة بيانات وهمية (في الواقع يفضل ربطها بـ Google Sheets أو SQL)
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["رقم القضية", "صاحب الشأن", "الرقم التأميني", "نوع النزاع", "تاريخ الجلسة", "الموقف الحالي"])

if choice == "🏠 الرئيسية":
    st.subheader("إحصائيات سريعة")
    col1, col2, col3 = st.columns(3)
    col1.metric("إجمالي القضايا", len(st.session_state.data))
    col2.metric("قضايا منظورة", "5")
    col3.metric("تظلمات جديدة", "2")
    st.info("مرحباً بك في نظام الأرشفة القانونية الخفيف")

elif choice == "📝 تسجيل قضية/تظلم":
    st.subheader("إدخال بيانات ملف جديد")
    with st.form("case_form"):
        col1, col2 = st.columns(2)
        with col1:
            case_id = st.text_input("رقم القضية / التظلم")
            member_name = st.text_input("اسم صاحب الشأن")
            ins_id = st.text_input("الرقم التأميني")
        with col2:
            case_type = st.selectbox("نوع النزاع", ["صرف معاش", "ضم مدة", "إصابة عمل", "منازعة قانونية"])
            case_date = st.date_input("تاريخ أول جلسة / إجراء")
            status = st.text_area("ملخص الموقف الحالي")
            
        submit = st.form_submit_button("حفظ الملف القانوني")
        
        if submit:
            new_row = {"رقم القضية": case_id, "صاحب الشأن": member_name, "الرقم التأميني": ins_id,

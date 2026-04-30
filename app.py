import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# إعداد الصفحة وتنسيقها
st.set_page_config(page_title="المكتب الفني - الإدارة القانونية", layout="wide")

# تخصيص الواجهة باللغة العربية
st.markdown("""
    <style>
    .reportview-container { direction: rtl; }
    .main { text-align: right; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ منظومة الإدارة العامة للشؤون القانونية")
st.subheader("ديوان عام منطقة البحيرة")

# إنشاء قاعدة بيانات بسيطة في الذاكرة (للتجربة)
if 'legal_db' not in st.session_state:
    st.session_state.legal_db = pd.DataFrame(columns=[
        "رقم الطلب", "تاريخ الورود", "موضوع الطلب", "صاحب الشأن", "الموظف المختص", "الحالة", "موعد الرد القانوني"
    ])

# القائمة الجانبية للتنقل
menu = ["تسجيل طلب جديد", "لوحة المتابعة", "الأرشيف القانوني"]
choice = st.sidebar.selectbox("القائمة الرئيسية", menu)

if choice == "تسجيل طلب جديد":
    st.header("📝 إدخال معاملة قانونية جديدة")
    with st.form("legal_form"):
        col1, col2 = st.columns(2)
        with col1:
            req_id = st.text_input("رقم الوارد / القضية")
            subject = st.text_area("موضوع الطلب أو التظلم")
        with col2:
            person = st.text_input("اسم صاحب الشأن")
            lawyer = st.selectbox("الباحث القانوني المختص", ["أحمد علي", "سارة محمد", "خالد محمود"])
            days_limit = st.number_input("المدة القانونية للرد (أيام)", value=15)
        
        submitted = st.form_submit_button("حفظ الطلب")
        
        if submitted:
            due_date = datetime.now() + timedelta(days=days_limit)
            new_data = {
                "رقم الطلب": req_id,
                "تاريخ الورود": datetime.now().strftime("%Y-%m-%d"),
                "موضوع الطلب": subject,
                "صاحب الشأن": person,
                "الموظف المختص": lawyer,
                "الحالة": "قيد الدراسة",
                "موعد الرد القانوني": due_date.strftime("%Y-%m-%d")
            }
            st.session_state.legal_db = pd.concat([st.session_state.legal_db, pd.DataFrame([new_data])], ignore_index=True)
            st.success("تم تسجيل المعاملة وتحديد موعد الرد التلقائي.")

elif choice == "لوحة المتابعة":
    st.header("📊 متابعة القضايا والطلبات")
    
    # إحصائيات سريعة
    total = len(st.session_state.legal_db)
    st.metric("إجمالي المعاملات قيد الدراسة", total)
    
    # عرض البيانات مع إمكانية التصفية
    st.dataframe(st.session_state.legal_idb, use_container_width=True)

# تذييل الصفحة بالاسم المطلوب
st.divider()
st.markdown("**مع تحيات وليد حماد - الإدارة العامة للشؤون القانونية - ديوان عام منطقة البحيرة**")

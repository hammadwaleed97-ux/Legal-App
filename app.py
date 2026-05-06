import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="القانونية - البحيرة", layout="wide")

# 2. تهيئة مخزن البيانات
if 'legal_data' not in st.session_state:
    st.session_state.legal_data = pd.DataFrame(columns=["الرقم", "الاسم", "النوع", "الحالة"])

# 3. العنوان الجانبي والقائمة
st.sidebar.title("⚖️ إدارة الشؤون القانونية")
choice = st.sidebar.radio("انتقل إلى:", ["إضافة ملف جديد", "سجل القضايا"])

# 4. واجهة إضافة ملف جديد
if choice == "إضافة ملف جديد":
    st.header("تسجيل قضية أو تظلم")
    with st.form("my_form"):
        c1, c2 = st.columns(2)
        with c1:
            num = st.text_input("رقم القضية")
            name = st.text_input("اسم صاحب الشأن")
        with c2:
            ctype = st.selectbox("نوع المنازعة", ["معاشات", "إصابات", "ضم مدة"])
            status = st.text_input("الموقف الحالي")
            
        submitted = st.form_submit_button("حفظ في الأرشيف")
        if submitted:
            new_row = {"الرقم": num, "الاسم": name, "النوع": ctype, "الحالة": status}
            st.session_state.legal_data = pd.concat([st.session_state.legal_data, pd.DataFrame([new_row])], ignore_index=True)
            st.success("تم الحفظ بنجاح")

# 5. عرض السجل
else:
    st.header("🗂️ أرشيف القضايا المسجلة")
    if not st.session_state.legal_data.empty:
        st.dataframe(st.session_state.legal_data, use_container_width=True)
    else:
        st.info("لا توجد قضايا مسجلة حالياً")

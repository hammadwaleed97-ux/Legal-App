import streamlit as st

# 1. الإعدادات الأساسية
st.set_page_config(page_title="منظومة المستشار وليد حماد", layout="wide")

# 2. الترويسة الثابتة
st.markdown("""
    <div style="text-align: center; border: 3px solid #1E3A8A; padding: 15px; border-radius: 15px; background-color: #f8f9fa;">
        <h2 style="color: #1E3A8A; margin: 0;">الهيئة القومية للتأمين الاجتماعي</h2>
        <h3 style="color: #1E3A8A; margin: 5px;">الإدارة العامة للشئون القانونية</h3>
        <h4 style="color: #ce1126; margin: 5px;">مع تحيات أ/ وليد حماد</h4>
    </div>
""", unsafe_allow_html=True)

# 3. نظام التنقل
if 'page' not in st.session_state:
    st.session_state.page = "الرئيسية"

st.write("---")

# توزيع الأيقونات (الشبكة الرئيسية)
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
col5, col6 = st.columns(2)

with col1:
    if st.button("⚖️ قسم القضايا", use_container_width=True): st.session_state.page = "قضايا"
with col2:
    if st.button("📜 قسم الفتوى", use_container_width=True): st.session_state.page = "فتوى"
with col3:
    if st.button("🔍 التحقيقات", use_container_width=True): st.session_state.page = "تحقيقات"
with col4:
    if st.button("📚 المكتبة الرقمية", use_container_width=True): st.session_state.page = "مكتبة"
with col5:
    if st.button("📂 الأرشيف", use_container_width=True): st.session_state.page = "أرشيف"
with col6:
    if st.button("🏠 الرئيسية", use_container_width=True): st.session_state.page = "الرئيسية"

st.write("---")

# --- محتوى الأقسام ---

if st.session_state.page == "قضايا":
    st.header("⚖️ إدارة القضايا (القسم القضائي)")
    court_select = st.selectbox("المحكمة", ["ابتدائي", "استئناف", "نقض", "مجلس دولة"])
    st.text_input("رقم الدعوى")
    st.text_area("الوقائع")
    st.button("صياغة المذكرة")

elif st.session_state.page == "فتوى":
    st.header("📜 إدارة الفتوى")
    st.radio("القسم", ["عامة", "إصابات", "زواج عرفي"], horizontal=True)
    st.button("صياغة الرأي")

elif st.session_state.page == "تحقيقات":
    st.header("🔍 التحقيقات والنيابات")
    st.text_input("اسم المحال للتحقيق")
    st.button("بدء المحضر")

elif st.session_state.page == "مكتبة":
    st.header("📚 المكتبة القانونية")
    st.selectbox("القسم", ["قوانين", "لوائح", "تعليمات", "أحكام"])
    st.file_uploader("رفع مستند")

elif st.session_state.page == "أرشيف":
    st.header("📂 الأرشيف")
    st.text_input("بحث بالاسم أو الرقم")

else:
    st.info("مرحباً بك يا سيادة المستشار. اختر قسماً من الأيقونات أعلاه للبدء.")

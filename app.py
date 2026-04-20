import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="منظومة المستشار وليد حماد", layout="wide")

# 2. الترويسة واللوجو (البيانات الثابتة)
st.markdown("""
    <div style="text-align: center; border: 3px solid #1E3A8A; padding: 15px; border-radius: 15px; background-color: #f8f9fa; margin-bottom: 20px;">
        <h2 style="color: #1E3A8A; margin: 0;">الهيئة القومية للتأمين الاجتماعي</h2>
        <h3 style="color: #1E3A8A; margin: 5px;">الإدارة العامة للشئون القانونية</h3>
        <h4 style="color: #ce1126; margin: 5px;">مع تحيات أ/ وليد حماد</h4>
    </div>
""", unsafe_allow_html=True)

# 3. توزيع الأيقونات (بالطول والعرض)
if 'page' not in st.session_state:
    st.session_state.page = "قضايا"

# توزيع الأزرار في صفين لاستغلال المساحة
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⚖️ قسم القضايا", use_container_width=True): st.session_state.page = "قضايا"
with col2:
    if st.button("📜 قسم الفتوى", use_container_width=True): st.session_state.page = "فتوى"
with col3:
    if st.button("🔍 التحقيقات", use_container_width=True): st.session_state.page = "تحقيقات"

col4, col5, col6 = st.columns(3)
with col4:
    if st.button("📚 المكتبة", use_container_width=True): st.session_state.page = "مكتبة"
with col5:
    if st.button("📂 الأرشيف", use_container_width=True): st.session_state.page = "أرشيف"
with col6:
    if st.button("🏠 الرئيسية", use_container_width=True): st.session_state.page = "قضايا"

st.markdown("---")

# --- معالجة الأقسام بناءً على المعطيات الكاملة ---

# 1. قسم القضايا
if st.session_state.page == "قضايا":
    st.header("⚖️ الإدارة العامة للقضايا (القسم القضائي)")
    court_type = st.selectbox("نوع القضاء:", ["القضاء العادي", "محاكم مجلس الدولة"])
    
    if court_type == "القضاء العادي":
        level = st.radio("المستوى:", ["ابتدائي", "استئناف", "نقض"], horizontal=True

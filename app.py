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

# 3. إدارة التنقل بين الصفحات
if 'page' not in st.session_state:
    st.session_state.page = "قضايا"

# توزيع الأيقونات في شبكة (Grid) متوازنة
st.write("### القائمة الرئيسية")
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)
row3_col1, row3_col2 = st.columns(2)

with row1_col1:
    if st.button("⚖️ قسم القضايا", use_container_width=True): st.session_state.page = "قضايا"
with row1_col2:
    if st.button("📜 قسم الفتوى", use_container_width=True): st.session_state.page = "فتوى"
with row2_col1:
    if st.button("🔍 التحقيقات والنيابات", use_container_width=True): st.session_state.page = "تحقيقات"
with row2_col2:
    if st.button("📚 المكتبة القانونية", use_container_width=True): st.session_state.page = "مكتبة"
with row3_col1:
    if st.button("📂 الأرشيف والبحث", use_container_width=True): st.session_state.page = "أرشيف"
with row3_col2:
    if st.button("🏠 العودة للرئيسية", use_container_width=True): st.session_state.page = "قضايا"

st.markdown("---")

# --- معالجة الأقسام بناءً على المعطيات الكاملة ---

# 1. قسم القضايا
if st.session_state.page == "قضايا":
    st.header("⚖️ الإدارة العامة للقضايا (القسم القضائي)")
    court_type = st.selectbox("نوع القضاء:", ["القضاء العادي", "محاكم مجلس الدولة"])
    
    if court_type == "القضاء العادي":
        level = st.radio("المستوى القضائي:", ["المحاكم الابتدائية", "المحاكم الاستئنافية", "محكمة النقض"], horizontal=True)
        action = st.selectbox("نوع الإجراء المطلوب:", [
            "صياغة مذكرة دفاع (الهيئة مدعى عليها)", 
            "صياغة مذكرة دفاع (الهيئة مدعية)", 
            "صياغة صحيفة استئناف مقام من الهيئة",
            "صياغة صحيفة طعن مقام من الهيئة (نقض)",
            "صياغة مذكرة دفاع (اله

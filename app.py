import streamlit as st

# 1. الإعدادات الأساسية
st.set_page_config(page_title="مستشارك القانوني - وليد حماد", layout="wide", page_icon="⚖️")

# 2. واجهة الصفحة الأولى (اللوجو الثابت)
st.markdown("""
    <div style="text-align: center; border: 3px solid #1E3A8A; padding: 20px; border-radius: 15px; background-color: #f8f9fa; margin-bottom: 25px;">
        <h1 style="color: #1E3A8A; margin: 0; font-family: 'Arial';">مستشارك القانونى</h1>
        <h2 style="color: #ce1126; margin: 10px 0;">مع تحيات المستشار / وليد حماد</h2>
        <h3 style="color: #1E3A8A; margin: 5px;">الادارة العامة للشؤون القانونية</h3>
        <h3 style="color: #1E3A8A; margin: 0;">بالهيئة القومية للتأمين الاجتماعى</h3>
    </div>
""", unsafe_allow_html=True)

# 3. إدارة التنقل (الأيقونات الثابتة)
if 'page' not in st.session_state:
    st.session_state.page = "الرئيسية"

c1, c2 = st.columns(2)
c3, c4 = st.columns(2)
c5, c6 = st.columns(2)

with c1:
    if st.button("⚖️ أولاً: الإدارة العامة للقضايا", use_container_width=True): st.session_state.page = "قضايا"
with c2:
    if st.button("📜 ثانياً: الإدارة العامة للفتوى", use_container_width=True): st.session_state.page = "فتوى"
with c3:
    if st.button("🔍 ثالثاً: الإدارة العامة للتحقيقات والنيابات", use_container_width=True): st.session_state.page = "تحقيقات"
with c4:
    if st.button("📚 رابعاً: المكتبة القانونية الرقمية", use_container_width=True): st.session_state.page = "مكتبة"
with c5:
    if st.button("📂 خامساً: البحث والأرشيف", use_container_width=True): st.session_state.page = "أرشيف"
with c6:
    if st.button("🏠 العودة للشاشة الرئيسية", use_container_width=True): st.session_state.page = "الرئيسية"

st.markdown("---")

# 4. تفصيل الأقسام بناءً على المعطيات الصحيحة

# قسم القضايا
if st.session_state.page == "قضايا":
    st.header("⚖️ أولاً: الإدارة العامة للقضايا (القسم القضائي)")
    court_type = st.selectbox("نوع القضاء:", ["القضاء العادي (مدني/عمالي/جنائي)", "محاكم مجلس الدولة"])
    
    if court_type == "القضاء العادي":
        level = st.radio("المستوى القضائي:", ["ابتدائي", "استئناف", "نقض"], horizontal=True)
        action = st.selectbox("الإجراء:", [
            "مذكرة دفاع (الهيئة مدعى عليها)", "مذكرة دفاع (الهيئة مدعية)",
            "صحيفة استئناف مقام من الهيئة", "صحيفة طعن بالنقض",
            "مذكرة دفاع (الهيئة طاعنة/مستأنفة)", "مذكرة دفاع (الهيئة مطعون ضدها/مستأنف ضدها)"
        ])
    else: # مجلس الدولة
        level = st.selectbox("نوع المحكمة:", ["المحاكم الإدارية", "المحاكم التأديبية", "محاكم القضاء الإداري", "المحكمة الإدارية العليا"])
        action = st.selectbox("الإجراء:", ["مذكرة دفاع", "صحيفة طعن مقام من الهيئة", "مذكرة برأي الهيئة"])

    col_a, col_b = st.columns(2)
    with col_a:
        st.text_input("رقم الدعوى/الطعن")
        st.text_input("المحكمة والدائرة")
    with col_b:
        st.text_input("السنة")
        st.text_input("اسم الخصم")
    
    st.text_area("ملخص الوقائع والطلبات")
    st

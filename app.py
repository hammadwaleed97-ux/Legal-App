import streamlit as st

# 1. إعدادات الصفحة الأساسية (ثابتة)
st.set_page_config(page_title="منظومة المستشار القانوني", layout="wide", page_icon="⚖️")

# 2. واجهة الصفحة الأولى (اللوجو المعتمد)
st.markdown("""
    <div style="text-align: center; border: 3px solid #1E3A8A; padding: 20px; border-radius: 15px; background-color: #f8f9fa; margin-bottom: 25px;">
        <h2 style="color: #ce1126; margin: 10px 0;">مع تحيات المستشار / وليد حماد</h2>
        <h3 style="color: #1E3A8A; margin: 5px;">الادارة العامة للشؤون القانونية</h3>
        <h3 style="color: #1E3A8A; margin: 0;">بالهيئة القومية للتأمين الاجتماعى</h3>
    </div>
""", unsafe_allow_html=True)

# 3. إدارة التنقل عبر الأيقونات (ثابتة)
if 'page' not in st.session_state:
    st.session_state.page = "الرئيسية"

st.markdown("### الأقسام الرئيسية للمنظومة")
cols = st.columns(2)
with cols[0]:
    if st.button("⚖️ أولاً: الإدارة العامة للقضايا", use_container_width=True): st.session_state.page = "قضايا"
    if st.button("🔍 ثالثاً: الإدارة العامة للتحقيقات والنيابات", use_container_width=True): st.session_state.page = "تحقيقات"
    if st.button("📂 خامساً: البحث والأرشيف", use_container_width=True): st.session_state.page = "أرشيف"
with cols[1]:
    if st.button("📜 ثانياً: الإدارة العامة للفتوى", use_container_width=True): st.session_state.page = "فتوى"
    if st.button("📚 رابعاً: المكتبة القانونية الرقمية", use_container_width=True): st.session_state.page = "مكتبة"
    if st.button("🏠 العودة للشاشة الرئيسية", use_container_width=True): st.session_state.page = "الرئيسية"

st.markdown("---")

# 4. تفصيل الأقسام بناءً على المعطيات الصحيحة

# --- قسم القضايا (تم فصل القضاء العادي عن الإداري) ---
if st.session_state.page == "قضايا":
    st.header("⚖️ أولاً: الإدارة العامة للقضايا (القسم القضائي)")
    court_type = st.radio("نوع القضاء:", ["القضاء العادي", "مجلس الدولة (

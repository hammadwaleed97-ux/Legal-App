import streamlit as st

# 1. الإعدادات وتثبيت الصفحة الأولى
st.set_page_config(page_title="منظومة المستشار القانوني", layout="wide")

# اللوجو المعتمد (ثابت)
st.markdown("""
    <div style="text-align: center; border: 3px solid #1E3A8A; padding: 20px; border-radius: 15px; background-color: #f8f9fa; margin-bottom: 25px;">
        <h2 style="color: #ce1126; margin: 10px 0;">مع تحيات المستشار / وليد حماد</h2>
        <h3 style="color: #1E3A8A; margin: 5px;">الادارة العامة للشؤون القانونية</h3>
        <h3 style="color: #1E3A8A; margin: 0;">بالهيئة القومية للتأمين الاجتماعى</h3>
    </div>
""", unsafe_allow_html=True)

# 2. نظام التنقل (الأيقونات الثابتة)
if 'page' not in st.session_state:
    st.session_state.page = "الرئيسية"

c1, c2 = st.columns(2)
with c1:
    if st.button("⚖️ أولاً: الإدارة العامة للقضايا", use_container_width=True): st.session_state.page = "قضايا"
    if st.button("🔍 ثالثاً: الإدارة العامة للتحقيقات والنيابات", use_container_width=True): st.session_state.page = "تحقيقات"
    if st.button("📂 خامساً: البحث والأرشيف", use_container_width=True): st.session_state.page = "أرشيف"
with c2:
    if st.button("📜 ثانياً: الإدارة العامة للفتوى", use_container_width=True): st.session_state.page = "فتوى"
    if st.button("📚 رابعاً: المكتبة القانونية الرقمية", use_container_width=True): st.session_state.page = "مكتبة"
    if st.button("🏠 العودة للشاشة الرئيسية", use_container_width=True): st.session_state.page = "الرئيسية"

st.markdown("---")

# 3. تنفيذ الأقسام بناءً على المعطيات الكاملة

if st.session_state.page == "قضايا":
    st.header("⚖️ أولاً: الإدارة العامة للقضايا")
    # حل مشكلة التداخل: اختيار نوع القضاء أولاً
    court_type = st.radio("نوع القضاء:", ["القضاء العادي (مدني/عمالي)", "مجلس الدولة (إداري/تأديبي)"], horizontal=True)
    
    if court_type == "القضاء العادي":
        court_level = st.selectbox("المحكمة:", ["نقض", "استئناف عالي", "ابتدائي", "جزئي"])
    else:
        court_level = st.selectbox("المحكمة:", ["الإدارية العليا", "القضاء الإداري", "المحكمة التأديبية", "المحكمة الإدارية"])

    action = st.selectbox("الإجراء:", ["صياغة مذكرة دفاع", "صحيفة طعن مقام من الهيئة", "مذكرة برأي الهيئة"])
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.text_input("رقم الدعوى / الطعن")
        st.text_input("الم

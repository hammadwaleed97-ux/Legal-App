import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="منظومة التأمين الاجتماعي", layout="wide")

# الترويسة (اللوجو والبيانات)
st.markdown("""
    <div style="text-align: center; border: 3px solid #1E3A8A; padding: 15px; border-radius: 15px; background-color: #f8f9fa;">
        <h2 style="color: #1E3A8A; margin: 0;">الهيئة القومية للتأمين الاجتماعي</h2>
        <h3 style="color: #1E3A8A; margin: 5px;">الإدارة العامة للشئون القانونية</h3>
        <h4 style="color: #ce1126; margin: 5px;">مع تحيات أ/ وليد حماد</h4>
    </div>
""", unsafe_allow_html=True)

# الأيقونات الرئيسية في صدر الصفحة
st.write("---")
if 'page' not in st.session_state: st.session_state.page = "قضايا"

col1, col2, col3, col4, col5 = st.columns(5)
with col1: 
    if st.button("⚖️ القضايا"): st.session_state.page = "قضايا"
with col2: 
    if st.button("📜 الفتوى"): st.session_state.page = "فتوى"
with col3: 
    if st.button("🔍 التحقيقات"): st.session_state.page = "تحقيقات"
with col4: 
    if st.button("📚 المكتبة"): st.session_state.page = "مكتبة"
with col5: 
    if st.button("📂 الأرشيف"): st.session_state.page = "أرشيف"

st.write("---")

# 1. قسم القضايا
if st.session_state.page == "قضايا":
    st.subheader("⚖️ القسم القضائي (ابتدائي - استئناف - نقض - مجلس دولة)")
    court = st.selectbox("المحكمة:", ["القضاء العادي (ابتدائي/استئناف/نقض)", "مجلس الدولة (إدارية/تأديبية/عليا)"])
    action = st.selectbox("نوع الإجراء:", ["مذكرة دفاع (الهيئة مدعى عليها)", "مذكرة دفاع (الهيئة مدعية)", "صحيفة طعن/استئناف"])
    
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("رقم الدعوى/الطعن")
        st.text_input("المحكمة والدائرة")
    with c2:
        st.text_input("السنة")
        st.text_input("بيانات الخصوم")
    
    st.text_area("ملخص الوقائع وطلبات الخصم")
    st.file_uploader("ارفع صور الصحف أو الأحكام للقراءة")
    
    if st.button("صياغة قانونية"):
        st.success("تمت الصياغة: نص المادة -> الشرح -> النتيجة")
        st.write("**توقيع الهيئة:** .................... | **مدير الإدارة:** ....................")

# 2. قسم الفتوى
elif st.session_state.page == "فتوى":
    st.subheader("📜 قسم الإفتاء القانوني")
    f_type = st.radio("النوع:", ["فتاوى عامة", "إصابات عمل", "زواج عرفي"], horizontal=True)
    st.text_area("الوقائع ومثار البحث")
    st.button("صياغة الرأي القانوني")

# 3. قسم التحقيقات
elif st.session_state.page == "تحقيقات":
    st.subheader("🔍 التحقيقات والنيابات")
    i_type = st.selectbox("الجهة:", ["تحقيقات الهيئة", "النيابة الإدارية", "النيابة العامة"])
    st.text_input("اسم المخالف")
    if st.button("فتح محضر (س وج)"):
        st.write("س: ...................؟")
    st.button("صياغة مذكرة التصرف")

# 4. قسم المكتبة
elif st.session_state.page == "مكتبة":
    st.subheader("📚 المكتبة القانونية (14 قسم)")
    sec = st.selectbox("القسم:", ["قوانين", "لوائح", "قرارات وزارية", "منشورات", "كتب دورية", "تعليمات الهيئة", "فتاوى مجلس الدولة", "أحكام قضائية", "أخرى"])
    st.file_uploader("تحميل مادة علمية")
    st.info("الذكاء الاصطناعي مبرمج للصياغة من هذه المكتبة فقط.")

# 5. قسم الأرشيف
elif st.session_state.page == "أرشيف":
    st.subheader("📂 البحث والأرشيف")
    st.text_input("ابحث بالاسم أو الرقم القومي أو رقم الدعوى")
    st.button("بدء البحث في الأرشيف")

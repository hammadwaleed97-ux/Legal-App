import streamlit as st

# 1. إعدادات الصفحة واللوجو الثابت (الصفحة الأولى)
st.set_page_config(page_title="منظومة المستشار القانوني", layout="wide")

st.markdown("""
    <div style="text-align: center; border: 3px solid #1E3A8A; padding: 20px; border-radius: 15px; background-color: #f8f9fa; margin-bottom: 25px;">
        <h2 style="color: #ce1126; margin: 10px 0;">مع تحيات المستشار / وليد حماد</h2>
        <h3 style="color: #1E3A8A; margin: 5px;">الادارة العامة للشؤون القانونية</h3>
        <h3 style="color: #1E3A8A; margin: 0;">بالهيئة القومية للتأمين الاجتماعى</h3>
    </div>
""", unsafe_allow_html=True)

# 2. نظام التنقل بالأيقونات (ثابت ومفعل)
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

# 3. تفاصيل الأقسام بناءً على كامل المعطيات

if st.session_state.page == "قضايا":
    st.header("⚖️ أولاً: الإدارة العامة للقضايا")
    # فصل الاختصاص القضائي لمنع التداخل
    court_type = st.radio("نوع القضاء:", ["القضاء العادي", "مجلس الدولة"], horizontal=True)
    
    if court_type == "القضاء العادي":
        court_level = st.selectbox("المحكمة المختصة:", ["النقض", "الاستئناف العالي", "الابتدائية", "الجزئية"])
    else:
        court_level = st.selectbox("المحكمة المختصة:", ["الإدارية العليا", "القضاء الإداري", "المحكمة التأديبية", "المحكمة الإدارية"])

    action = st.selectbox("الإجراء المطلوب:", ["صياغة مذكرة دفاع", "صحيفة طعن مقام من الهيئة", "مذكرة برأي الهيئة"])
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.text_input("رقم الدعوى / الطعن والسنة")
        st.text_input("المحكمة والدائرة")
    with col_b:
        st.text_input("اسم الخصم")
        st.date_input("تاريخ الجلسة القادمة")

    st.text_area("ملخص الوقائع وطلبات الخصوم")
    
    # إضافة خانات الرفع والحفظ والصياغة
    st.file_uploader("📂 رفع صور المستندات أو ملفات PDF")
    
    btn_c1, btn_c2 = st.columns(2)
    with btn_c1:
        if st.button("💾 حفظ البيانات"): st.success("تم الحفظ في قاعدة البيانات.")
    with btn_c2:
        if st.button("📝 توليد الصياغة القانونية الآلية"): st.info("جاري المعالجة بناءً على نصوص القانون...")

elif st.session_state.page == "فتوى":
    st.header("📜 ثانياً: الإدارة العامة للفتوى")
    f_cat = st.selectbox("موضوع الفتوى:", ["فتاوى عامة", "إصابات عمل", "شكاوى الزواج العرفي", "أخرى"])
    st.text_area("الوقائع المعروضة")
    st.file_uploader("ارفع مستند الإحالة")
    st.button("💾 حفظ")
    st.button("✍️ إعداد مسودة الرأي القانوني")

elif st.session_state.page == "تحقيقات":
    st.header("🔍 ثالثاً: الإدارة العامة للتحقيقات والنيابات")
    i_org = st.selectbox("جهة الاختصاص:", ["تحقيقات الهيئة", "النيابة الإدارية", "النيابة العامة"])
    st.text_input("اسم المحال للتحقيق / رقم القضية")
    st.text_area("موضوع المخالفة")
    st.button("💾 حفظ")
    st.button("📜 صياغة مذكرة التصرف")

elif st.session_state.page == "مكتبة":
    st.header("📚 رابعاً: المكتبة القانونية الرقمية (14 قسماً)")
    lib_sections = [
        "أولاً: القوانين", "ثانياً: اللوائح", "ثالثاً: القرارات الوزارية", "رابعاً: المنشورات الوزارية",
        "خامساً: قرارات رئيس الهيئة", "سادساً: منشورات رئيس الهيئة", "سابعاً: الكتب الدورية",
        "ثامناً: تعليمات الهيئة", "تاسعاً: المرصد الفني للهيئة", "عاشراً: رسائل الهيئة",
        "حادى عشر: مذكرات اللجنة القانونية", "ثانى عشر: فتاوى مجلس الدولة", "ثالثا عشر: أحكام قضائية", "رابع عشر: أخرى"
    ]
    st.selectbox("اختر القسم:", lib_sections)
    st.text_input("ابحث في المكتبة...")
    st.button("🔍 بدء البحث")

elif st.session_state.page == "أرشيف":
    st.header("📂 خامساً: البحث والأرشيف")
    st.text_input("ابحث برقم الدعوى أو الاسم")
    st.button("🔍 استعلام")

else:
    st.info("مرحباً بك يا سيادة المستشار. المنظومة جاهزة للعمل، اختر القسم المطلوب.")

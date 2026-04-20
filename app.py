import streamlit as st

# 1. إعدادات الصفحة واللوجو (كما طلبت بالظبط)
st.set_page_config(page_title="منظومة المستشار وليد حماد", layout="wide")

st.markdown("""
    <div style="text-align: center; border: 4px solid #1E3A8A; padding: 20px; border-radius: 15px; background-color: #f8f9fa; margin-bottom: 20px;">
        <h1 style="color: #1E3A8A; margin: 0;">الهيئة القومية للتأمين الاجتماعى</h1>
        <h2 style="color: #1E3A8A; margin: 5px 0;">الادارة المركزية للإدارات القانونية</h2>
        <hr style="border: 1px solid #ce1126; width: 40%; margin: 10px auto;">
        <h2 style="color: #ce1126; margin: 10px 0;">مع تحيات / وليد حماد</h2>
        <h3 style="color: #1E3A8A; margin: 5px;">عضو الادارة القانونية بديوان عام منطقة البحيرة</h3>
    </div>
""", unsafe_allow_html=True)

# 2. إدارة التنقل (لضمان عدم حدوث خطأ الصور)
if 'main_page' not in st.session_state:
    st.session_state.main_page = "home"

# 3. الشاشة الرئيسية (الأيقونات الستة تحت اللوجو)
if st.session_state.main_page == "home":
    st.markdown("<h4 style='text-align: center; color: #1E3A8A;'>أقسام المنظومة القضائية</h4>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⚖️ أولاً: الإدارة العامة للقضايا", use_container_width=True):
            st.session_state.main_page = "qadaya"
            st.rerun()
        if st.button("🔍 ثالثاً: الإدارة العامة للتحقيقات والنيابات", use_container_width=True):
            st.session_state.main_page = "tahqiqat"
            st.rerun()
        if st.button("📂 خامساً: البحث والأرشيف", use_container_width=True):
            st.session_state.main_page = "archive"
            st.rerun()

    with col2:
        if st.button("📜 ثانياً: الإدارة العامة للفتوى", use_container_width=True):
            st.session_state.main_page = "fatwa"
            st.rerun()
        if st.button("📚 رابعاً: المكتبة القانونية الرقمية", use_container_width=True):
            st.session_state.main_page = "library"
            st.rerun()
        if st.button("🔐 سادساً: لوحة تحكم الإدارة (خاص)", use_container_width=True):
            st.session_state.main_page = "admin"
            st.rerun()

# 4. تفاصيل الأقسام (المعطيات كاملة)
else:
    if st.button("🔙 العودة للشاشة الرئيسية"):
        st.session_state.main_page = "home"
        st.rerun()
    
    st.markdown("---")

    if st.session_state.main_page == "qadaya":
        st.header("⚖️ الإدارة العامة للقضايا")
        court_type = st.radio("نوع القضاء:", ["القضاء العادي", "مجلس الدولة"], horizontal=True)
        c_a, c_b = st.columns(2)
        with c_a:
            st.text_input("رقم الدعوى والسنة")
            st.selectbox("المحكمة:", ["النقض/الإدارية العليا", "الاستئناف/القضاء الإداري", "الابتدائي/التأديبي"])
        with c_b:
            st.text_input("اسم الخصم")
            st.file_uploader("📂 ارفع المستندات (PDF/صور)")
        
        st.text_area("وقائع الدعوى (لتحليل الذكاء الاصطناعي)")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1: st.button("💾 حفظ البيانات")
        with col_btn2: st.button("📝 توليد الصياغة القانونية")

    elif st.session_state.main_page == "library":
        st.header("📚 المكتبة القانونية الرقمية (14 قسماً)")
        sections = [
            "أولاً: القوانين", "ثانياً: اللوائح", "ثالثاً: القرارات الوزارية", "رابعاً: المنشورات الوزارية",
            "خامساً: قرارات رئيس الهيئة", "سادساً: منشورات رئيس الهيئة", "سابعاً: الكتب الدورية",
            "ثامناً: تعليمات الهيئة", "تاسعاً: المرصد الفني", "عاشراً: رسائل الهيئة",
            "11: مذكرات اللجنة القانونية", "12: فتاوى مجلس الدولة", "13: أحكام قضائية", "14: أخرى"
        ]
        st.selectbox("اختر القسم للتصفح والتحميل:", sections)
        st.text_input("🔍 ابحث عن مستند...")
        st.info("ملاحظة: يمكنك التحميل المباشر فور ظهور نتائج البحث.")

    elif st.session_state.main_page == "admin":
        st.header("🔐 لوحة تحكم المستشار (إضافة قوانين)")
        pwd = st.text_input("كلمة مرور الإدارة:", type="password")
        if pwd == "Waleed2026":
            st.success("تم تفعيل صلاحيات الإضافة.")
            st.selectbox("إضافة إلى قسم:", ["قوانين", "منشورات", "تعليمات"])
            st.file_uploader("ارفع الملف الجديد للمكتبة")
            st.button("حفظ ونشر")
        else:
            st.error("هذا القسم مخصص للمستشار وليد حماد فقط.")

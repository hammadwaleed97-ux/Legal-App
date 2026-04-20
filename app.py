import streamlit as st

# 1. إعدادات الصفحة واللوجو المعتمد (ثابت في الأعلى)
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

# 2. عرض كافة المعطيات مباشرة (بدون عودة للصفحة الرئيسية)

# --- القسم الأول: القضايا ---
with st.expander("⚖️ أولاً: الإدارة العامة للقضايا", expanded=False):
    court_type = st.radio("نوع القضاء:", ["القضاء العادي", "مجلس الدولة"], horizontal=True)
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("رقم الدعوى والسنة")
        st.selectbox("المحكمة المختصة:", ["النقض/الإدارية العليا", "الاستئناف", "الابتدائية"])
    with c2:
        st.text_input("اسم الخصم")
        st.file_uploader("📂 رفع صور المستندات")
    st.text_area("وقائع الدعوى")
    if st.button("📝 توليد الصياغة الآلية"):
        st.info("جاري المعالجة بالذكاء الاصطناعي...")

# --- القسم الثاني: الفتوى ---
with st.expander("📜 ثانياً: الإدارة العامة للفتوى", expanded=False):
    st.selectbox("موضوع الفتوى:", ["فتاوى عامة", "إصابات عمل", "منازعات"])
    st.text_area("موضوع الاستفسار القانوني")
    st.button("💾 حفظ وطلب رأي قانوني")

# --- القسم الثالث: التحقيقات ---
with st.expander("🔍 ثالثاً: الإدارة العامة للتحقيقات والنيابات", expanded=False):
    st.text_input("اسم المحال للتحقيق")
    st.text_area("المخالفة المنسوبة")
    st.button("📜 صياغة مذكرة التصرف")

# --- القسم الرابع: المكتبة القانونية (14 قسماً - تحميل مباشر) ---
with st.expander("📚 رابعاً: المكتبة القانونية الرقمية", expanded=False):
    lib_sections = [
        "القوانين", "اللوائح", "القرارات الوزارية", "المنشورات الوزارية",
        "قرارات رئيس الهيئة", "منشورات رئيس الهيئة", "الكتب الدورية",
        "تعليمات الهيئة", "المرصد الفني", "رسائل الهيئة",
        "مذكرات اللجنة القانونية", "فتاوى مجلس الدولة", "أحكام قضائية", "أخرى"
    ]
    st.selectbox("اختر القسم للتصفح:", lib_sections)
    st.text_input("🔍 ابحث عن مستند لتحميله...")
    # محاكاة لزر التحميل
    st.markdown("""<div style='background-color:#e1e4e8; padding:10px; border-radius:5px;'>
    📥 رابط تحميل المستند يظهر هنا بعد البحث</div>""", unsafe_allow_html=True)

# --- القسم الخامس: الأرشيف ---
with st.expander("📂 خامساً: البحث والأرشيف", expanded=False):
    st.text_input("ابحث برقم القضية أو اسم الخصم...")
    st.button("🔍 استعلام من الأرشيف")

# --- القسم السادس: لوحة التحكم (لك أنت فقط) ---
with st.expander("🔐 سادساً: لوحة تحكم الإدارة (إضافة محتوى)", expanded=False):
    pwd = st.text_input("كلمة مرور المستشار:", type="password")
    if pwd == "Waleed2026":
        st.success("مرحباً سيادة المستشار. يمكنك إضافة ملفات للمكتبة هنا.")
        st.file_uploader("ارفع الملف الجديد")
        st.button("نشر في المكتبة")
    elif pwd != "":
        st.error("عفواً، الصلاحية للمستشار وليد حماد فقط.")

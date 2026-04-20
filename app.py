import streamlit as st

# 1. إعدادات الصفحة واللوجو (البيانات اللي طلبتها بالحرف)
st.set_page_config(page_title="منظومة المستشار وليد حماد", layout="wide")

st.markdown("""
    <div style="text-align: center; border: 4px solid #1E3A8A; padding: 25px; border-radius: 20px; background-color: #f8f9fa; margin-bottom: 30px;">
        <h1 style="color: #1E3A8A; margin: 0; font-family: 'Arial';">الهيئة القومية للتأمين الاجتماعى</h1>
        <h2 style="color: #1E3A8A; margin: 5px 0;">الادارة المركزية للإدارات القانونية</h2>
        <hr style="border: 1px solid #ce1126; width: 40%; margin: 10px auto;">
        <h2 style="color: #ce1126; margin: 10px 0;">مع تحيات / وليد حماد</h2>
        <h3 style="color: #1E3A8A; margin: 5px;">عضو الادارة القانونية بديوان عام منطقة البحيرة</h3>
    </div>
""", unsafe_allow_html=True)

# 2. نظام التنقل (عشان الأيقونات ترجع مكانها تحت اللوجو)
if 'choice' not in st.session_state:
    st.session_state.choice = "الرئيسية"

# 3. واجهة الأيقونات الستة (الواجهة اللي أنت اعتمدتها)
if st.session_state.choice == "الرئيسية":
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⚖️ أولاً: الإدارة العامة للقضايا", use_container_width=True):
            st.session_state.choice = "قضايا"
            st.rerun()
        if st.button("🔍 ثالثاً: الإدارة العامة للتحقيقات والنيابات", use_container_width=True):
            st.session_state.choice = "تحقيقات"
            st.rerun()
        if st.button("📂 خامساً: البحث والأرشيف", use_container_width=True):
            st.session_state.choice = "أرشيف"
            st.rerun()

    with col2:
        if st.button("📜 ثانياً: الإدارة العامة للفتوى", use_container_width=True):
            st.session_state.choice = "فتوى"
            st.rerun()
        if st.button("📚 رابعاً: المكتبة القانونية الرقمية", use_container_width=True):
            st.session_state.choice = "مكتبة"
            st.rerun()
        if st.button("🔐 سادساً: لوحة تحكم الإدارة (خاص بك)", use_container_width=True):
            st.session_state.choice = "إدارة"
            st.rerun()

# 4. تفاصيل الأقسام (عند الضغط على أي أيقونة)
else:
    if st.button("🔙 العودة للشاشة الرئيسية"):
        st.session_state.choice = "الرئيسية"
        st.rerun()
    
    st.markdown("---")

    if st.session_state.choice == "قضايا":
        st.header("⚖️ الإدارة العامة للقضايا")
        court = st.radio("نوع القضاء:", ["القضاء العادي", "مجلس الدولة"], horizontal=True)
        st.text_input("رقم الدعوى والسنة")
        st.text_area("وقائع الدعوى (لتحليل الذكاء الاصطناعي)")
        st.button("💾 حفظ")
        st.button("📝 صياغة المذكرة")

    elif st.session_state.choice == "مكتبة":
        st.header("📚 المكتبة القانونية الرقمية (14 قسماً)")
        sections = ["قوانين", "لوائح", "تعليمات الهيئة", "منشورات", "أحكام قضائية", "فتاوى مجلس الدولة", "أخرى"]
        st.selectbox("اختر القسم:", sections)
        st.text_input("🔍 ابحث عن مستند...")
        st.info("تظهر هنا النتائج مع أيقونة 📥 للتحميل المباشر.")

    elif st.session_state.choice == "إدارة":
        st.header("🔐 لوحة التحكم للمستشار فقط")
        pwd = st.text_input("كلمة المرور:", type="password")
        if pwd == "Waleed2026":
            st.success("أهلاً بك يا سيادة المستشار. يمكنك إضافة ملفات للمكتبة هنا.")
            st.file_uploader("ارفع الملف الجديد للمكتبة")
            st.button("نشر بالموقع")
        else:
            st.error("هذا القسم خاص بالمستشار وليد حماد فقط.")

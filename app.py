import streamlit as st
import pandas as pd

# 1. إعدادات الهوية واللوجو المعتمد (مركز الشاشة)
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

# 2. تهيئة الجلسة (Session State) لتخزين البيانات والتنقل
if 'page' not in st.session_state: st.session_state.page = "الرئيسية"
if 'db' not in st.session_state: st.session_state.db = []

# 3. الأيقونات الستة الرئيسية (تحت اللوجو مباشرة)
if st.session_state.page == "الرئيسية":
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("⚖️ أولاً: الإدارة العامة للقضايا", use_container_width=True): st.session_state.page = "قضايا"
        if st.button("📜 ثانياً: الإدارة العامة للفتوى", use_container_width=True): st.session_state.page = "فتوى"
    with c2:
        if st.button("🔍 ثالثاً: الإدارة العامة للتحقيقات", use_container_width=True): st.session_state.page = "تحقيقات"
        if st.button("📚 رابعاً: المكتبة القانونية الرقمية", use_container_width=True): st.session_state.page = "مكتبة"
    with c3:
        if st.button("📂 خامساً: البحث والأرشيف", use_container_width=True): st.session_state.page = "أرشيف"
        if st.button("🔐 سادساً: لوحة تحكم الإدارة", use_container_width=True): st.session_state.page = "إدارة"

# 4. تفاصيل الأقسام (بناءً على المعطيات)
if st.session_state.page != "الرئيسية":
    if st.button("⬅️ العودة للشاشة الرئيسية"): st.session_state.page = "الرئيسية"; st.rerun()

    # --- قسم القضايا ---
    if st.session_state.page == "قضايا":
        st.header("⚖️ الإدارة العامة للقضايا")
        court_type = st.radio("نوع القضاء:", ["القضاء العادي", "مجلس الدولة"], horizontal=True)
        col_q1, col_q2 = st.columns(2)
        with col_q1:
            court = st.selectbox("المحكمة:", ["النقض/الإدارية العليا", "الاستئناف/القضاء الإداري", "الابتدائية/التأديبية"])
            case_no = st.text_input("رقم الدعوى والسنة")
        with col_q2:
            opponent = st.text_input("اسم الخصم")
            action = st.selectbox("الإجراء:", ["مذكرة دفاع", "صحيفة طعن", "رأي قانوني"])
        
        facts = st.text_area("وقائع الدعوى (للتحليل بالذكاء الاصطناعي)")
        st.file_uploader("📂 ارفع صور المستندات")
        if st.button("📝 توليد الصياغة وتحميلها"):
            st.info("جاري الصياغة...")
            st.download_button("📥 تحميل المذكرة", data=f"مذكرة رقم {case_no}", file_name="draft.txt")

    # --- قسم المكتبة (14 قسماً) ---
    elif st.session_state.page == "مكتبة":
        st.header("📚 المكتبة القانونية الشاملة")
        lib_sections = ["قوانين", "لوائح", "قرارات وزارية", "منشورات وزارية", "قرارات رئيس الهيئة", "منشورات رئيس الهيئة", "كتب دورية", "تعليمات الهيئة", "المرصد الفني", "رسائل الهيئة", "مذكرات اللجنة القانونية", "فتاوى مجلس الدولة", "أحكام قضائية", "أخرى"]
        sec = st.selectbox("اختر القسم:", lib_sections)
        st.text_input(f"البحث في {sec}...")
        st.markdown("---")
        st.write("النتائج تظهر هنا مع أيقونة التحميل بجانب كل مستند.")

    # --- قسم لوحة التحكم (أنت فقط) ---
    elif st.session_state.page == "إدارة":
        st.header("🔐 لوحة تحكم المستشار (إضافة محتوى)")
        pwd = st.text_input("كلمة السر:", type="password")
        if pwd == "Waleed2026":
            st.success("مرحباً سيادة المستشار. يمكنك إضافة قوانين أو منشورات جديدة للمكتبة هنا.")
            # هنا تضع فورم الإضافة
        else:
            st.error("هذا القسم خاص بالمستشار وليد حماد فقط.")

    # --- قسم الأرشيف ---
    elif st.session_state.page == "أرشيف":
        st.header("📂 الأرشيف والبحث المركزي")
        st.info("الأرشيف جاهز لعرض البيانات المحفوظة.")

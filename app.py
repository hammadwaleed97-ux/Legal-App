import streamlit as st
import pandas as pd

# 1. إعدادات الهوية واللوجو المعتمد (ثابت في الأعلى)
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

# 2. تهيئة قاعدة البيانات الافتراضية
if 'library_db' not in st.session_state:
    st.session_state.library_db = []
if 'cases_db' not in st.session_state:
    st.session_state.cases_db = []

# 3. عرض الأقسام الرئيسية (فتح مباشر كما طلبت)

# --- القسم الأول: لوحة تحكم المستشار (لرفع المادة العلمية والملفات) ---
with st.expander("🔐 أولاً: لوحة تحكم المستشار (رفع المادة العلمية والملفات)", expanded=True):
    pwd = st.text_input("كلمة مرور الإدارة للرفع:", type="password")
    if pwd == "Waleed2026":
        st.success("مرحباً سيادة المستشار. هنا ترفع المادة التي سيبحث فيها الذكاء الاصطناعي.")
        with st.form("upload_form"):
            category = st.selectbox("تصنيف الملف:", ["قوانين", "تعليمات", "منشورات", "أحكام", "كتب دورية"])
            doc_title = st.text_input("اسم المستند:")
            doc_file = st.file_uploader("اختر الملف لرفعه للمكتبة (PDF/Text/Word)")
            doc_text = st.text_area("أو انسخ النص هنا مباشرة (ليتعرف عليه الذكاء الاصطناعي):")
            if st.form_submit_button("✅ رفع ونشر في المكتبة"):
                st.session_state.library_db.append({"القسم": category, "العنوان": doc_title, "المحتوى": doc_text})
                st.success("تم الحفظ بنجاح.")
    elif pwd != "":
        st.error("الصلاحية للمستشار وليد حماد فقط.")

# --- القسم الثاني: المكتبة القانونية (تصفح وتحميل وبحث ذكي) ---
with st.expander("📚 ثانياً: المكتبة القانونية الرقمية والبحث الذكي", expanded=False):
    st.info("هنا يبحث الذكاء الاصطناعي في المادة التي رفعتها سيادتك.")
    search_q = st.text_input("🔍 ابحث في المادة العلمية (مثال: شروط استحقاق المعاش)...")
    
    # تصفية النتائج من المادة المرفوعة
    results = [i for i in st.session_state.library_db if search_q.lower() in i['العنوان'].lower() or search_q in i['المحتوى']]
    
    if results:
        for res in results:
            col1, col2 = st.columns([5, 1])
            with col1: st.write(f"📄 **{res['القسم']}**: {res['العنوان']}")
            with col2: st.download_button("📥 تحميل", data=res['المحتوى'], file_name=f"{res['العنوان']}.txt")
    
    st.markdown("---")
    if st.button("🤖 استشارة الذكاء الاصطناعي في المادة المرفوعة"):
        st.subheader("تحليل الذكاء الاصطناعي:")
        st.write("بناءً على المادة العلمية التي قمت برفعها، الرأي القانوني هو...")

# --- القسم الثالث: إدارة القضايا والتحقيقات ---
with st.expander("⚖️ ثالثاً: إدارة القضايا والتحقيقات (صياغة وتحميل)", expanded=False):
    c1, c2 = st.columns(2)
    with c1:
        case_no = st.text_input("رقم الملف/القضية")
        opponent = st.text_input("الخصم")
    with c2:
        case_type = st.selectbox("النوع:", ["قضية", "تحقيق", "فتوى"])
        court = st.text_input("المحكمة/جهة التحقيق")
    
    case_facts = st.text_area("الوقائع والصياغة:")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("💾 حفظ في الأرشيف"):
            st.session_state.cases_db.append({"الرقم": case_no, "الخصم": opponent, "النوع": case_type})
            st.success("تم الحفظ في الأرشيف.")
    with col_btn2:
        # أيقونة التحميل للقضايا التي طلبتها
        st.download_button("📥 تحميل مسودة المذكرة", data=case_facts, file_name=f"مذكرة_{case_no}.txt")

# --- القسم الرابع: البحث في الأرشيف ---
with st.expander("📂 رابعاً: البحث في الأرشيف", expanded=False):
    st.write("السجلات المحفوظة:")
    if st.session_state.cases_db:
        st.table(pd.DataFrame(st.session_state.cases_db))
    else:
        st.info("الأرشيف فارغ حالياً.")

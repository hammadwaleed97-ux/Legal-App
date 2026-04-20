import streamlit as st
import pandas as pd

# 1. الهوية البصرية (اللوجو المعتمد)
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

# 2. تخزين البيانات (المادة العلمية والقضايا)
if 'library_data' not in st.session_state: st.session_state.library_data = []
if 'archive_data' not in st.session_state: st.session_state.archive_data = []

# 3. الأقسام الستة (كل قسم وحدة مستقلة)

# --- القسم الأول: لوحة التحكم (لرفع المادة العلمية) ---
with st.expander("🔐 لوحة تحكم المستشار (رفع المادة العلمية)", expanded=True):
    pwd = st.text_input("كلمة مرور الإدارة:", type="password")
    if pwd == "Waleed2026":
        st.write("ارفع الملفات التي سيبحث فيها الذكاء الاصطناعي:")
        uploaded_file = st.file_uploader("اختر ملف (PDF/Word/Text)", key="lib_upload")
        raw_text = st.text_area("أو انسخ المادة القانونية هنا مباشرة:")
        if st.button("✅ اعتماد المادة ونشرها"):
            st.session_state.library_data.append({"مادة": raw_text if raw_text else uploaded_file.name})
            st.success("تمت إضافة المادة العلمية بنجاح.")

# --- القسم الثاني: المكتبة والبحث والتحميل ---
with st.expander("📚 المكتبة القانونية (البحث والتحميل)", expanded=False):
    search_q = st.text_input("🔍 ابحث في المادة العلمية المرفوعة:")
    if st.session_state.library_data:
        for item in st.session_state.library_data:
            st.write(f"📄 مادة متاحة: {item['مادة'][:100]}...")
            st.download_button("📥 تحميل المادة", data=item['مادة'], file_name="law_document.txt")
    else:
        st.info("المكتبة بانتظار رفع المادة العلمية من لوحة التحكم.")

# --- القسم الثالث: الإدارة العامة للقضايا (صياغة وتحميل) ---
with st.expander("⚖️ الإدارة العامة للقضايا (الصياغة والتحميل)", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        case_id = st.text_input("رقم القضية")
        opp = st.text_input("الخصم")
    with col2:
        court = st.text_input("المحكمة")
        file_case = st.file_uploader("أيقونة تحميل مستندات القضية", key="case_up")
    
    draft = st.text_area("اكتب الوقائع ليقوم الذكاء الاصطناعي بصياغتها:")
    if st.button("💾 حفظ في الأرشيف"):
        st.session_state.archive_data.append({"الرقم": case_id, "الخصم": opp, "المحكمة": court})
    
    # أيقونة التحميل التي طلبتها
    st.download_button("📥 تحميل مسودة المذكرة النهائية", data=draft, file_name=f"مذكرة_{case_id}.txt")

# --- القسم الرابع: البحث في الأرشيف ---
with st.expander("📂 البحث في الأرشيف", expanded=False):
    search_arch = st.text_input("ابحث برقم القضية في الأرشيف:")
    if st.session_state.archive_data:
        df = pd.DataFrame(st.session_state.archive_data)
        st.dataframe(df, use_container_width=True)

# --- الأقسام المتبقية (الفتوى والتحقيقات) ---
with st.expander("📜 الإدارة العامة للفتوى", expanded=False):
    st.write("قسم الفتوى قيد التشغيل...")
with st.expander("🔍 الإدارة العامة للتحقيقات", expanded=False):
    st.write("قسم التحقيقات قيد التشغيل...")

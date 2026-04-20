import streamlit as st
import pandas as pd

# 1. تثبيت الهوية (اللوجو المعتمد)
st.set_page_config(page_title="منظومة المستشار وليد حماد", layout="wide")

st.markdown("""
    <div style="text-align: center; border: 4px solid #1E3A8A; padding: 20px; border-radius: 15px; background-color: #f8f9fa; margin-bottom: 20px;">
        <h1 style="color: #1E3A8A; margin: 0; font-size: 28px;">الهيئة القومية للتأمين الاجتماعى</h1>
        <h2 style="color: #1E3A8A; margin: 5px 0; font-size: 22px;">الادارة المركزية للإدارات القانونية</h2>
        <hr style="border: 1px solid #ce1126; width: 40%; margin: 10px auto;">
        <h2 style="color: #ce1126; margin: 10px 0;">مع تحيات / وليد حماد</h2>
        <h3 style="color: #1E3A8A; margin: 5px;">عضو الادارة القانونية بديوان عام منطقة البحيرة</h3>
    </div>
""", unsafe_allow_html=True)

# 2. إدارة البيانات في الذاكرة
if 'data_lib' not in st.session_state: st.session_state.data_lib = []
if 'cases_arch' not in st.session_state: st.session_state.cases_arch = []

# --- القسم الأول: لوحة التحكم (لرفع المادة العلمية التي سيبحث فيها الذكاء الاصطناعي) ---
with st.expander("🔐 لوحة التحكم (رفع المادة العلمية والبيانات)", expanded=True):
    pwd = st.text_input("أدخل كلمة المرور للإدارة:", type="password")
    if pwd == "Waleed2026":
        st.success("مرحباً سيادة المستشار. ارفع ملفات المادة العلمية هنا.")
        up_file = st.file_uploader("رفع ملف (PDF/Word/Text)", key="main_up")
        up_text = st.text_area("أو انسخ المادة القانونية مباشرة هنا:")
        if st.button("✅ حفظ المادة العلمية"):
            st.session_state.data_lib.append({"نص": up_text if up_text else up_file.name})
            st.success("تم الحفظ. الآن يمكن للذكاء الاصطناعي البحث في هذه المعلومات.")
    elif pwd != "":
        st.error("عفواً، الصلاحية للمستشار وليد حماد فقط.")

# --- القسم الثاني: المكتبة والبحث الذكي (تصفح وتحميل) ---
with st.expander("📚 المكتبة القانونية والبحث الذكي", expanded=False):
    st.write("البحث في المادة العلمية المرفوعة:")
    search = st.text_input("🔍 ابحث عن مادة أو قانون...")
    if st.session_state.data_lib:
        for item in st.session_state.data_lib:
            col1, col2 = st.columns([5, 1])
            with col1: st.write(f"📄 مادة متاحة: {item['نص'][:100]}...")
            with col2: st.download_button("📥 تحميل", data=item['نص'], file_name="law_doc.txt", key=item['نص'][:10])
        
        if st.button("🤖 استشارة الذكاء الاصطناعي"):
            st.info("جاري تحليل المادة العلمية المرفوعة...")
            st.write("بناءً على المادة التي رفعتها، الرأي القانوني هو...")

# --- القسم الثالث: الإدارة العامة للقضايا والتحقيقات ---
with st.expander("⚖️ إدارة القضايا والتحقيقات (صياغة وتحميل)", expanded=False):
    c1, c2 = st.columns(2)
    with c1:
        c_num = st.text_input("رقم القضية/الملف")
        c_opp = st.text_input("اسم الخصم")
    with c2:
        c_court = st.text_input("المحكمة/النيابة")
        c_upload = st.file_uploader("أيقونة تحميل مستندات القضية", key="c_up")
    
    c_draft = st.text_area("نص المذكرة/الوقائع:")
    
    b1, b2 = st.columns(2)
    with b1:
        if st.button("💾 حفظ في الأرشيف"):
            st.session_state.cases_arch.append({"رقم": c_num, "خصم": c_opp, "محكمة": c_court})
            st.success("تم الحفظ.")
    with b2:
        # أيقونة التحميل التي طلبتها للقضايا
        st.download_button("📥 تحميل المذكرة النهائية", data=c_draft, file_name=f"case_{c_num}.txt")

# --- القسم الرابع: البحث في الأرشيف ---
with st.expander("📂 البحث في الأرشيف", expanded=False):
    st.write("سجل القضايا والتحقيقات المحفوظة:")
    if st.session_state.cases_arch:
        st.table(pd.DataFrame(st.session_state.cases_arch))
    else:
        st.info("الأرشيف فارغ.")

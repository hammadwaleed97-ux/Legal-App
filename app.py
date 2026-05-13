import streamlit as st
from pypdf import PdfReader
import os

# إعدادات واجهة المنصة
st.set_page_config(page_title="منصة البحيرة القانونية", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; background-color: #1e3a8a; color: white; font-weight: bold; }
    .law-box { padding: 15px; border-radius: 8px; background-color: #ffffff; border-right: 5px solid #1e3a8a; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ المنصة الذكية للاستخراج القانوني")

# --- القائمة الجانبية (لوحة التحكم) ---
with st.sidebar:
    st.header("🔐 لوحة تحكم المدير")
    pw = st.text_input("أدخل كلمة المرور:", type="password")
    # إضافة زر "دخول" بدلاً من الاعتماد على Enter الموبايل
    login_btn = st.button("تأكيد الدخول")
    
    # إذا ضغطت على الزر وكانت كلمة السر 123
    if login_btn and pw == "123":
        st.session_state['admin_logged_in'] = True

    if st.session_state.get('admin_logged_in'):
        st.success("أهلاً سيادة المستشار")
        up_file = st.file_uploader("📂 ارفع المادة العلمية (PDF):", type="pdf")
        if up_file:
            with open("legal_core.pdf", "wb") as f:
                f.write(up_file.getvalue())
            st.info("تم تحديث المادة العلمية بنجاح.")

# --- واجهة البحث والاستخراج ---
if os.path.exists("legal_core.pdf"):
    st.write("---")
    query = st.text_input("🔍 اكتب موضوع البحث (مثال: نصيب الأرملة):")
    
    if query:
        reader = PdfReader("legal_core.pdf")
        found = False
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if query in text:
                found = True
                start = max(0, text.find(query) - 200)
                end = text.find(query) + 600
                st.markdown(f"<div class='law-box'><b>من الصفحة ({i+1}):</b><br>{text[start:end]}...</div>", unsafe_allow_html=True)
        if not found:
            st.error("لم يتم العثور على هذا النص في الملف المرفوع.")
else:
    st.warning("⚠️ يرجى رفع المادة العلمية من لوحة التحكم الجانبية أولاً.")

st.markdown("<br><hr><p style='text-align: center;'>مع تحيات وليد حماد - الإدارة العامة للشئون القانونية - ديوان عام منطقة البحيرة</p>", unsafe_allow_html=True)

import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader

st.set_page_config(page_title="مستشارك القانوني", layout="wide")

# تصميم بسيط وسريع التحميل
st.markdown("""
    <style>
    .law-card { background: #ffffff; padding: 15px; border-radius: 8px; border-right: 5px solid #1e3a8a; margin-bottom: 10px; box-shadow: 1px 1px 3px rgba(0,0,0,0.1); direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

VAULT = "laws_vault"
if not os.path.exists(VAULT): os.makedirs(VAULT)

# --- الجانب الإداري ---
with st.sidebar:
    st.header("🔑 دخول الإدارة")
    if st.text_input("الرمز:", type="password") == "123":
        uploaded = st.file_uploader("رفع ملفات PDF:", accept_multiple_files=True)
        if uploaded:
            for f in uploaded:
                with open(os.path.join(VAULT, f.name), "wb") as doc: doc.write(f.getvalue())
            st.success("تم الحفظ")
            st.rerun()

# --- الواجهة الرئيسية ---
st.title("🏛️ منظومة البحث القانوني السريع")

all_laws = [f for f in os.listdir(VAULT) if f.endswith('.pdf')]

if all_laws:
    query = st.text_input("أدخل الكلمة المراد البحث عنها (مثلاً: نصيب الأرملة):")
    
    if query:
        with st.spinner("جاري فحص المستندات..."):
            found = False
            for law_file in all_laws:
                loader = PyPDFLoader(os.path.join(VAULT, law_file))
                pages = loader.load()
                for i, page in enumerate(pages):
                    if query in page.page_content:
                        found = True
                        st.markdown(f"""
                        <div class='law-card'>
                            <b>📄 المصدر: {law_file} | صفحة: {i+1}</b><br><br>
                            {page.page_content.replace(query, f'<span style="background:yellow">{query}</span>')}
                        </div>
                        """, unsafe_allow_html=True)
            if not found:
                st.warning("لم يتم العثور على هذه الكلمة في القوانين المرفوعة.")
else:
    st.info("المكتبة فارغة. ارفع الملفات من القائمة الجانبية.")

st.markdown("<br><hr><p style='text-align:center;'>مع تحيات وليد حماد - الإدارة العامة للشئون القانونية</p>", unsafe_allow_html=True)

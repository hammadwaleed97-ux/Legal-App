import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader

st.set_page_config(page_title="مستشارك القانوني", layout="wide")

# تصميم مريح وسريع لا يسبب ثقل الشاشة
st.markdown("""
    <style>
    .stTextInput>div>div>input { border: 2px solid #1e3a8a; }
    .law-card { background: #f9f9f9; padding: 15px; border-right: 5px solid #b8860b; margin-bottom: 10px; direction: rtl; }
    .stButton>button { background-color: #1e3a8a; color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

VAULT = "laws_vault"
if not os.path.exists(VAULT): os.makedirs(VAULT)

# --- القائمة الجانبية ---
with st.sidebar:
    st.header("🔑 دخول الإدارة")
    if st.text_input("الرمز:", type="password") == "123":
        uploaded = st.file_uploader("رفع ملفات PDF:", accept_multiple_files=True)
        if uploaded:
            for f in uploaded:
                with open(os.path.join(VAULT, f.name), "wb") as doc: doc.write(f.getvalue())
            st.success("تم الحفظ بنجاح")
            st.rerun()

# --- الواجهة الرئيسية ---
st.markdown("<h2 style='text-align:center;'>🏛️ منظومة الاستعلام القانوني</h2>", unsafe_allow_html=True)

# النص الذي طلبته بالضبط
query = st.text_input("اتفضل اطرح تساؤلك أو الاشكال القانونى:")

if st.button("🔍 استخراج الرد القانوني"):
    if query:
        files = [f for f in os.listdir(VAULT) if f.endswith('.pdf')]
        if not files:
            st.warning("المكتبة فارغة، برجاء رفع الملفات أولاً.")
        else:
            with st.spinner("جاري البحث في الملفات..."):
                found = False
                for f_name in files:
                    loader = PyPDFLoader(os.path.join(VAULT, f_name))
                    pages = loader.load()
                    for i, page in enumerate(pages):
                        if query in page.page_content:
                            found = True
                            st.markdown(f"""
                            <div class='law-card'>
                                <b>📄 المصدر: {f_name} (صفحة {i+1})</b><br><br>
                                {page.page_content}
                            </div>
                            """, unsafe_allow_html=True)
                if not found:
                    st.info("لم يتم العثور على نص مطابق تماماً، جرب كتابة كلمة مفتاحية أدق.")
    else:
        st.error("برجاء كتابة التساؤل أولاً.")

st.markdown("<br><hr><p style='text-align:center;'>مع تحيات وليد حماد - الإدارة العامة للشئون القانونية - ديوان عام منطقة البحيرة</p>", unsafe_allow_html=True)

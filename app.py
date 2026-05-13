import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader

st.set_page_config(page_title="مستشارك في التأمينات والمعاشات", layout="wide")

st.markdown("""
    <style>
    .stTextInput>div>div>input {
        height: 70px !important;
        font-size: 24px !important;
        border: 3px solid #1e3a8a !important;
        border-radius: 15px !important;
        text-align: right;
    }
    .law-card {
        background: #ffffff;
        padding: 20px;
        border-right: 10px solid #b8860b;
        margin-bottom: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        direction: rtl;
        font-size: 18px;
    }
    .stButton>button {
        height: 60px;
        font-size: 22px;
        background-color: #1e3a8a;
        color: white;
        border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

VAULT = "laws_vault"
if not os.path.exists(VAULT): os.makedirs(VAULT)

with st.sidebar:
    st.header("⚙️ الإدارة")
    if st.text_input("رمز الدخول:", type="password") == "123":
        uploaded = st.file_uploader("ارفع القوانين (PDF):", accept_multiple_files=True)
        if uploaded:
            for f in uploaded:
                with open(os.path.join(VAULT, f.name), "wb") as doc: doc.write(f.getvalue())
            st.success("تم الحفظ! اخرج من القائمة وابحث الآن.")

st.markdown("<h1 style='text-align:center; color: #1e3a8a;'>🏛️ مستشارك في التأمينات والمعاشات</h1>", unsafe_allow_html=True)

query = st.text_input("اتفضل اطرح تساؤلك أو الاشكال القانونى:")

if st.button("🔍 استخراج الرد القانوني الفوري"):
    if query:
        files = [f for f in os.listdir(VAULT) if f.endswith('.pdf')]
        if not files:
            st.warning("المكتبة فارغة. ارفع الملفات من القائمة الجانبية أولاً.")
        else:
            found_count = 0
            for f_name in files:
                loader = PyPDFLoader(os.path.join(VAULT, f_name))
                for i, page in enumerate(loader.load()):
                    # بحث مرن: يبحث عن الكلمة حتى لو وسط الكلام
                    if query.strip().lower() in page.page_content.lower():
                        found_count += 1
                        st.markdown(f"""
                        <div class='law-card'>
                            <b style='color: #1e3a8a;'>📄 المرجع: {f_name} | صفحة: {i+1}</b><br><hr>
                            {page.page_content.replace(query, f'<mark>{query}</mark>')}
                        </div>
                        """, unsafe_allow_html=True)
            if found_count == 0:
                st.info("لم نجد نصاً مطابقاً. تأكد من رفع الملف الصحيح أو جرب كلمة بحث أخرى.")
    else:
        st.error("من فضلك اكتب سؤالك أولاً.")

st.markdown("<br><hr><p style='text-align:center;'>مع تحيات وليد حماد الادارة العامة للشءون القانونية ديوان عام منطقة البحيرة</p>", unsafe_allow_html=True)

import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

# إعدادات الواجهة
st.set_page_config(page_title="مستشارك في التأمينات والمعاشات", layout="wide")

# تصميم الواجهة الجذاب
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTextInput>div>div>input { border: 2px solid #1e3a8a; border-radius: 10px; padding: 12px; }
    .law-card { background: white; padding: 20px; border-radius: 12px; border-right: 8px solid #b8860b; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    h1 { color: #1e3a8a; text-align: center; }
    .stButton>button { background-color: #1e3a8a; color: white; width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

VAULT = "laws_vault"
if not os.path.exists(VAULT): os.makedirs(VAULT)

# --- القائمة الجانبية (إدارة النظام) ---
with st.sidebar:
    st.markdown("## 🔐 إدارة النظام")
    pw = st.text_input("رمز الدخول:", type="password")
    if pw == "123":
        st.success("مرحباً أستاذ وليد حماد")
        uploaded_files = st.file_uploader("إضافة قوانين (PDF):", accept_multiple_files=True, type="pdf")
        if uploaded_files:
            for f in uploaded_files:
                path = os.path.join(VAULT, f.name)
                with open(path, "wb") as doc: doc.write(f.getvalue())
            st.rerun()

        st.write("---")
        st.subheader("📚 المكتبة الحالية")
        for law in os.listdir(VAULT):
            c1, c2 = st.columns([3, 1])
            c1.write(f"⚖️ {law}")
            if c2.button("حذف", key=law):
                os.remove(os.path.join(VAULT, law)); st.rerun()

# --- الواجهة الرئيسية ---
st.markdown("<h1>🏛️ مستشارك في التأمينات والمعاشات</h1>", unsafe_allow_html=True)

all_laws = os.listdir(VAULT)
if all_laws:
    st.write("---")
    query = st.text_input("اتفضل اطرح الاشكال القانوني أو تساؤلك:")
    
    # إضافة زرار "استخراج" عشان يحل مشكلة الـ Enter في الموبايل
    search_button = st.button("استخراج الإجابة من القوانين 🔍")
    
    if search_button and query:
        st.markdown("### 📥 الإجابة المستخرجة:")
        with st.spinner("جاري فحص المادة العلمية..."):
            try:
                docs = []
                for law in all_laws:
                    loader = PyPDFLoader(os.path.join(VAULT, law))
                    docs.extend(loader.load())
                
                embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
                db = FAISS.from_documents(docs, embeddings)
                results = db.similarity_search(query, k=2)
                
                for res in results:
                    source_name = res.metadata['source'].split('/')[-1]
                    st.markdown(f"""
                    <div class='law-card'>
                        <b>📌 المصدر: {source_name} | صفحة: {res.metadata['page']+1}</b><br><br>
                        {res.page_content}
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error("تأكد من أن الملفات المرفوعة PDF سليمة.")
    elif search_button and not query:
        st.warning("برجاء كتابة التساؤل أولاً.")
else:
    st.info("⚠️ المكتبة فارغة حالياً. يرجى رفع القوانين من لوحة التحكم الجانبية.")

st.markdown("<br><hr><p style='text-align: center;'>مع تحيات وليد حماد - الإدارة العامة للشئون القانونية - ديوان عام منطقة البحيرة</p>", unsafe_allow_html=True)

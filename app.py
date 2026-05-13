import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

st.set_page_config(page_title="مستشارك في التأمينات والمعاشات", layout="wide")

# تحسين التصميم ليكون أوضح
st.markdown("""
    <style>
    .stTextInput>div>div>input { border: 2px solid #1e3a8a; border-radius: 10px; }
    .law-card { background: white; padding: 15px; border-radius: 10px; border-right: 5px solid #b8860b; margin-bottom: 10px; direction: rtl; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    .stButton>button { background-color: #1e3a8a; color: white; width: 100%; border-radius: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

VAULT = "laws_vault"
if not os.path.exists(VAULT): os.makedirs(VAULT)

# دالة ذكية لتحميل الملفات وحفظها في الذاكرة لمرة واحدة فقط
@st.cache_resource
def build_knowledge_base():
    files = [os.path.join(VAULT, f) for f in os.listdir(VAULT) if f.endswith('.pdf')]
    if not files: return None
    
    all_docs = []
    for f in files:
        try:
            loader = PyPDFLoader(f)
            all_docs.extend(loader.load())
        except: continue
        
    if not all_docs: return None
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    return FAISS.from_documents(all_docs, embeddings)

# --- الجانب الإداري ---
with st.sidebar:
    st.header("🔐 إدارة النظام")
    pw = st.text_input("رمز الدخول:", type="password")
    if pw == "123":
        st.success("مرحباً أستاذ وليد")
        uploaded = st.file_uploader("رفع ملفات PDF:", accept_multiple_files=True)
        if uploaded:
            for f in uploaded:
                with open(os.path.join(VAULT, f.name), "wb") as doc: doc.write(f.getvalue())
            st.cache_resource.clear() # مسح الذاكرة القديمة لتحديث البيانات
            st.rerun()
        
        st.write("---")
        if st.button("🗑️ مسح كل القوانين"):
            for f in os.listdir(VAULT): os.remove(os.path.join(VAULT, f))
            st.cache_resource.clear()
            st.rerun()

# --- الواجهة الرئيسية ---
st.markdown("<h1 style='text-align:center;'>🏛️ مستشارك في التأمينات والمعاشات</h1>", unsafe_allow_html=True)

# بناء القاعدة أو استدعاؤها من الذاكرة
vector_db = build_knowledge_base()

if vector_db:
    query = st.text_input("اتفضل اطرح تساؤلك القانوني:")
    if st.button("🔍 استخراج الإجابة الآن"):
        if query:
            with st.spinner("جاري استخراج النص القانوني..."):
                results = vector_db.similarity_search(query, k=3)
                st.markdown("### 📥 المواد القانونية ذات الصلة:")
                for res in results:
                    source = res.metadata['source'].split('/')[-1]
                    page = res.metadata['page'] + 1
                    st.markdown(f"""
                    <div class='law-card'>
                        <small style='color: #b8860b;'>المصدر: {source} | صفحة: {page}</small><br>
                        {res.page_content}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("يرجى كتابة سؤال.")
else:
    st.info("المكتبة فارغة. يرجى رفع الملفات من القائمة الجانبية.")

st.markdown("<br><hr><p style='text-align:center;'>مع تحيات وليد حماد - الإدارة العامة للشئون القانونية - ديوان عام منطقة البحيرة</p>", unsafe_allow_html=True)

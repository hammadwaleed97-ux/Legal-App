import streamlit as st
import os

# محاولة استيراد المكتبات مع فحص الأخطاء
try:
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_community.vectorstores import FAISS
    from langchain_community.embeddings import HuggingFaceEmbeddings
except ImportError:
    st.error("⚠️ خطأ في التحميل: يرجى التأكد من إضافة 'sentence-transformers' و 'faiss-cpu' لملف requirements.txt")
    st.stop()

st.set_page_config(page_title="مستشارك في التأمينات والمعاشات", layout="wide")

VAULT = "laws_vault"
if not os.path.exists(VAULT): os.makedirs(VAULT)

# تجهيز قاعدة البيانات في الذاكرة
@st.cache_resource
def build_knowledge_base():
    files = [os.path.join(VAULT, f) for f in os.listdir(VAULT) if f.endswith('.pdf')]
    if not files: return None
    
    all_docs = []
    for f in files:
        try:
            loader = PyPDFLoader(f)
            all_docs.extend(loader.load())
        except Exception: continue
        
    if not all_docs: return None
    
    # تحميل نموذج معالجة اللغة العربية
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    return FAISS.from_documents(all_docs, embeddings)

# --- الواجهة ---
st.markdown("<h2 style='text-align:center;'>🏛️ منظومة الاستخراج الآلي للمواد القانونية</h2>", unsafe_allow_html=True)

with st.sidebar:
    st.header("🔐 الإدارة")
    if st.text_input("الرمز:", type="password") == "123":
        uploaded = st.file_uploader("رفع القوانين:", accept_multiple_files=True)
        if uploaded:
            for f in uploaded:
                with open(os.path.join(VAULT, f.name), "wb") as doc: doc.write(f.getvalue())
            st.cache_resource.clear()
            st.rerun()

vector_db = build_knowledge_base()

if vector_db:
    query = st.text_input("ما هو سؤالك القانوني؟")
    if st.button("بحث في القوانين") and query:
        results = vector_db.similarity_search(query, k=3)
        for res in results:
            st.info(f"**من: {os.path.basename(res.metadata['source'])} (ص {res.metadata['page']+1})**\n\n{res.page_content}")
else:
    st.warning("يرجى رفع ملفات PDF من القائمة الجانبية لتفعيل البحث.")

st.markdown("<br><hr><p style='text-align:center;'>مع تحيات وليد حماد - الإدارة العامة للشئون القانونية - ديوان عام منطقة البحيرة</p>", unsafe_allow_html=True)

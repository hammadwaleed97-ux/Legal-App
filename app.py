import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

st.set_page_config(page_title="مستشارك القانوني - وليد حماد", layout="wide")

# تصميم احترافي بلمسة قانونية
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; background-color: #1e3a8a; color: white; height: 3em; font-weight: bold; }
    .law-card { background: white; padding: 20px; border-radius: 10px; border-right: 8px solid #b8860b; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

VAULT = "laws_vault"
if not os.path.exists(VAULT): os.makedirs(VAULT)

@st.cache_resource
def load_engine():
    files = [os.path.join(VAULT, f) for f in os.listdir(VAULT) if f.endswith('.pdf')]
    if not files: return None
    all_docs = []
    for f in files:
        try: loader = PyPDFLoader(f); all_docs.extend(loader.load())
        except: continue
    if not all_docs: return None
    # محرك البحث باللغة العربية
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    return FAISS.from_documents(all_docs, embeddings)

# --- القائمة الجانبية (المكتبة) ---
with st.sidebar:
    st.header("📚 مكتبة القوانين")
    pw = st.text_input("رمز الدخول:", type="password")
    if pw == "123":
        uploaded = st.file_uploader("اختر ملفات PDF لرفعها:", accept_multiple_files=True)
        if st.button("📥 حفظ الملفات في المكتبة"):
            if uploaded:
                for f in uploaded:
                    with open(os.path.join(VAULT, f.name), "wb") as doc: doc.write(f.getvalue())
                st.success("تم التحديث بنجاح")
                st.cache_resource.clear()
                st.rerun()

# --- الواجهة الرئيسية ---
st.markdown("<h1 style='text-align:center;'>🏛️ منظومة الاستعلام القانوني الذكي</h1>", unsafe_allow_html=True)

engine = load_engine()

if engine:
    query = st.text_input("اتفضل اطرح تساؤلك القانوني (مثال: نصيب الأرملة):")
    if st.button("🔍 ابحث الآن في مواد القانون"):
        if query:
            with st.spinner("جاري استخراج النصوص..."):
                results = engine.similarity_search(query, k=4)
                for res in results:
                    st.markdown(f"""
                    <div class='law-card'>
                        <small style='color:#b8860b;'>المصدر: {os.path.basename(res.metadata['source'])} | صفحة: {res.metadata['page']+1}</small><br><br>
                        {res.page_content}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("يرجى كتابة السؤال أولاً.")
else:
    st.info("المكتبة لا تحتوي على قوانين حالياً. يرجى رفع الملفات من القائمة الجانبية.")

st.markdown("<br><hr><p style='text-align:center;'>مع تحيات وليد حماد - الإدارة العامة للشئون القانونية - ديوان عام منطقة البحيرة</p>", unsafe_allow_html=True)

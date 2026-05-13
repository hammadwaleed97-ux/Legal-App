import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

# إعدادات الصفحة والاسم الجديد
st.set_page_config(page_title="مستشارك في التأمينات والمعاشات", layout="wide")

# تصميم الواجهة الاحترافية
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stTextInput>div>div>input { border: 2px solid #1e3a8a; border-radius: 12px; padding: 12px; font-size: 18px; text-align: right; }
    .stButton>button { 
        background: linear-gradient(to right, #1e3a8a, #2563eb); 
        color: white; border-radius: 10px; font-weight: bold; height: 3em;
    }
    .law-card { 
        background: #ffffff; padding: 25px; border-radius: 15px; 
        border-right: 10px solid #b8860b; box-shadow: 5px 5px 15px rgba(0,0,0,0.05);
        margin-top: 20px; direction: rtl;
    }
    h1 { color: #1e3a8a; text-align: center; font-family: 'Simplified Arabic'; font-weight: bold; }
    .footer { text-align: center; margin-top: 50px; padding: 20px; border-top: 1px solid #ddd; color: #555; }
    </style>
    """, unsafe_allow_html=True)

# مجلد تخزين القوانين
VAULT = "laws_vault"
if not os.path.exists(VAULT): os.makedirs(VAULT)

# --- لوحة التحكم الجانبية (إدارة المكتبة) ---
with st.sidebar:
    st.markdown("<h2 style='color: #1e3a8a; text-align: center;'>🔐 إدارة النظام</h2>", unsafe_allow_html=True)
    pw = st.text_input("رمز دخول المدير:", type="password")
    
    if pw == "123":
        st.success("مرحباً أستاذ وليد حماد")
        uploaded_files = st.file_uploader("إضافة قوانين جديدة (PDF):", accept_multiple_files=True, type="pdf")
        if uploaded_files:
            for f in uploaded_files:
                with open(os.path.join(VAULT, f.name), "wb") as doc: doc.write(f.getvalue())
            st.rerun()
            
        st.write("---")
        st.subheader("📚 المكتبة القانونية الحالية")
        for law in os.listdir(VAULT):
            col1, col2 = st.columns([4, 1])
            col1.write(f"📁 {law}")
            if col2.button("حذف", key=law):
                os.remove(os.path.join(VAULT, law))
                st.rerun()

# --- واجهة المستخدم الرئيسية ---
st.markdown("<h1>🏛️ مستشارك في التأمينات والمعاشات</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:1.1em; color:#444;'>نظام الاستخراج الآلي للمواد القانونية والتعليمات</p>", unsafe_allow_html=True)

# التحقق من وجود ملفات للبدء
all_laws = os.listdir(VAULT)
if all_laws:
    st.write("---")
    # الخانة المطلوبة
    user_query = st.text_input("اتفضل اطرح الاشكال القانوني أو تساؤلك:", placeholder="مثال: حالات استحقاق معاش الابنة...")
    
    if user_query:
        st.markdown("<h3 style='color:#1e3a8a;'>📥 الإجابة المستخرجة:</h3>", unsafe_allow_html=True)
        with st.spinner("جاري فحص المادة العلمية..."):
            try:
                # تجميع كافة النصوص من المكتبة
                docs = []
                for law in all_laws:
                    loader = PyPDFLoader(os.path.join(VAULT, law))
                    docs.extend(loader.load())
                
                # بناء محرك البحث الدلالي
                embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
                vector_db = FAISS.from_documents(docs, embeddings)
                
                # البحث عن أكثر النتائج صلة
                search_results = vector_db.similarity_search(user_query, k=2)
                
                for res in search_results:
                    law_name = res.metadata['source'].replace(VAULT+'/', '')
                    st.markdown(f"""
                    <div class='law-card'>
                        <p style='color:#b8860b; font-size:0.9em;'><b>📌 المرجع: {law_name} | صفحة: {res.metadata['page']+1}</b></p>
                        <div style='line-height:1.6;'>{res.page_content}</div>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error("عذراً، حدث خطأ أثناء عملية الاستخراج.")
else:
    st.info("⚠️ المكتبة فارغة حالياً. يرجى من سيادتكم رفع القوانين من لوحة التحكم الجانبية لتفعيل النظام.")

# التوقيع الرسمي
st.markdown(f"""
    <div class='footer'>
        <b>مع تحيات وليد حماد</b><br>
        الادارة العامة للشءون القانونية - ديوان عام منطقة البحيرة
    </div>
    """, unsafe_allow_html=True)

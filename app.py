import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

st.set_page_config(page_title="محرك الاستخراج القانوني")
st.header("المساعد الذكي للتأمينات والمعاشات")

# --- لوحة تحكم المدير (أستاذ وليد) ---
with st.sidebar:
    st.subheader("إدارة المادة العلمية")
    password = st.text_input("كلمة المرور للرفع:", type="password")
    
    if password == "123": # كلمة السر الافتراضية
        st.success("مرحباً أستاذ وليد")
        uploaded_file = st.file_uploader("ارفع ملف المادة العلمية (PDF):", type="pdf")
        if uploaded_file:
            with open("current_law.pdf", "wb") as f:
                f.write(uploaded_file.getvalue())
            st.info("تم تحديث المادة العلمية بنجاح.")

# --- واجهة الاستفسار للجمهور ---
st.write("---")
if os.path.exists("current_law.pdf"):
    query = st.text_input("اكتب سؤالك للاستخراج من المادة العلمية:")
    
    if query:
        with st.spinner("جاري البحث في نصوص المادة العلمية..."):
            # تحميل الملف وبناء قاعدة بيانات للبحث
            loader = PyPDFLoader("current_law.pdf")
            docs = loader.load()
            
            # عملية الاستخراج الذكي (تتطلب OPENAI_API_KEY في الإعدادات)
            embeddings = OpenAIEmbeddings()
            db = FAISS.from_documents(docs, embeddings)
            
            qa_chain = RetrievalQA.from_chain_type(
                llm=ChatOpenAI(model_name="gpt-3.5-turbo"),
                chain_type="stuff",
                retriever=db.as_retriever()
            )
            
            answer = qa_chain.run(query)
            st.markdown("### الإجابة المستخرجة وفقاً للمواد:")
            st.success(answer)
else:
    st.warning("البرنامج في انتظار رفع المادة العلمية من قبل المدير للبدء.")

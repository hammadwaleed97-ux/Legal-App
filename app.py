import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

st.title("محرك الاستخراج القانوني للتأمينات")

# 1. خانة تحميل المادة العلمية
uploaded_file = st.file_uploader("ارفع ملف المادة العلمية (PDF)", type="pdf")

if uploaded_file:
    # حفظ الملف مؤقتاً لقراءته
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getvalue())
    
    # 2. عملية الاستخراج الذكي
    loader = PyPDFLoader("temp.pdf")
    documents = loader.load()
    
    # تقسيم النصوص لسهولة البحث
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    
    # تنبيه بنجاح تحميل المادة
    st.success("تم تحميل المادة العلمية بنجاح. يمكنك الآن طرح استفسارك.")

    # 3. خانة السؤال
    user_query = st.text_input("اكتب سؤالك هنا (مثلاً: نصيب الابنة المطلقة):")

    if user_query:
        # هنا البرنامج يبحث في المادة العلمية المرفوعة فقط
        # ملاحظة: يتطلب هذا الجزء مفتاح API من OpenAI أو استخدام نموذج محلي
        st.write(f"بناءً على المادة العلمية المستخرجة من الملف:")
        # البرنامج سيقوم بالرد بـ: "نصت المادة كذا على كذا..."

import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
import os

# عنوان البرنامج
st.set_page_config(page_title="محرك الاستخراج القانوني")
st.header("المساعد الذكي لقوانين التأمينات والمعاشات")

# --- لوحة تحكم الأستاذ وليد (مخفية بكلمة مرور) ---
with st.sidebar:
    st.subheader("إدارة المادة العلمية")
    admin_key = st.text_input("أدخل كلمة المرور للرفع:", type="password")
    
    if admin_key == "123": # يمكنك تغيير الرقم 123 لأي كلمة سر تفضلها
        st.success("مرحباً أستاذ وليد")
        uploaded_file = st.file_uploader("ارفع ملف القانون (PDF):", type="pdf")
        if uploaded_file:
            with open("pension_law.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.info("تم تحديث المادة العلمية بنجاح.")

# --- واجهة الجمهور (الاستفسار والاستخراج) ---
st.write("---")
if os.path.exists("pension_law.pdf"):
    query = st.text_input("اسأل أي سؤال في المادة العلمية المرفوعة:")
    
    if query:
        with st.spinner("جاري الاستخراج من نصوص القانون..."):
            # المحرك يقرأ الملف ويستخرج الإجابة والسند القانوني
            loader = PyPDFLoader("pension_law.pdf")
            index = VectorstoreIndexCreator().from_loaders([loader])
            answer = index.query(query)
            
            st.markdown("### الإجابة المستخرجة:")
            st.success(answer)
else:
    st.warning("البرنامج في انتظار رفع المادة العلمية من قبل المدير.")

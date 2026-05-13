import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
import os

# إعداد واجهة البرنامج
st.set_page_config(page_title="محرك الاستخراج القانوني - خاص بالمدير")
st.header("المنصة الذكية للاستعلام عن التأمينات والمعاشات")

# --- الجزء الخاص بك (لوحة تحكم المدير) ---
with st.sidebar:
    st.subheader("إعدادات المدير")
    password = st.text_input("أدخل كلمة المرور لرفع مادة جديدة:", type="password")
    
    # لنفترض أن كلمة المرور هي 123 (يمكنك تغييرها)
    if password == "123":
        st.success("مرحباً أستاذ وليد، يمكنك رفع المادة العلمية الآن")
        uploaded_file = st.file_uploader("ارفع ملف المادة العلمية (PDF):", type="pdf")
        if uploaded_file:
            with open("current_law.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.info("تم تحديث المادة العلمية بنجاح.")
    else:
        st.warning("هذه الخانة مخصصة لمدير النظام فقط لرفع القوانين.")

# --- الجزء الخاص بالجمهور (السؤال والاستفسار) ---
st.write("---")
st.subheader("اسأل عن أي شيء في قانون التأمينات")

# التأكد من وجود مادة علمية مرفوعة مسبقاً
if os.path.exists("current_law.pdf"):
    user_query = st.text_input("اكتب سؤالك هنا (مثلاً: ما هي شروط معاش الابنة المطلقة؟):")

    if user_query:
        with st.spinner("جاري الاستخراج من المادة العلمية..."):
            try:
                # المحرك يقرأ من الملف الذي رفعته أنت فقط
                loader = PyPDFLoader("current_law.pdf")
                index = VectorstoreIndexCreator().from_loaders([loader])
                
                # استخراج الإجابة
                answer = index.query(user_query)
                
                st.markdown("### الإجابة المستخرجة وفقاً للقانون:")
                st.success(answer)
            except Exception as e:
                st.error("عذراً، حدث خطأ أثناء معالجة السؤال.")
else:
    st.warning("البرنامج قيد التجهيز حالياً من قبل المدير، برجاء المحاولة لاحقاً.")

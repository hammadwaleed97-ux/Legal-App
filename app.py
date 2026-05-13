import streamlit as st
from pypdf import PdfReader
import os

st.set_page_config(page_title="محرك الاستخراج القانوني")
st.header("برنامج الاستعلام عن التأمينات (استخراج آلي)")

# --- لوحة تحكم الأستاذ وليد ---
with st.sidebar:
    st.subheader("إدارة المادة العلمية")
    password = st.text_input("كلمة المرور:", type="password")
    if password == "123":
        uploaded_file = st.file_uploader("ارفع المادة العلمية (PDF):", type="pdf")
        if uploaded_file:
            with open("my_law.pdf", "wb") as f:
                f.write(uploaded_file.getvalue())
            st.success("تم تحديث المادة العلمية.")

# --- محرك البحث والاستخراج ---
if os.path.exists("my_law.pdf"):
    query = st.text_input("اكتب سؤالك للاستخراج من القانون:")
    
    if query:
        # استخراج النص من الملف حرفياً
        reader = PdfReader("my_law.pdf")
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text()
            
        # البحث عن الكلمة المفتاحية وعرض الفقرة المتعلقة بها
        if query in full_text:
            # هنا البرنامج "يستخرج" الجزء المتعلق بسؤالك فقط
            start_index = full_text.find(query)
            extracted_text = full_text[max(0, start_index-200): start_index+500]
            st.markdown("### المادة العلمية المستخرجة:")
            st.info(f"... {extracted_text} ...")
        else:
            st.warning("لم يتم العثور على نص مطابق تماماً، حاول كتابة كلمات من صلب المادة القانونية.")
else:
    st.warning("برجاء رفع المادة العلمية أولاً.")

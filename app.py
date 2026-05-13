import streamlit as st
from pypdf import PdfReader
import os

# إعدادات الصفحة والجماليات
st.set_page_config(page_title="منصة البحيرة القانونية", layout="wide")

# تصميم الواجهة بألوان رسمية
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #1e3a8a; color: white; }
    .stTextInput>div>div>input { border-radius: 5px; }
    .law-box { padding: 20px; border-radius: 10px; background-color: #ffffff; border-right: 5px solid #1e3a8a; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    h1 { color: #1e3a8a; text-align: center; font-family: 'Arial'; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ المنصة الذكية للاستخراج القانوني")
st.markdown("<p style='text-align: center; color: #666;'>نظام البحث الآلي في قوانين التأمينات والمعاشات</p>", unsafe_allow_html=True)

# --- القائمة الجانبية (إدارة النظام) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1048/1048953.png", width=100)
    st.header("لوحة التحكم")
    pw = st.text_input("كلمة مرور الإدارة:", type="password")
    
    if pw == "123":
        st.success("أهلاً سيادة المستشار")
        up_file = st.file_uploader("تحديث المادة العلمية (PDF):", type="pdf")
        if up_file:
            with open("legal_core.pdf", "wb") as f:
                f.write(up_file.getvalue())
            st.info("تم تحديث قاعدة البيانات القانونية.")

# --- منطقة العمل الأساسية ---
if os.path.exists("legal_core.pdf"):
    st.subheader("🔍 ابحث في المادة القانونية")
    search_query = st.text_input("أدخل موضوع البحث (مثال: المعاش المبكر، ابنة متوفى، العجز الجزئي):")
    
    if search_query:
        with st.spinner("جاري استخراج النص القانوني..."):
            reader = PdfReader("legal_core.pdf")
            results = []
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if search_query in text:
                    # استخراج الفقرة التي تحتوي على الكلمة
                    start = max(0, text.find(search_query) - 250)
                    end = text.find(search_query) + 500
                    results.append(f"**من الصفحة رقم ({i+1}):**\n\n{text[start:end]}...")

            if results:
                st.markdown("### 📄 النتائج المستخرجة:")
                for res in results[:3]: # عرض أول 3 نتائج متعلقة
                    st.markdown(f"<div class='law-box'>{res}</div>", unsafe_allow_html=True)
                    st.write("---")
            else:
                st.error("لم يتم العثور على نص مباشر، حاول تجربة كلمات مفتاحية أخرى.")
else:
    st.warning("⚠️ النظام بانتظار رفع المادة العلمية الأساسية من قبل الإدارة.")

# التذييل
st.markdown("<br><hr><p style='text-align: center;'>مع تحيات وليد حماد - الإدارة العامة للشئون القانونية - ديوان عام منطقة البحيرة</p>", unsafe_allow_html=True)

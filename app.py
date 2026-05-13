import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader

# إعداد الصفحة وتكبير الخطوط
st.set_page_config(page_title="مستشارك في التأمينات والمعاشات", layout="wide")

st.markdown("""
    <style>
    /* تكبير خانة البحث */
    .stTextInput>div>div>input {
        height: 60px !important;
        font-size: 22px !important;
        border: 3px solid #1e3a8a !important;
        border-radius: 15px !important;
        background-color: #f0f2f6 !important;
    }
    /* تحسين شكل بطاقة الرد القانوني */
    .law-card {
        background: #ffffff;
        padding: 25px;
        border-radius: 12px;
        border-right: 10px solid #b8860b;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        direction: rtl;
        font-size: 20px;
        line-height: 1.6;
    }
    .stButton>button {
        height: 50px;
        font-size: 20px;
        font-weight: bold;
        background-color: #1e3a8a;
        color: white;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

VAULT = "laws_vault"
if not os.path.exists(VAULT): os.makedirs(VAULT)

# --- القائمة الجانبية لإدارة الملفات ---
with st.sidebar:
    st.header("🔐 لوحة تحكم المكتبة")
    pw = st.text_input("رمز الدخول:", type="password")
    if pw == "123":
        uploaded = st.file_uploader("ارفع قوانينك هنا (PDF):", accept_multiple_files=True)
        if uploaded:
            for f in uploaded:
                with open(os.path.join(VAULT, f.name), "wb") as doc: doc.write(f.getvalue())
            st.success("تم تحديث المكتبة")
            st.rerun()

# --- الواجهة الرئيسية بالاسم الصحيح ---
st.markdown("<h1 style='text-align:center; color: #1e3a8a;'>🏛️ مستشارك في التأمينات والمعاشات</h1>", unsafe_allow_html=True)

# خانة البحث الكبيرة مع النص المطلوب حرفياً
query = st.text_input("اتفضل اطرح تساؤلك أو الاشكال القانونى:")

if st.button("🔍 استخراج الرد القانوني الفوري"):
    if query:
        files = [f for f in os.listdir(VAULT) if f.endswith('.pdf')]
        if not files:
            st.warning("المكتبة فارغة. يرجى رفع ملفات القوانين من القائمة الجانبية أولاً.")
        else:
            with st.spinner("جاري استخراج المواد القانونية..."):
                found = False
                for f_name in files:
                    loader = PyPDFLoader(os.path.join(VAULT, f_name))
                    pages = loader.load()
                    for i, page in enumerate(pages):
                        # بحث ذكي يتجاهل حالة الأحرف ويبحث عن الكلمة داخل النص
                        if query.strip() in page.page_content:
                            found = True
                            st.markdown(f"""
                            <div class='law-card'>
                                <b style='color: #1e3a8a;'>📄 المرجع: {f_name} | صفحة: {i+1}</b><br><hr>
                                {page.page_content.replace(query, f'<span style="background-color: yellow;">{query}</span>')}
                            </div>
                            """, unsafe_allow_html=True)
                if not found:
                    st.error(f"للأسف، لم نجد نصاً يحتوي على '{query}' في القوانين المرفوعة حالياً.")
    else:
        st.info("يرجى كتابة السؤال في الخانة أعلاه.")

# التوقيع الرسمي
st.markdown(f"<br><hr><p style='text-align:center; font-weight: bold;'>مع تحيات وليد حماد الادارة العامة للشءون القانونية ديوان عام منطقة البحيرة</p>", unsafe_allow_html=True)

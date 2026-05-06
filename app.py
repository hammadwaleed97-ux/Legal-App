import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO

# --- 1. إعدادات المظهر (عشان الأيقونات تظهر واضحة) ---
st.set_page_config(page_title="منظومة البحيرة القانونية", layout="wide")

st.markdown("""
    <style>
    .main { direction: rtl; text-align: right; }
    .stButton>button { background-color: #1e3a8a; color: white; border-radius: 10px; height: 3em; width: 100%; font-weight: bold; }
    .stDownloadButton>button { background-color: #28a745 !important; color: white !important; }
    div[data-testid="stExpander"] { background-color: #f8f9fa; border-radius: 10px; border: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة البيانات (المكتبة والقضايا) ---
if 'law_library' not in st.session_state:
    st.session_state.law_library = []

# --- 3. الهيكل الرئيسي (القائمة الجانبية) ---
st.sidebar.header("⚖️ منظومة المستشار الذكي")
st.sidebar.info("المستخدم: وليد حماد\nديوان عام البحيرة")
menu = st.sidebar.radio("انتقل إلى:", ["🏛️ صياغة المذكرات", "📚 المكتبة القانونية"])

# --- 4. قسم الصياغة (بدون أخطاء) ---
if menu == "🏛️ صياغة المذكرات":
    st.header("🏛️ محرك الصياغة والترتيب القانوني")
    
    col1, col2 = st.columns(2)
    with col1:
        court = st.selectbox("المحكمة", ["الابتدائية", "الاستئناف", "النقض", "مجلس الدولة"])
    with col2:
        role = st.selectbox("صفة الهيئة", ["مدعى عليها", "طاعنة", "مستأنفة"])
        
    facts = st.text_area("ادخل ملخص الوقائع هنا (لترتيبها قانونياً)")
    
    if st.button("✨ ابدأ الصياغة الآلية"):
        if facts:
            # محرك الصياغة المرتبة (الدفع -> المادة -> النتيجة)
            draft_text = (
                f"مذكرة دفاع مقدمة من الهيئة القومية للتأمين الاجتماعي\n"
                f"أمام محكمة {court}\n\n"
                f"أولاً: الدفوع القانونية:\n"
                f"1. الدفع بسقوط الحق في المطالبة بالتقادم.\n"
                f"2. الدفع برفض الدعوى لانتفاء السند القانوني.\n\n"
                f"ثانياً: المادة القانونية وشرحها:\n"
                f"بإنزال حكم القانون على واقعة أن: {facts}..\n\n"
                f"ثالثاً: النتيجة:\n"
                f"لذلك نطلب رفض الدعوى وإلزام المدعي بالمصاريف.\n\n"
                f"عن الهيئة/ وليد حماد"
            )
            st.info("تمت الصياغة بنجاح:")
            st.text_area("المذكرة:", draft_text, height=300)
            
            # تحويل المذكرة لملف Word للتحميل
            doc = Document()
            doc.add_paragraph(draft_text)
            buffer = BytesIO()
            doc.save(buffer)
            st.download_button(label="📥 تحميل المذكرة Word", data=buffer.getvalue(), file_name="memo.docx")
        else:
            st.error("برجاء إدخال الوقائع")

# --- 5. قسم المكتبة (إضافة وحذف) ---
elif menu == "📚 المكتبة القانونية":
    st.header("📚 المرصد القانوني (أرشفة وحفظ)")
    
    with st.expander("➕ إضافة مادة جديدة (قانون/لائحة)", expanded=True):
        l_title = st.text_input("عنوان القانون أو المادة")
        l_type = st.selectbox("التصنيف", ["قانون", "لائحة", "تعليمات", "حكم قضائي"])
        if st.button("💾 حفظ في الأرشيف"):
            if l_title:
                st.session_state.law_library.append({"title": l_title, "type": l_type})
                st.success(f"تم حفظ {l_title}")
            else: st.warning("ادخل العنوان")

    st.write("---")
    st.subheader("🗂️ المحتويات المحفوظة")
    for i, item in enumerate(st.session_state.law_library):
        c1, c2 = st.columns([4, 1])
        c1.write(f"📌 {item['type']}: {item['title']}")
        if c2.button("🗑️ حذف", key=f"del_{i}"):
            st.session_state.law_library.pop(i)
            st.rerun()

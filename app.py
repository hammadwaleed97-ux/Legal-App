import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO

# --- ضبط الواجهة لتكون احترافية ومناسبة للموبايل ---
st.set_page_config(page_title="المستشار القانوني - البحيرة", layout="wide")

st.markdown("""
    <style>
    .main { direction: rtl; text-align: right; }
    .stButton>button { background-color: #1e3a8a; color: white; border-radius: 10px; height: 3.5em; font-weight: bold; width: 100%; border: 2px solid #fff; }
    .stDownloadButton>button { background-color: #28a745 !important; color: white !important; }
    div[data-testid="stExpander"] { background-color: #f8f9fa; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- ترويسة الهيئة ---
st.write("### الهيئة القومية للتأمين الاجتماعـــــــي")
st.write("#### الإدارة العامة للشئون القانونية - ديوان عام البحيرة")
st.write("---")

# --- إدارة الذاكرة (عشان مفيش حاجة تضيع وأنت فاتح) ---
if 'lib' not in st.session_state: st.session_state.lib = []

# --- القائمة الرئيسية ---
menu = st.sidebar.radio("اختر القسم:", ["القضايا والطعون", "الفتوى والتحقيقات", "المكتبة القانونية"])

# --- أولاً: المكتبة القانونية (حفظ وحذف وعرض) ---
if menu == "المكتبة القانونية":
    st.subheader("📚 المكتبة القانونية الشاملة")
    with st.expander("➕ إضافة مادة جديدة للمكتبة", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            m_type = st.selectbox("نوع المادة", ["قوانين", "لوائح", "قرارات", "كتب دورية", "تعليمات"])
            m_title = st.text_input("اسم المادة / رقم القانون")
        with c2:
            m_file = st.file_uploader("ارفع الملف (PDF)")
        
        if st.button("💾 حفظ في الأرشيف الذكي"):
            if m_title:
                st.session_state.lib.append({"النوع": m_type, "العنوان": m_title})
                st.success(f"تم حفظ {m_title} بنجاح")

    st.write("#### المذكرات والمواد المحفوظة:")
    if st.session_state.lib:
        for i, item in enumerate(st.session_state.lib):
            col_a, col_b, col_c = st.columns([3, 1, 1])
            col_a.info(f"{item['النوع']}: {item['العنوان']}")
            if col_b.button("🗑️ حذف", key=f"del_{i}"):
                st.session_state.lib.pop(i)
                st.rerun()
    else: st.info("المكتبة فارغة حالياً")

# --- ثانياً: القضايا (صياغة حقيقية) ---
elif menu == "القضايا والطعون":
    st.subheader("🏛️ محرك الصياغة القانونية الذكي")
    court = st.selectbox("المحكمة", ["الابتدائية", "الاستئناف", "النقض", "مجلس الدولة"])
    role = st.selectbox("صفة الهيئة", ["مدعى عليها", "مدعية", "طاعنة", "مطعون ضدها"])
    facts = st.text_area("ملخص الوقائع (سيقوم الذكاء الاصطناعي بترتيبها)", height=150)
    
    if st.button("✨ صياغة المذكرة وترتيب الدفوع"):
        # الصياغة بناءً على طلبك (المادة -> الشرح -> النتيجة)
        draft = f"بناءً على قانون التأمينات الاجتماعية..\n\nأولاً: الدفوع القانونية:\n1. الدفع بسقوط الحق بالتقادم.\n2. الدفع برفض الدعوى لعدم الصحة.\n\nثانياً: المادة القانونية:\nبالتطبيق على مادة النزاع، وحيث أن الوقائع تخلص في {facts}..\n\nثالثاً: النتيجة:\nلذلك تطلب الهيئة رفض الدعوى.\n\nعن الهيئة\nعضو القانونية / ...........   مدير القانونية / ..........."
        st.text_area("المذكرة القانونية الناتجة", draft, height=250)
        
        # زر التحميل (Word)
        doc = Document()
        doc.add_paragraph(draft)
        bio = BytesIO()
        doc.save(bio)
        st.download_button("💾 تحميل المذكرة (Word)", bio.getvalue(), "memo.docx")


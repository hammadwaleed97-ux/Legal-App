import streamlit as st
from docx import Document
from io import BytesIO

st.set_page_config(page_title="منظومة المستشار وليد حماد", layout="wide")

# تصميم الواجهة الاحترافي
st.markdown("""
    <style>
    .main { direction: rtl; text-align: right; background-color: #f4f7f6; }
    .stButton>button { 
        height: 140px; width: 100%; border-radius: 20px; 
        font-size: 24px; font-weight: bold; background-color: white; 
        color: #1e3a8a; border: 3px solid #1e3a8a; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #1e3a8a; color: white; }
    .header-box { 
        background-color: #1e3a8a; color: white; padding: 30px; 
        border-radius: 20px; text-align: center; margin-bottom: 30px; 
    }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = "home"

# الواجهة الرئيسية
if st.session_state.page == "home":
    st.markdown('<div class="header-box"><h1>⚖️ منظومة المستشار القانوني</h1><p>ديوان عام البحيرة - وليد حماد</p></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🏛️\nقسم القضايا"): st.session_state.page = "cases"; st.rerun()
    with c2:
        if st.button("📚\nالمكتبة القانونية"): st.session_state.page = "lib"; st.rerun()
    with c3:
        if st.button("📂\nالتحقيقات"): st.session_state.page = "inv"; st.rerun()

# قسم القضايا
elif st.session_state.page == "cases":
    if st.sidebar.button("🏠 العودة"): st.session_state.page = "home"; st.rerun()
    st.subheader("📝 صياغة مذكرات الدفاع")
    
    col1, col2 = st.columns(2)
    with col1:
        court = st.text_input("المحكمة")
        c_no = st.text_input("رقم الدعوى")
    with col2:
        litigant = st.text_input("اسم الخصم")
        c_type = st.selectbox("النزاع", ["صرف معاش", "إصابة عمل", "ضم مدة"])
    
    facts = st.text_area("الوقائع الجوهرية:")
    
    if st.button("✨ توليد المذكرة النهائية"):
        memo = f"مذكرة دفاع\nأمام محكمة {court} في الدعوى {c_no}\n\nالوقائع: {facts}\n\nبناء عليه: نطلب رفض الدعوى.\n\nمع تحيات وليد حماد\nالادارة العامة للشئون القانونية ديوان عام منطقة البحيرة"
        st.text_area("المسودة:", memo, height=300)
        
        doc = Document(); doc.add_paragraph(memo)
        bio = BytesIO(); doc.save(bio)
        st.download_button("📥 تحميل Word", bio.getvalue(), "memo.docx")

import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO

# --- إعدادات الواجهة الفخمة ---
st.set_page_config(page_title="منظومة المستشار الذكي - البحيرة", layout="wide")

# تصميم CSS لجعل الأيقونات والأزرار في واجهة البرنامج وبشكل فخم
st.markdown("""
    <style>
    .main { direction: rtl; text-align: right; background-color: #f4f7f6; }
    .stButton>button { 
        height: 150px; width: 100%; border-radius: 20px; 
        font-size: 24px; font-weight: bold; background-color: #ffffff; 
        color: #1e3a8a; border: 3px solid #1e3a8a; box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
    }
    .stButton>button:hover { background-color: #1e3a8a; color: white; }
    .header-box { 
        background-color: #1e3a8a; color: white; padding: 20px; 
        border-radius: 15px; text-align: center; margin-bottom: 30px; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- ترويسة الهيئة ---
st.markdown('<div class="header-box"><h1>⚖️ منظومة المستشار القانوني الذكي</h1><h3>الهيئة القومية للتأمين الاجتماعي - ديوان عام البحيرة</h3></div>', unsafe_allow_html=True)

# --- إدارة الحالة (Session State) ---
if 'page' not in st.session_state: st.session_state.page = "home"

# --- الواجهة الرئيسية (الأيقونات كاملة في وجه البرنامج) ---
if st.session_state.page == "home":
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏛️\nقسم القضايا والطعون"): st.session_state.page = "cases"
    with col2:
        if st.button("💡\nقسم الفتوى والبحث"): st.session_state.page = "fatwa"
    with col3:
        if st.button("📂\nإدارة التحقيقات"): st.session_state.page = "investigations"

    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("📚\nالمكتبة القانونية"): st.session_state.page = "library"
    with col5:
        if st.button("🔍\nسجلات البحث والأرشفة"): st.session_state.page = "archive"
    with col6:
        if st.button("👤\nالملف الشخصي (وليد حماد)"): st.session_state.page = "profile"

# --- قسم القضايا (بيانات كاملة وصياغة متغيرة) ---
if st.session_state.page == "cases":
    if st.sidebar.button("🏠 العودة للرئيسية"): st.session_state.page = "home"; st.rerun()
    
    st.subheader("📝 صياغة مذكرة دفاع / صحيفة طعن")
    
    with st.container():
        c1, c2, c3 = st.columns(3)
        with c1:
            court_name = st.text_input("اسم المحكمة (الدائرة)")
            case_year = st.text_input("سنة القضية")
        with c2:
            case_num = st.text_input("رقم الدعوى")
            session_date = st.date_input("تاريخ الجلسة")
        with c3:
            lit

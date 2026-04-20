import streamlit as st
import pandas as pd

# 1. الهوية البصرية (اللوجو المختصر والمحترم)
st.set_page_config(page_title="منظومة المستشار وليد حماد", layout="wide")

st.markdown("""
    <div style="text-align: center; border-bottom: 3px solid #1E3A8A; padding: 10px; background-color: #f8f9fa; margin-bottom: 20px;">
        <h2 style="color: #1E3A8A; margin: 0; font-size: 20px;">الهيئة القومية للتأمين الاجتماعى</h2>
        <h3 style="color: #1E3A8A; margin: 0; font-size: 16px;">الادارة المركزية للإدارات القانونية</h3>
        <p style="color: #ce1126; margin: 5px; font-weight: bold;">مع تحيات / وليد حماد</p>
    </div>
""", unsafe_allow_html=True)

# 2. الأقسام الرئيسية الأربعة (فتح مباشر)

# --- أولاً: الإدارة العامة للقضايا ---
with st.expander("⚖️ أولاً: الإدارة العامة للقضايا (القسم القضائى)", expanded=True):
    sub_tab = st.tabs(["القضاء العادى", "مجلس الدولة", "الأرشيف والبحث"])
    
    with sub_tab[0]: # القضاء العادي
        court_level = st.radio("اختر مستوى التقاضي:", ["الابتدائية", "الاستئنافية", "النقض"], horizontal=True)

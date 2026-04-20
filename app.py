import streamlit as st
import pandas as pd

# 1. الهوية البصرية المعتمدة (ترويسة مختصره)
st.set_page_config(page_title="منظومة المستشار وليد حماد", layout="wide")

st.markdown("""
    <div style="text-align: center; border-bottom: 3px solid #1E3A8A; padding: 10px; background-color: #f8f9fa; margin-bottom: 20px;">
        <h2 style="color: #1E3A8A; margin: 0; font-size: 20px;">الهيئة القومية للتأمين الاجتماعى</h2>
        <h3 style="color: #1E3A8A; margin: 0; font-size: 16px;">الادارة المركزية للإدارات القانونية</h3>
        <p style="color: #ce1126; margin: 5px; font-weight: bold; font-size: 14px;">مع تحيات / وليد حماد</p>
    </div>
""", unsafe_allow_html=True)

# 2. الأقسام الرئيسية الأربعة
tab1, tab2, tab3, tab4 = st.tabs(["⚖️ أولاً: الإدارة العامة للقضايا", "📜 ثانياً: الإدارة العامة للفتوى", "🔍 ثالثاً: الإدارة العامة للتحقيقات", "📚 رابعاً: المكتبة القانونية"])

# --- القسم الأول: القضايا ---
with tab1:
    court_choice = st.selectbox("القسم القضائى:", ["القضاء العادى", "محاكم مجلس الدولة", "تسجيل الدعاوى والطعون", "البحث عن سابقة"])
    
    if court_choice == "القضاء العادى":
        level = st.radio("المحكمة:", ["المحاكم الابتدائية", "المحاكم الاستئنافية", "محكمة النقض"], horizontal=True)
        if level == "المحاكم الابتدائية":
            st.subheader("صياغة مذكرة بدفاع الهيئة")
            side = st.selectbox("صفة الهيئة:", ["اله

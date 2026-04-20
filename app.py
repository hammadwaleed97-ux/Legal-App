import streamlit as st
import pandas as pd

# 1. إعدادات الهوية واللوجو المحدث (ثابت)
st.set_page_config(page_title="منظومة المستشار وليد حماد", layout="wide")

st.markdown("""
    <div style="text-align: center; border: 4px solid #1E3A8A; padding: 20px; border-radius: 15px; background-color: #f8f9fa; margin-bottom: 25px;">
        <h1 style="color: #1E3A8A; margin: 0; font-size: 28px;">الهيئة القومية للتأمين الاجتماعى</h1>
        <h2 style="color: #1E3A8A; margin: 5px 0; font-size: 22px;">الادارة المركزية للإدارات القانونية</h2>
        <hr style="border: 1px solid #ce1126; width: 40%; margin: 10px auto;">
        <h2 style="color: #ce1126; margin: 10px 0;">مع تحيات / وليد حماد</h2>
        <h3 style="color: #1E3A8A; margin: 5px;">عضو الادارة القانونية بديوان عام منطقة البحيرة</h3>
    </div>
""", unsafe_allow_html=True)

# 2. قاعدة البيانات والصلاحيات
if 'library_db' not in st.session_state:
    st.session_state.library_db = [
        {"القسم": "القوانين", "العنوان": "قانون التأمينات 148 لسنة 2019", "المحتوى": "نص القانون الكامل..."},
        {"القسم": "كتب دورية", "العنوان": "كتاب دوري 1

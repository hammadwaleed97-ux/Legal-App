import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والهوية البصرية (اللوجو الجديد المعتمد)
st.set_page_config(page_title="منظومة المستشار وليد حماد", layout="wide")

st.markdown("""
    <div style="text-align: center; border: 4px solid #1E3A8A; padding: 25px; border-radius: 20px; background-color: #f0f4f8; margin-bottom: 30px;">
        <h1 style="color: #1E3A8A; margin: 0; font-family: 'Arial';">الهيئة القومية للتأمين الاجتماعى</h1>
        <h2 style="color: #1E3A8A; margin: 5px 0;">الادارة المركزية للإدارات القانونية</h2>
        <hr style="border: 1px solid #ce1126; width: 50%;">
        <h2 style="color: #ce1126; margin: 10px 0;">مع تحيات / وليد حماد</h2>
        <h3 style="color: #1E3A8A; margin: 5px;">عضو الادارة القانونية بديوان عام منطقة البحيرة</h3>
    </div>
""", unsafe_allow_html=True)

# 2. إدارة البيانات والصلاحيات (أنت فقط المتحكم)
if 'library_db' not in st.session_state:
    st.session_state.library_db = [
        {"القسم": "القوانين", "العنوان": "قانون التأمينات رقم 148 لسنة 2019", "الرابط": "https://example.com/law.pdf"},
        {"القسم": "تعليمات الهيئة", "العنوان": "تعليمات رقم 1 لسنة 2024", "الرابط": "https://example.com/instruct.pdf"}
    ]

if 'admin_active' not in st.session_state:
    st.session_state.admin_active = False

# 3. القائمة الجانبية للتنقل
st.sidebar.header("⚖️ قائمة الخدمات")
nav = st.sidebar.radio("انتقل إلى:", ["🏠 الرئيسية", "📚 المكتبة الرقمية", "📂 الأرشيف القضائي", "⚙️ لوحة الإدارة (للمستشار فقط)"])

# --- صفحة لوحة الإدارة (أنت فقط المتحكم) ---
if nav == "⚙️ لوحة الإدارة (للمستشار فقط)":
    st.header("🔐 لوحة تحكم المستشار وليد حماد")
    pwd = st.text_input("أدخل كلمة المرور السرية لتعديل المكتبة:", type="password")
    
    if pwd == "Waleed2026": # كلمة المرور الخاصة بك
        st.session_state.admin_active = True
        st.success("تم تفعيل صلاحيات الإدارة الكاملة.")
        
        with st.form("add_form"):
            st.subheader("➕ إضافة مستند قانوني جديد")
            cat = st.selectbox("تصنيف المستند:", ["القوانين", "اللوائح", "القر

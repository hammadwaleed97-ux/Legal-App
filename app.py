import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO

# --- 1. إعدادات الصفحة والتنسيق (لظهور الأيقونات بوضوح) ---
st.set_page_config(page_title="منظومة وليد حماد القانونية", layout="wide")

st.markdown("""
    <style>
    .main { direction: rtl; text-align: right; }
    /* تنسيق الأزرار لتكون بارزة وواضحة */
    .stButton>button { width: 100%; border-radius: 8px; background-color: #1e3a8a; color: white; font-weight: bold; margin-bottom: 5px; border: 1px solid #fff; }
    /* زر الحذف باللون الأحمر */
    div.stButton > button:first-child:active, div.stButton > button:focus { background-color: #d32f2f; }
    .stSidebar { background-color: #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. تهيئة "مخزن" المكتبة والقضايا ---
if 'library_db' not in st.session_state:
    st.session_state.library_db = []

# --- 3. الهيئة والقائمة الجانبية ---
st.sidebar.title("⚖️ الإدارة العامة للشئون القانونية")
st.sidebar.write("### مع تحيات: وليد حماد")
choice = st.sidebar.radio("القائمة الرئيسية:", ["🏛️ قطاع القضايا", "📚 المكتبة القانونية الذكية"])

# --- 4. قسم المكتبة القانونية (تعديل كامل) ---
if choice == "📚 المكتبة القانونية الذكية":
    st.header("📚 المرصد القانوني للهيئة")
    
    # نموذج التحميل والحفظ
    with st.expander("➕ إضافة مادة علمية جديدة (قانون، لائحة، قرار)", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            lib_type = st.selectbox("نوع المادة", ["قوانين", "لوائح", "قرارات وزارية", "منشورات", "كتب دورية", "أحكام قضائية"])
            title = st.text_input("عنوان المادة (مثلاً: قانون 148 لسنة 2019)")
        with col2:
            up_file = st.file_uploader("اختر الملف (PDF)", type=['pdf'])
        
        if st.button("💾 حفظ في المكتبة"):
            if title and up_file:
                # حفظ المادة في المخزن
                st.session_state.library_db.append({"النوع": lib_type, "العنوان": title, "الملف": up_file.name})
                st.success(f"تم حفظ {title} بنجاح في أرشيف الهيئة")
            else:
                st.error("برجاء إدخال العنوان ورفع الملف")

    st.divider()

    # استعراض المكتبة مع زر الحذف
    st.subheader("🗂️ المواد المحفوظة حالياً")
    if st.session_state.library_db:
        for index, item in enumerate(st.session_state.library_db):
            col_a, col_b, col_c, col_d = st.columns([2, 3, 2, 1])
            col_a.write(f"**{item['النوع']}**")
            col_b.write(item['العنوان'])
            col_c.button("👁️ فتح", key=f"open_{index}")
            
            # زر الحذف
            if col_d.button("🗑️ حذف", key=f"del_{index}"):
                st.session_state.library_db.pop(index)
                st.rerun() # لإعادة تحديث الصفحة فوراً بعد الحذف
            st.write("---")
    else:
        st.info("المكتبة فارغة حالياً. قم بإضافة القوانين واللوائح لتظهر هنا.")

# --- 5. قسم القضايا (الصياغة) ---
elif choice == "🏛️ قطاع القضايا":
    st.header("🏛️ القسم القضائي")
    st.info("هنا يتم الصياغة بناءً على المواد المرفوعة في المكتبة")
    # (كود الصياغة السابق يوضع هنا)

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import io

# --- 1. إعدادات الصفحة واللغة ---
st.set_page_config(page_title="نظام الإدارة القانونية", layout="wide")

# دالة لضبط ملف الوورد ليدعم العربية (يمين لليسار)
def set_doc_rtl(doc):
    for section in doc.sections:
        section.right_margin = Pt(30)
    for paragraph in doc.paragraphs:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        paragraph.style.font.rtl = True

# --- 2. تهيئة قاعدة البيانات (SQLite) ---
def init_db():
    conn = sqlite3.connect('legal_db.db', check_same_thread=False)
    c = conn.cursor()
    # جدول القضايا
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, case_no TEXT, year TEXT, 
                  court TEXT, lawyer TEXT, appeal_deadline DATE)''')
    # جدول الجلسات
    c.execute('''CREATE TABLE IF NOT EXISTS sessions 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, case_id INTEGER, 
                  session_date DATE, decision TEXT)''')
    conn.commit()
    return conn

conn = init_db()

# --- 3. تصميم واجهة المستخدم (Buttons) ---
st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>⚖️ الإدارة القانونية - منطقة البحيرة</h1>", unsafe_allow_html=True)

# نظام التنقل
if 'menu' not in st.session_state: st.session_state.menu = 'home'

cols = st.columns(4)
if cols[0].button("🏠 لوحة التحكم"): st.session_state.menu = 'home'
if cols[1].button("➕ إضافة قضية"): st.session_state.menu = 'add'
if cols[2].button("📅 الجلسات"): st.session_state.menu = 'sess'
if cols[3].button("📄 التقارير"): st.session_state.menu = 'rep'

st.markdown("---")

# --- 4. الصفحات ---

# الصفحة الرئيسية: التنبيهات وملخص القضايا
if st.session_state.menu == 'home':
    st.subheader("🔔 تنبيهات المواعيد الهامة")
    today = datetime.now().date()
    
    # تنبيه الجلسات خلال أسبوع
    next_week = today + timedelta(days=7)
    df_sess_alert = pd.read_sql(f"SELECT c.case_no, s.session_date FROM sessions s JOIN cases c ON s.case_id = c.id WHERE s.session_date BETWEEN '{today}' AND '{next_week}'", conn)
    
    if not df_sess_alert.empty:
        for _, r in df_sess_alert.iterrows():
            st.warning(f"⚠️ جلسة قادمة: قضية رقم {r['case_no']} بتاريخ {r['session_date']}")
    else:
        st.success("✅ لا توجد جلسات وشيكة حالياً")

    # تنبيه الطعون
    df_app_alert = pd.read_sql(f"SELECT case_no, appeal_deadline FROM cases WHERE appeal_deadline BETWEEN '{today}' AND '{(today + timedelta(days=10))}'", conn)
    if not df_app_alert.empty:
        for _, r in df_app_alert.iterrows():
            st.error(f"🚨 آخر ميعاد للطعن: قضية رقم {r['case_no']} يوم {r['appeal_deadline']}")

    st.markdown("---")
    st.subheader("📊 ملخص القضايا (تعديل/حذف)")
    all_cases = pd.read_sql("SELECT * FROM cases", conn)
    if not all_cases.empty:
        for _, row in all_cases.iterrows():
            c1, c2, c3, c4 = st.columns([3, 2, 1, 1])
            c1.write(f"📂 قضية {row['case_no']} لعام {row['year']} - {row['court']}")
            c2.write(f"👤 محامي: {row['lawyer']}")
            if c3.button("✏️", key=f"edit_{row['id']}"):
                st.info("ميزة التعديل ستفتح في التحديث القادم")
            if c4.button("🗑️", key=f"del_{row['id']}"):
                conn.execute(f"DELETE FROM cases WHERE id={row['id']}")
                conn.execute(f"DELETE FROM sessions WHERE case_id={row['id']}")
                conn.commit()
                st.rerun()
    else:
        st.info("لا توجد قضايا مسجلة")

# صفحة إضافة قضية جديدة
elif st.session_state.menu == 'add':
    with st.form("case_form"):
        st.subheader("📝 تسجيل دعوى جديدة")
        n = st.text_input("رقم الدعوى")
        y = st.text_input("السنة")
        ct = st.text_input("المحكمة")
        l = st.text_input("المحامي")
        d = st.date_input("آخر ميعاد للطعن (اختياري

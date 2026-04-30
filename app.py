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

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="نظام الإدارة القانونية", layout="wide")

# دالة لضبط ملف الوورد ليكون عربي بالكامل (RTL)
def set_doc_rtl(doc):
    for section in doc.sections:
        section.right_margin = Pt(30)
    for paragraph in doc.paragraphs:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT

def set_table_rtl(table):
    tblPr = table._element.xpath('w:tblPr')[0]
    bidi = OxmlElement('w:bidi')
    bidi.set(qn('w:val'), '1')
    tblPr.append(bidi)

# --- 2. تهيئة قاعدة البيانات (تحديث ذكي) ---
def init_db():
    conn = sqlite3.connect('legal_safe_db.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, case_no TEXT, year TEXT, 
                  court TEXT, lawyer TEXT, appeal_deadline DATE, created_at DATE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sessions 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, case_id INTEGER, 
                  session_date DATE, decision TEXT)''')
    conn.commit()
    return conn

conn = init_db()

# --- 3. الواجهة الرئيسية ---
st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>⚖️ الإدارة القانونية - منطقة البحيرة</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>نظام إدارة الدعاوى والطعون والتنبيهات</h4>", unsafe_allow_html=True)

if 'menu' not in st.session_state: st.session_state.menu = 'home'

cols = st.columns(4)
if cols[0].button("🏠 لوحة التحكم والتبيهات"): st.session_state.menu = 'home'
if cols[1].button("➕ إضافة دعوى جديدة"): st.session_state.menu = 'add'
if cols[2].button("📅 الجلسات والتعديل"): st.session_state.menu = 'sess'
if cols[3].button("📄 استخراج بيان رسمي"): st.session_state.menu = 'rep'

st.markdown("---")

# --- 4. الصفحات ---

# الصفحة الرئيسية (التنبيهات)
if st.session_state.menu == 'home':
    st.subheader("🔔 سجل التنبيهات العاجلة")
    today = datetime.now().date()
    
    c_alert1, c_alert2 = st.columns(2)
    
    with c_alert1:
        st.info("🗓️ جلسات الأسبوع القادم")
        next_week = today + timedelta(days=7)
        df_s = pd.read_sql(f"SELECT c.case_no, s.session_date FROM sessions s JOIN cases c ON s.case_id = c.id WHERE s.session_date BETWEEN '{today}' AND '{next_week}'", conn)
        if not df_s.empty:
            for _, r in df_s.iterrows():
                st.warning(f"⚠️ جلسة قضية {r['case_no']} بتاريخ {r['session_date']}")
        else: st.write("لا توجد جلسات وشيكة.")

    with c_alert2:
        st.error("🚨 مواعيد الطعن (خلال 10 أيام)")
        df_a = pd.read_sql(f"SELECT case_no, appeal_deadline FROM cases WHERE appeal_deadline BETWEEN '{today}' AND '{(today + timedelta(days=10))}'", conn)
        if not df_a.empty:
            for _, r in df_a.iterrows():
                st.error(f"📍 ميعاد طعن قضية {r['case_no']} ينتهي في {r['appeal_deadline']}")
        else: st.write("لا توجد مواعيد طعن حالياً.")

    st.markdown("---")
    st.subheader("📊 ملخص القضايا")
    df_all = pd.read_sql("SELECT id, case_no as 'رقم الدعوى', year as 'السنة', court as 'المحكمة', lawyer as 'المحامي' FROM cases", conn)
    if not df_all.empty:
        for idx, row in df_all.iterrows():
            col1, col2, col3 = st.columns([4, 1, 1])
            col1.write(f"📂 قضية {row['رقم الدعوى']} / {row['السنة']} - {row['المحكمة']} (المحامي: {row['المحامي']})")
            if col

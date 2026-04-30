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
st.set_page_config(page_title="نظام الإدارة القانونية - البحيرة", layout="wide")

# دالة ضبط اتجاه الجدول ونصوص الوورد للعربية (RTL)
def set_document_rtl(doc):
    for section in doc.sections:
        section.right_margin = Pt(30)
        section.left_margin = Pt(30)
    
def set_table_rtl(table):
    tblPr = table._element.xpath('w:tblPr')[0]
    bidi = OxmlElement('w:bidi')
    bidi.set(qn('w:val'), '1')
    tblPr.append(bidi)

# --- 2. إدارة قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('legal_management.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, case_no TEXT, year TEXT, 
                  court TEXT, circuit TEXT, plaintiff TEXT, defendant TEXT, 
                  subject TEXT, lawyer TEXT, status TEXT, appeal_deadline DATE, created_at DATE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sessions 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, case_id INTEGER, 
                  session_date DATE, decision TEXT)''')
    
    # تحديث تلقائي للأعمدة الناقصة
    cols = [col[1] for col in c.execute("PRAGMA table_info(cases)").fetchall()]
    if 'appeal_deadline' not in cols: c.execute("ALTER TABLE cases ADD COLUMN appeal_deadline DATE")
    conn.commit()
    return conn

conn = init_db()

# --- 3. واجهة المستخدم ---
st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>⚖️ الإدارة القانونية - ديوان عام منطقة البحيرة</h1>", unsafe_allow_html=True)

# أزرار التنقل العرضية
m = st.columns(4)
if 'page' not in st.session_state: st.session_state.page = 'dash'
if m[0].button("🏠 لوحة التحكم والتنبيهات"): st.session_state.page = 'dash'
if m[1].button("➕ إضافة دعوى/طعن"): st.session_state.page = 'add'
if m[2].button("📅 سجل الجلسات"): st.session_state.page = 'sessions'
if m[3].button("📄 استخراج التقرير الرسمي"): st.session_state.page = 'reports'

# --- الصفحة الرئيسية (التنبيهات والملخص) ---
if st.session_state.page == 'dash':
    st.markdown("### 🔔 سجل التنبيهات العاجلة")
    today = datetime.now().date()
    
    col_a, col_b = st.columns(2)
    
    # تنبيه الجلسات القادمة (أسبوع)
    with col_a:
        st.info("🗓️ جلسات خلال 7 أيام")
        next_week = today + timedelta(days=7)
        sessions_alert = pd.read_sql(f"SELECT c.case_no, s.session_date FROM sessions s JOIN cases c ON s.case_id = c.id WHERE s.session_date BETWEEN '{today}' AND '{next_week}'", conn)
        if not sessions_alert.empty:
            for _, r in sessions_alert.iterrows():
                st.warning(f"⚠️ قضية رقم {r['case_no']} - جلسة يوم: {r['session_date']}")
        else: st.write("لا توجد جلسات قريبة.")

    # تنبيه الطعون (10 أيام)
    with col_b:
        st.error("🚨 مواعيد طعن وشيكة (10 أيام)")
        appeal_alert = pd.read_sql(f"SELECT case_no, appeal_deadline FROM cases WHERE appeal_deadline BETWEEN '{today}' AND '{(today + timedelta(days=10))}'", conn)
        if not appeal_alert.

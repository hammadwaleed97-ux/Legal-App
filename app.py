import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import io

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="نظام الشئون القانونية - البحيرة", layout="wide")

# دالة هندسية لضبط الوورد ليكون عربي تماماً وغير مقلوب
def fix_docx_rtl(doc):
    for section in doc.sections:
        section.header_distance = Inches(0.5)
        # ضبط اتجاه القسم ككل
        sectPr = section._sectPr
        cols = sectPr.xpath('./w:cols')[0]
        cols.set(qn('w:sep'), '1')
    
    # ضبط الفقرات لتكون RTL
    for paragraph in doc.paragraphs:
        p_pr = paragraph._element.get_or_add_pPr()
        bidi = OxmlElement('w:bidi')
        bidi.set(qn('w:val'), '1')
        p_pr.append(bidi)

def set_table_rtl(table):
    tblPr = table._element.xpath('w:tblPr')[0]
    bidi = OxmlElement('w:bidi')
    bidi.set(qn('w:val'), '1')
    tblPr.append(bidi)

# --- 2. قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('legal_beheira_v5.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  c_type TEXT, c_no TEXT, c_year TEXT, court TEXT, 
                  plaintiff TEXT, subject TEXT, lawyer TEXT, 
                  last_proc TEXT, appeal_deadline DATE, reg_date DATE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sessions 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, case_id INTEGER, 
                  s_date DATE, decision TEXT)''')
    conn.commit()
    return conn

conn = init_db()

# --- 3. الواجهة ---
st.markdown("<h2 style='text-align: center;'>⚖️ الهيئة القومية للتأمين الاجتماعي</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>منطقة البحيرة - الإدارة العامة للشئون القانونية</h4>", unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'dash'

m = st.columns(4)
if m[0].button("🏠 الرئيسية والبحث"): st.session_state.page = 'dash'
if m[1].button("➕ قيد دعوى/طعن"): st.session_state.page = 'add'
if m[2].button("📅 الجلسات والتفاصيل"): st.session_state.page = 'sess'
if m[3].button("📄 التقارير الرسمية"): st.session_state.page = 'rep'

st.divider()

# --- 4. الصفحات ---

if st.session_state.page == 'dash':
    st.subheader("🔔 التنبيهات العاجلة")
    today = datetime.now().date()
    
    c1, c2 = st.columns(2)
    with c1:
        # تنبيه الجلسات ببيانات كاملة
        df_s = pd.read_sql(f"SELECT c.c_no, c.c_year, c.court, s.s_date FROM sessions s JOIN cases c ON s.case_id = c.id WHERE s.s_date BETWEEN '{today}' AND '{(today + timedelta(days=7))}'", conn)
        if not df_s.empty:
            for _, r in df_s.iterrows():
                st.warning(f"🗓️ جلسة: دعوى {r['c_no']} / {r['c_year']} - {r['court']} (بتاريخ: {r['s_date']})")
        else: st.info("لا توجد

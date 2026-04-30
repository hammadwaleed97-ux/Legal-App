import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="نظام الإدارة القانونية", layout="wide")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; font-weight: bold; }
    .main-title { text-align: center; color: #1e3a8a; background-color: #f0f2f6; padding: 15px; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('legal_management.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  case_no TEXT, year TEXT, court TEXT, circuit TEXT, 
                  plaintiff TEXT, defendant TEXT, subject TEXT, 
                  lawyer TEXT, status TEXT, created_at DATE)''')
    
    # تحديث الأعمدة آلياً
    columns = [col[1] for col in c.execute("PRAGMA table_info(cases)").fetchall()]
    check_cols = {'circuit': 'TEXT', 'plaintiff': 'TEXT', 'defendant': 'TEXT', 'lawyer': 'TEXT', 'created_at': 'DATE'}
    for col_name, col_type in check_cols.items():
        if col_name not in columns:
            c.execute("ALTER TABLE cases ADD COLUMN " + col_name + " " + col_type)
    
    c.execute('''CREATE TABLE IF NOT EXISTS sessions 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, case_id INTEGER, 
                  session_date DATE, decision TEXT)''')
    conn.commit()
    return conn

conn = init_db()

# --- 3. وظيفة الوورد (مكتوبة بأمان تام) ---
def create_word_report(df, lawyer_name, date_from, date_to):
    doc = Document()
    section = doc.sections[0]
    section.right_margin = Pt(20)
    
    # الرأس
    h = doc.add_paragraph()
    h.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    h.add_run("الهيئة القومية للتأمين الاجتماعي\nالادارة العامة للشئون القانونية\nمنطقة البحيرة").bold = True

    # العنوان
    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t.add_run("\nبيان بالدعاوى المتداولة طرف الأستاذ / " + str(lawyer_name)).bold = True
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run("عن الفترة من " + str(date_from) + " حتى " + str(date_to))

    # الجدول
    table = doc.add_table(rows=1, cols=9)
    table.style = 'Table Grid'
    headers = ['م', 'رقم الدعوى / سنة', 'المحكمة', 'الدائرة', 'المدعي', 'المدعى عليه', 'موضوع الدعوى', 'آخر إجراء', 'المحامي المختص']
    for i, title in enumerate(headers):
        table.rows[0].cells[i].text = title

    for index, row in df.iterrows():
        cells = table.add_row().cells
        cells[0].text = str(index + 1)
        cells[1].text = str(row.get('case_no','')) + " / " + str(row.get('year',''))
        cells[2].text = str(row.get('court','') or '')
        cells[3].text = str(row.get('circuit','') or '')
        cells[4].text = str(row.get('plaintiff','') or '')
        cells[5].text = str(row.get('defendant','') or '')
        cells[6].text = str(row.get('subject','') or '')
        cells[7].text = str(row.get('status','') or '')
        cells[8].text = str(row.get('lawyer','') or '')

    target = io.BytesIO()
    doc.save(target)
    return target.getvalue()

# --- 4. واجهة المستخدم ---
st.markdown("<div class='main-title'><h1>⚖️ نظام قضايا الإدارة القانونية</h1></div>", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1: b1 = st.button("🏠 لوحة التحكم")
with m2: b2 = st.button("➕ إضافة قضية")
with m3: b3 = st.button("📅 الجلسات")
with m4: b4 = st.button("📄 التقارير والحذف")

if 'page' not in st.

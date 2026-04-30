import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io

# --- إعدادات الصفحة ---
st.set_page_config(page_title="نظام الإدارة القانونية", layout="wide")

# تنسيق الواجهة (CSS) لتحسين المظهر العربي
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; font-weight: bold; font-size: 16px; }
    .main-title { text-align: center; color: #1e3a8a; background-color: #f0f2f6; padding: 15px; border-radius: 15px; border: 1px solid #1e3a8a; }
    .stTable { direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

# --- إدارة قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('legal_management.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  case_no TEXT, year TEXT, court TEXT, circuit TEXT, 
                  plaintiff TEXT, defendant TEXT, subject TEXT, 
                  lawyer TEXT, status TEXT, created_at DATE)''')
    
    # فحص الأعمدة وتحديثها آلياً
    columns = [col[1] for col in c.execute("PRAGMA table_info(cases)").fetchall()]
    check_cols = {'circuit': 'TEXT', 'plaintiff': 'TEXT', 'defendant': 'TEXT', 'lawyer': 'TEXT', 'created_at': 'DATE'}
    for col_name, col_type in check_cols.items():
        if col_name not in columns:
            c.execute(f"ALTER TABLE cases ADD COLUMN {col_name} {col_type}")
    
    c.execute('''CREATE TABLE IF NOT EXISTS sessions 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, case_id INTEGER, 
                  session_date DATE, decision TEXT)''')
    conn.commit()
    return conn

conn = init_db()

# --- وظيفة إنشاء ملف Word (التنسيق الرسمي) ---
def create_word_report(df, lawyer_name, date_from, date_to):
    doc = Document()
    # الهوامش
    section = doc.sections[0]
    section.right_margin = Pt(25)
    
    # رأس الصفحة
    header = doc.add_paragraph()
    header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = header.add_run("الهيئة القومية للتأمين الاجتماعي\nالادارة العامة للشئون القانونية\nمنطقة البحيرة")
    run.bold = True
    run.font.size = Pt(13)

    # العنوان
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    # استبدال f-string بطريقة أكثر أماناً لتجنب خطأ الأقواس
    title_text = "\nبيان بالدعاوى المتداولة طرف الأستاذ / " + str(lawyer_name)
    run_t = title.add_run(title_text)
    run_t.bold = True
    run_t.font.size = Pt(16)
    
    period_text = "عن الفترة من " + str(date_from) + " حتى " + str(date_to)
    doc.add_paragraph(period

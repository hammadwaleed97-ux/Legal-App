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

# تنسيق الواجهة
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; }
    .main-title { text-align: center; color: #1e3a8a; }
    th { background-color: #f0f2f6 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- إدارة قاعدة البيانات مع التحديث التلقائي ---
def init_db():
    conn = sqlite3.connect('legal_management.db', check_same_thread=False)
    c = conn.cursor()
    # إنشاء الجدول بالهيكل الجديد
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  case_no TEXT, year TEXT, court TEXT, circuit TEXT, 
                  plaintiff TEXT, defendant TEXT, subject TEXT, 
                  lawyer TEXT, status TEXT, created_at DATE)''')
    
    # التأكد من وجود الأعمدة الجديدة (في حال كانت القاعدة قديمة)
    columns = [col[1] for col in c.execute("PRAGMA table_info(cases)").fetchall()]
    new_cols = {'circuit': 'TEXT', 'plaintiff': 'TEXT', 'defendant': 'TEXT', 'lawyer': 'TEXT', 'created_at': 'DATE'}
    for col_name, col_type in new_cols.items():
        if col_name not in columns:
            c.execute(f"ALTER TABLE cases ADD COLUMN {col_name} {col_type}")
    
    c.execute('''CREATE TABLE IF NOT EXISTS sessions 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, case_id INTEGER, 
                  session_date DATE, decision TEXT)''')
    conn.commit()
    return conn

conn = init_db()

# --- وظيفة إنشاء ملف Word بالتنسيق المطلوب ---
def create_word_report(df, lawyer_name, date_from, date_to):
    doc = Document()
    # إعدادات الصفحة للعربية
    section = doc.sections[0]
    section.right_margin = Pt(36)
    
    # الرأس (Header)
    header = doc.add_paragraph()
    header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = header.add_run("الهيئة القومية للتأمين الاجتماعي\nالادارة العامة للشئون القانونية\nمنطقة البحيرة")
    run.bold = True

    # العنوان
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_t = title.add_run(f"\nبيان بالدعاوى المتداولة طرف الأستاذ / {lawyer_name}")
    run_t.bold = True
    run_t.font.size = Pt(15)
    
    doc.add_paragraph(f"عن الفترة من {date_from} حتى {date_to}").alignment = WD_ALIGN_PARAGRAPH.CENTER

    # الجدول
    table = doc.add_table(rows=1, cols=9)
    table.style = 'Table Grid'
    headers = ['م', 'رقم الدعوى / سنة', 'المحكمة', 'الدائرة', 'المدعي', 'المدعى عليه', 'موضوع الدعوى', 'آخر إجراء', 'المحامي المختص']
    
    for i, h in enumerate(headers):
        table.rows[0].cells[i].text = h

    for index, row in df.iterrows():
        cells = table.add_row().cells
        cells[0].text = str(index + 1)
        cells[1].text = f"{row['case_no']} / {row['year']}"
        cells[2].text = str(row['court'])
        cells[3].text = str(row['circuit'])
        cells[4].text = str(row['plaintiff'])
        cells[5].text = str(row['defendant'])
        cells[6].text = str(row['subject'])
        cells[7].text = str(row['status'])
        cells[8].text = str(row['lawyer'])

    target = io.BytesIO()
    doc.save(target)
    return target.getvalue()

# --- واجهة البرنامج ---
st.markdown("<h1 class='main-title'>⚖️ نظام إدارة قضايا الإدارة القانونية</h1>", unsafe_allow_html=True)

menu_cols = st.columns(4)
with menu_cols[0]: btn_dash = st.button("🏠 لوحة التحكم")
with menu_cols[1]: btn_add = st.button("➕ إضافة قضية")
with menu_cols[2]: btn_sessions = st.button("📅 الجلسات")
with menu_cols[3]: btn_reports = st.button("📄 التقارير والحذف")

if 'page' not in st.session_state: st.session_state.page = 'dash'
if btn_dash: st.session_state.page = 'dash'
if btn_add: st.session_state.page = 'add'
if btn_sessions: st.session_state.page = 'sessions'
if btn_reports: st.session_state.page = 'reports'

# --- 1. لوحة التحكم ---
if st.session_state.page == 'dash':
    st.subheader("📊 ملخص عام")
    total = pd.read_sql_query("SELECT COUNT(*) FROM cases", conn).iloc[0,0]
    st.metric("إجمالي القضايا", total)
    st.write("---")
    st.subheader("🗓️ أحدث القضايا المضافة")
    # استعلام آمن لتجنب الخطأ
    latest = pd.read_sql_query("SELECT case_no as 'الرقم', year as 'السنة', plaintiff as 'المدعي' FROM cases ORDER BY id DESC LIMIT 5", conn)
    st.table(latest)

# --- 2. إضافة قضية ---
elif st.session_state.page == 'add':
    st.subheader("📝 إدخال بيانات دعوى")
    with st.form("add_case"):
        c1, c2, c3 = st.columns(3)
        case_no = c1.text_input("رقم الدعوى")
        year = c2.text_input("السنة")
        court = c3.text_input("المحكمة")
        
        c4, c5, c6 = st.columns(3)
        circuit = c4.text_input("الدائرة")
        plaintiff = c5.text_input("المدعي")
        defendant = c6.text_input("المدعى عليه")
        
        subject = st.text_area("الموضوع")
        lawyer = st.text_input("المحامي المختص")
        status = st.text_input("آخر إجراء")
        
        if st.form_submit_button("حفظ"):
            conn.execute("INSERT INTO cases (case_no, year, court, circuit, plaintiff, defendant, subject, lawyer, status, created_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
                         (case_no, year, court, circuit, plaintiff, defendant, subject, lawyer, status, datetime

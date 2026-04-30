import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="نظام الإدارة القانونية", layout="wide")

# دالة ضبط اتجاه جدول الوورد للعربية
def set_rtl(table):
    tblPr = table._element.xpath('w:tblPr')[0]
    bidi = OxmlElement('w:bidi')
    bidi.set(qn('w:val'), '1')
    tblPr.append(bidi)

# --- 2. إدارة قاعدة البيانات (تحديث تلقائي) ---
def init_db():
    conn = sqlite3.connect('legal_management.db', check_same_thread=False)
    c = conn.cursor()
    # إنشاء الجداول الأساسية
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, case_no TEXT, year TEXT, 
                  court TEXT, circuit TEXT, plaintiff TEXT, defendant TEXT, 
                  subject TEXT, lawyer TEXT, status TEXT, appeal_deadline DATE, created_at DATE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sessions 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, case_id INTEGER, 
                  session_date DATE, decision TEXT)''')
    
    # فحص الأعمدة الناقصة (مثل ميعاد الطعن) وإضافتها آلياً
    existing_cols = [col[1] for col in c.execute("PRAGMA table_info(cases)").fetchall()]
    if 'appeal_deadline' not in existing_cols:
        c.execute("ALTER TABLE cases ADD COLUMN appeal_deadline DATE")
    if 'circuit' not in existing_cols:
        c.execute("ALTER TABLE cases ADD COLUMN circuit TEXT")
        
    conn.commit()
    return conn

conn = init_db()

# --- 3. واجهة المستخدم ---
st.markdown("<h1 style='text-align: center;'>⚖️ نظام الإدارة القانونية - البحيرة</h1>", unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'dash'

m1, m2, m3, m4 = st.columns(4)
if m1.button("🏠 لوحة التحكم"): st.session_state.page = 'dash'
if m2.button("➕ إضافة قضية"): st.session_state.page = 'add'
if m3.button("📅 الجلسات"): st.session_state.page = 'sessions'
if m4.button("📄 التقارير"): st.session_state.page = 'reports'

# --- الصفحة الرئيسية (التنبيهات والملخص) ---
if st.session_state.page == 'dash':
    st.subheader("🔔 تنبيهات المواعيد")
    today = datetime.now().date()
    
    # تنبيه الجلسات القادمة
    next_week = today + timedelta(days=7)
    try:
        alert_s = pd.read_sql(f"SELECT c.case_no, s.session_date FROM sessions s JOIN cases c ON s.case_id = c.id WHERE s.session_date BETWEEN '{today}' AND '{next_week}'", conn)
        for _, r in alert_s.iterrows():
            st.warning(f"⚠️ جلسة قادمة للقضية رقم {r['case_no']} بتاريخ {r['session_date']}")
    except: pass

    # تنبيه الطعون
    try:
        alert_a = pd.read_sql(f"SELECT case_no, appeal_deadline FROM cases WHERE appeal_deadline BETWEEN '{today}' AND '{(today + timedelta(days=10))}'", conn)
        for _, r in alert_a.iterrows():
            st.error(f"🚨 ميعاد طعن وشيك للقضية {r['case_no']} يوم {r['appeal_deadline']}")
    except: pass

    st.markdown("---")
    st.subheader("📊 ملخص القضايا")
    df = pd.read_sql("SELECT id, case_no as 'رقم الدعوى', year as 'السنة', court as 'المحكمة', lawyer as 'المحامي' FROM cases", conn)
    if not df.empty:
        for idx, row in df.iterrows():
            c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
            c1.write(f"قضية {row['رقم الدعوى']} / {row['السنة']}")
            c2.write(f"المحامي: {row['المحامي']}")
            if c3.button("🗑️ حذف", key=f"del_{row['id']}"):
                conn.execute(f"DELETE FROM cases WHERE id={row['id']}")
                conn.commit()
                st.rerun()
    else: st.info("لا توجد بيانات")

# --- صفحة الجلسات (تم إصلاحها) ---
elif st.session_state.page == 'sessions':
    st.subheader("📅 سجل الجلسات")
    all_c = pd.read_sql("SELECT id, case_no FROM cases", conn)
    if not all_c.empty:
        choice = st.selectbox("اختر القضية", all_c['id'], format_func=lambda x: f"قضية رقم {all_c[all_c['id']==x]['case_no'].values[0]}")
        with st.form("session_form"):
            d = st.date_input("تاريخ الجلسة")
            res = st.text_area("القرار")
            if st.form_submit_button("حفظ"):
                conn.execute("INSERT INTO sessions (case_id, session_date, decision) VALUES (?,?,?)", (int(choice), d, res))
                conn.commit()
                st.success("تم الحفظ")
        
        st.write("القرارات السابقة:")
        st.table(pd.read_sql(f"SELECT session_date as 'التاريخ', decision as 'القرار' FROM sessions WHERE case_id={choice}", conn))

# --- صفحة التقارير وإضافة القضايا ---
# (تم تبسيط الأكواد لضمان عدم حدوث خطأ Syntax)
elif st.session_state.page == 'add':
    with st.form("new_case"):
        no = st.text_input("رقم الدعوى")
        yr = st.text_input("السنة")
        ct = st.text_input("المحكمة")
        law = st.text_input("المحامي")
        ap = st.date_input("آخر ميعاد طعن", value=None)
        if st.form_submit_button("إضافة"):
            conn.execute("INSERT INTO cases (case_no, year, court, lawyer, appeal_deadline, created_at) VALUES (?,?,?,?,?,?)", (no, yr, ct, law, ap, datetime.now().date()))
            conn.commit()
            st.success("تمت الإضافة")

elif st.session_state.page == 'reports':
    st.subheader("📄 تقارير Word")
    if st.button("استخراج بيان المحامي"):
        df_rep = pd.read_sql("SELECT * FROM cases", conn)
        if not df_rep.empty:
            doc = Document()
            t = doc.add_table(rows=1, cols=5)
            t.style = 'Table Grid'
            set_rtl(t)
            # إضافة بيانات للجدول (تبسيط)
            for r in df_rep.itertuples():
                cells = t.add_row().cells
                cells[0].text = str(r.case_no)
                cells[1].text = str(r.court)
            
            buf = io.BytesIO()
            doc.save(buf)
            st.download_button("تحميل الملف", buf.getvalue(), "report.docx")

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

def set_table_rtl(table):
    tblPr = table._element.xpath('w:tblPr')[0]
    bidi = OxmlElement('w:bidi')
    bidi.set(qn('w:val'), '1')
    tblPr.append(bidi)

# --- 2. قاعدة البيانات (هيكلة شاملة لضمان عدم السقوط) ---
def init_db():
    # استخدام اسم قاعدة بيانات جديد لتجنب تضارب النسخ القديمة
    conn = sqlite3.connect('legal_system_final_v2.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  case_type TEXT, case_no TEXT, case_year TEXT, court TEXT, circuit TEXT,
                  plaintiff TEXT, defendant TEXT, subject TEXT, 
                  lawyer TEXT, last_procedure TEXT, appeal_deadline DATE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sessions 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, case_id INTEGER, 
                  session_date DATE, decision TEXT)''')
    conn.commit()
    return conn

conn = init_db()

# --- 3. الواجهة الرئيسية ---
st.markdown("<h2 style='text-align: center; color: #1e3a8a;'>⚖️ الإدارة العامة للشئون القانونية - ديوان عام محافظة البحيرة</h2>", unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'dashboard'

# قائمة التنقل
m = st.columns(4)
if m[0].button("🔔 التنبيهات والملخص"): st.session_state.page = 'dashboard'
if m[1].button("➕ إضافة (دعوى/طعن)"): st.session_state.page = 'add'
if m[2].button("📅 الجلسات والتعديل"): st.session_state.page = 'sessions'
if m[3].button("📄 التقارير الرسمية"): st.session_state.page = 'reports'

st.divider()

# --- 4. الصفحات ---

# الصفحة الرئيسية (التنبيهات والبحث)
if st.session_state.page == 'dashboard':
    st.subheader("📢 لوحة التنبيهات الذكية")
    today = datetime.now().date()
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.info("🗓️ جلسات الأسبوع القادم")
        df_s = pd.read_sql(f"SELECT c.case_no, s.session_date FROM sessions s JOIN cases c ON s.case_id = c.id WHERE s.session_date BETWEEN '{today}' AND '{(today + timedelta(days=7))}'", conn)
        if not df_s.empty:
            for _, r in df_s.iterrows(): st.warning(f"⚠️ جلسة قضية {r['case_no']} بتاريخ {r['session_date']}")
        else: st.write("لا توجد جلسات وشيكة.")

    with col_b:
        st.error("🚨 مواعيد طعون (خلال 10 أيام)")
        df_a = pd.read_sql(f"SELECT case_no, appeal_deadline FROM cases WHERE appeal_deadline BETWEEN '{today}' AND '{(today + timedelta(days=10))}'", conn)
        if not df_a.empty:
            for _, r in df_a.iterrows(): st.error(f"📍 ميعاد طعن قضية {r['case_no']} ينتهي في {r['appeal_deadline']}")
        else: st.write("لا توجد مواعيد طعون وشيكة.")

    st.divider()
    st.subheader("🔍 سجل القضايا المسجلة")
    search = st.text_input("بحث برقم القضية أو المحامي")
    query = "SELECT id, case_type as 'النوع', case_no as 'الرقم', case_year as 'السنة', court as 'المحكمة', lawyer as 'المحامي', subject as 'الموضوع' FROM cases"
    if search: query += f" WHERE case_no LIKE '%{search}%' OR lawyer LIKE '%{search}%'"
    df_display = pd.read_sql(query, conn)
    st.dataframe(df_display, use_container_width=True)

# صفحة الإضافة (شاملة كل الخانات)
elif st.session_state.page == 'add':
    with st.form("add_form"):
        st.subheader("📝 تسجيل بيانات قضية/طعن جديدة")
        ctype = st.selectbox("نوع القيد", ["دعوى", "طعن"])
        c1, c2, c3 = st.columns(3)
        c_no = c1.text_input("رقم القضية")
        c_yr = c2.text_input("السنة")
        c_court = c3.text_input("المحكمة")
        c_cir = st.text_input("الدائرة")
        plaint = st.text_input("المدعي (طرف أول)")
        defend = st.text_input("المدعى عليه (طرف ثان)")
        subj = st.text_area("موضوع الدعوى بالتفصيل")
        law = st.text_input("المحامي المسؤول")
        proc = st.text_input("آخر إجراء اتخذ")
        deadline = st.date_input("ميعاد الطعن (إن وجد)", value=None)
        
        if st.form_submit_button("حفظ البيانات في السجل"):
            conn.execute("INSERT INTO cases (case_type, case_no, case_year, court, circuit, plaintiff, defendant, subject, lawyer, last_procedure, appeal_deadline) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                         (ctype, c_no, c_yr, c_court, c_cir, plaint, defend, subj, law, proc, deadline))
            conn.commit()
            st.success("تم الحفظ بنجاح")

# صفحة الجلسات والتعديل (تعديل مباشر وحذف)
elif st.session_state.page == 'sessions':
    st.subheader("📅 إدارة الجلسات وتصحيح القرارات")
    c_list = pd.read_sql("SELECT id, case_no, case_year FROM cases", conn)
    if not c_list.empty:
        cid = st.selectbox("اختر القضية للعمل عليها", c_list['id'], format_func=lambda x: f"قضية {c_list[c_list['id']==x]['case_no'].values[0]} لعام {c_list[c_list['id']==x]['case_year'].values[0]}")
        
        with st.expander("📝 إضافة قرار جلسة جديد"):
            s_date = st.date_input("تاريخ الجلسة")
            s_dec = st.text_area("نص قرار الجلسة")
            if st.button("حفظ"):
                conn.execute("INSERT INTO sessions (case_id, session_date, decision) VALUES (?,?,?)", (int(cid), s_date, s_dec))
                conn.commit()
                st.rerun()

        st.markdown("---")
        st.write("📜 القرارات المسجلة (يمكنك تعديلها بالأسفل):")
        hist = pd.read_sql(f"SELECT * FROM sessions WHERE case_id={cid} ORDER BY session_date DESC", conn)
        for _, r in hist.iterrows():
            with st.container():
                new_val = st.text_area(f"تعديل قرار جلسة {r['session_date']}", value=r['decision'], key=f"edit_{r['id']}")
                col1, col2

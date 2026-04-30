import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from docx import Document
from docx.shared import Pt
import io

# --- 1. الإعدادات ---
st.set_page_config(page_title="نظام الإدارة القانونية", layout="wide")

# --- 2. قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('legal_final.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, case_no TEXT, year TEXT, 
                  court TEXT, lawyer TEXT, appeal_date DATE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sessions 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, case_id INTEGER, 
                  session_date DATE, decision TEXT)''')
    conn.commit()
    return conn

conn = init_db()

# --- 3. الواجهة ---
st.markdown("<h1 style='text-align:center;'>⚖️ الإدارة القانونية - منطقة البحيرة</h1>", unsafe_allow_html=True)

if 'pg' not in st.session_state: st.session_state.pg = 'home'

# أزرار التنقل
c1, c2, c3, c4 = st.columns(4)
if c1.button("🏠 التنبيهات والملخص"): st.session_state.pg = 'home'
if c2.button("➕ إضافة قضية"): st.session_state.pg = 'add'
if c3.button("📅 الجلسات والتعديل"): st.session_state.pg = 'sess'
if c4.button("📄 التقرير الرسمي"): st.session_state.pg = 'rep'

st.divider()

# --- الصفحة الرئيسية (التنبيهات) ---
if st.session_state.pg == 'home':
    st.subheader("🔔 التنبيهات العاجلة")
    today = datetime.now().date()
    
    # تنبيهات الجلسات (أسبوع)
    next_week = today + timedelta(days=7)
    s_alert = pd.read_sql(f"SELECT c.case_no, s.session_date FROM sessions s JOIN cases c ON s.case_id = c.id WHERE s.session_date BETWEEN '{today}' AND '{next_week}'", conn)
    if not s_alert.empty:
        for _, r in s_alert.iterrows():
            st.warning(f"🗓️ جلسة قادمة: قضية {r['case_no']} بتاريخ {r['session_date']}")
            
    # تنبيهات الطعون (10 أيام)
    a_alert = pd.read_sql(f"SELECT case_no, appeal_date FROM cases WHERE appeal_date BETWEEN '{today}' AND '{(today + timedelta(days=10))}'", conn)
    if not a_alert.empty:
        for _, r in a_alert.iterrows():
            st.error(f"🚨 ميعاد طعن وشيك: قضية {r['case_no']} يوم {r['appeal_date']}")

    st.divider()
    st.subheader("📊 القضايا المسجلة (حذف)")
    all_c = pd.read_sql("SELECT * FROM cases", conn)
    for _, r in all_c.iterrows():
        col1, col2 = st.columns([5, 1])
        col1.write(f"📂 {r['case_no']} / {r['year']} - {r['court']} ({r['lawyer']})")
        if col2.button("🗑️", key=f"del_{r['id']}"):
            conn.execute(f"DELETE FROM cases WHERE id={r['id']}")
            conn.commit()
            st.rerun()

# --- إضافة قضية ---
elif st.session_state.pg == 'add':
    with st.form("add"):
        no = st.text_input("رقم الدعوى")
        yr = st.text_input("السنة")
        ct = st.text_input("المحكمة")
        law = st.text_input("المحامي")
        ap = st.date_input("آخر ميعاد للطعن", value=None)
        if st.form_submit_button("حفظ"):
            conn.execute("INSERT INTO cases (case_no, year, court, lawyer, appeal_date) VALUES (?,?,?,?,?)", (no, yr, ct, law, ap))
            conn.commit()
            st.success("تم الحفظ")

# --- الجلسات والتعديل ---
elif st.session_state.pg == 'sess':
    st.subheader("📅 إدارة الجلسات والقرارات")
    c_list = pd.read_sql("SELECT id, case_no FROM cases", conn)
    if not c_list.empty:
        cid = st.selectbox("اختر القضية", c_list['id'], format_func=lambda x: f"رقم {c_list[c_list['id']==x]['case_no'].values[0]}")
        
        # إضافة قرار
        with st.expander("➕ إضافة قرار"):
            sd = st.date_input("التاريخ")
            dec = st.text_area("القرار")
            if st.button("حفظ القرار"):
                conn.execute("INSERT INTO sessions (case_id, session_date, decision) VALUES (?,?,?)", (int(cid), sd, dec))
                conn.commit()
                st.success("تم")

        # عرض وتعديل القرارات
        st.write("📜 القرارات السابقة:")
        h = pd.read_sql(f"SELECT * FROM sessions WHERE case_id={cid}", conn)
        for _, row in h.iterrows():
            col_d, col_t, col_b = st.columns([2, 5, 1])
            col_d.write(row['session_date'])
            new_val = col_t.text_area("القرار", value=row['decision'], key=f"val_{row['id']}")
            if col_t.button("💾 حفظ التعديل", key=f"sv_{row['id']}"):
                conn.execute("UPDATE sessions SET decision=? WHERE id=?", (new_val, row['id']))
                conn.commit()
                st.success("تم التعديل")
            if col_b.button("🗑️", key=f"sd_{row['id']}"):
                conn.execute(f"DELETE FROM sessions WHERE id={row['id']}")
                conn.commit()
                st.rerun()

# --- التقرير ---
elif st.session_state.pg == 'rep':
    if st.button("📥 تحميل التقرير (Word)"):
        df = pd.read_sql("SELECT * FROM cases", conn)
        doc = Document()
        doc.add_heading('الهيئة القومية للتأمين الاجتماعي - البحيرة', 0)
        doc.add_heading('بيان القضايا والطعون المتداولة', 2)
        for _, r in df.iterrows():
            doc.add_paragraph(f"قضية رقم: {r['case_no']} لعام {r['year']} - محكمة: {r['court']} - محامي: {r['lawyer']}")
        
        buf = io.BytesIO()
        doc.save(buf)
        st.download_button("تحميل الملف", buf.getvalue(), "report.docx")

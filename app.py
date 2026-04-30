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
st.set_page_config(page_title="نظام الإدارة القانونية المطور", layout="wide")

def set_table_rtl(table):
    tblPr = table._element.xpath('w:tblPr')[0]
    bidi = OxmlElement('w:bidi')
    bidi.set(qn('w:val'), '1')
    tblPr.append(bidi)

# --- 2. قاعدة البيانات (هيكلة شاملة) ---
def init_db():
    conn = sqlite3.connect('legal_pro_v1.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  type TEXT, case_no TEXT, year TEXT, court TEXT, 
                  plaintiff TEXT, defendant TEXT, subject TEXT, 
                  lawyer TEXT, last_action TEXT, appeal_deadline DATE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sessions 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, case_id INTEGER, 
                  session_date DATE, decision TEXT)''')
    conn.commit()
    return conn

conn = init_db()

# --- 3. تصميم الواجهة ---
st.markdown("<h2 style='text-align: center; color: #1e3a8a;'>⚖️ الإدارة العامة للشئون القانونية - منطقة البحيرة</h2>", unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'dashboard'

# أزرار التنقل الأساسية
m1, m2, m3, m4 = st.columns(4)
if m1.button("🔔 التنبيهات والملخص"): st.session_state.page = 'dashboard'
if m2.button("➕ إضافة (دعوى/طعن)"): st.session_state.page = 'add'
if m3.button("📅 الجلسات والتعديل"): st.session_state.page = 'sessions'
if m4.button("📄 التقارير الرسمية"): st.session_state.page = 'reports'

# --- 4. الصفحات ---

if st.session_state.page == 'dashboard':
    st.subheader("📢 لوحة التنبيهات العاجلة")
    today = datetime.now().date()
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.info("🗓️ جلسات خلال 7 أيام")
        df_s = pd.read_sql(f"SELECT c.case_no, s.session_date FROM sessions s JOIN cases c ON s.case_id = c.id WHERE s.session_date BETWEEN '{today}' AND '{(today + timedelta(days=7))}'", conn)
        if not df_s.empty: st.warning(f"لديك {len(df_s)} جلسات قادمة")
        else: st.write("لا يوجد")

    with col_b:
        st.error("🚨 طعون أوشكت على الانتهاء")
        df_a = pd.read_sql(f"SELECT case_no, appeal_deadline FROM cases WHERE appeal_deadline BETWEEN '{today}' AND '{(today + timedelta(days=10))}'", conn)
        if not df_a.empty: st.error(f"تحذير: {len(df_a)} طعون تنتهي قريباً")
        else: st.write("لا يوجد")

    st.divider()
    st.subheader("📋 كافة القضايا")
    df_all = pd.read_sql("SELECT id, type as 'النوع', case_no as 'الرقم', year as 'السنة', subject as 'الموضوع', last_action as 'آخر إجراء' FROM cases", conn)
    st.dataframe(df_all, use_container_width=True)
    if st.button("🗑️ مسح قضية محددة"):
        id_to_del = st.number_input("أدخل ID القضية للمسح", step=1)
        if st.button("تأكيد الحذف"):
            conn.execute(f"DELETE FROM cases WHERE id={id_to_del}")
            conn.commit()
            st.rerun()

elif st.session_state.page == 'add':
    with st.form("add_form"):
        st.subheader("📝 تسجيل بيانات جديدة")
        c_type = st.selectbox("النوع", ["دعوى", "طعن"])
        c1, c2 = st.columns(2)
        no = c1.text_input("رقم القضية")
        yr = c2.text_input("السنة")
        court = st.text_input("المحكمة / الدائرة")
        p_name = st.text_input("المدعي")
        d_name = st.text_input("المدعى عليه")
        subj = st.text_area("موضوع الدعوى")
        lawyer = st.text_input("المحامي المختص")
        last = st.text_input("آخر إجراء")
        deadline = st.date_input("ميعاد الطعن", value=None)
        
        if st.form_submit_button("حفظ بالنظام"):
            conn.execute("INSERT INTO cases (type, case_no, year, court, plaintiff, defendant, subject, lawyer, last_action, appeal_deadline) VALUES (?,?,?,?,?,?,?,?,?,?)",
                         (c_type, no, yr, court, p_name, d_name, subj, lawyer, last, deadline))
            conn.commit()
            st.success("تم الحفظ بنجاح")

elif st.session_state.page == 'sessions':
    st.subheader("📅 إدارة الجلسات وتعديل القرارات")
    case_list = pd.read_sql("SELECT id, case_no, year FROM cases", conn)
    if not case_list.empty:
        cid = st.selectbox("اختر القضية", case_list['id'], format_func=lambda x: f"قضية {case_list[case_list['id']==x]['case_no'].values[0]}")
        
        with st.expander("📝 إضافة قرار جلسة"):
            dt = st.date_input("تاريخ الجلسة")
            dec = st.text_area("القرار")
            if st.button("حفظ"):
                conn.execute("INSERT INTO sessions (case_id, session_date, decision) VALUES (?,?,?)", (int(cid), dt, dec))
                conn.commit()
                st.rerun()

        st.write("🔄 القرارات السابقة (يمكنك تعديل النص مباشرة):")
        h = pd.read_sql(f"SELECT * FROM sessions WHERE case_id={cid}", conn)
        for _, r in h.iterrows():
            new_val = st.text_area(f"قرار جلسة {r['session_date']}", value=r['decision'], key=f"s_{r['id']}")
            c1, c2 = st.columns(2)
            if c1.button("💾 حفظ التعديل", key=f"b_{r['id']}"):
                conn.execute("UPDATE sessions SET decision=? WHERE id=?", (new_val, r['id']))
                conn.commit()
                st.success("تم التعديل")
            if c2.button("🗑️ حذف", key=f"d_{r['id']}"):
                conn.execute(f"DELETE FROM sessions WHERE id={r['id']}")
                conn.commit()
                st.rerun()

elif st.session_state.page == 'reports':
    st.subheader("

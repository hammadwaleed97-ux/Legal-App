import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# --- إعدادات الصفحة ---
st.set_page_config(page_title="نظام الإدارة القانونية", layout="wide")

# --- إدارة قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('legal_management.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  case_no TEXT, year TEXT, court TEXT, opponent TEXT, 
                  case_type TEXT, subject TEXT, status TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sessions 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  case_id INTEGER, session_date DATE, requirements TEXT, decision TEXT,
                  FOREIGN KEY(case_id) REFERENCES cases(id))''')
    conn.commit()
    return conn

conn = init_db()
c = conn.cursor()

# --- واجهة البرنامج ---
st.sidebar.title("⚖️ القائمة الرئيسية")
menu = ["🏠 لوحة التحكم", "➕ إضافة قضية جديدة", "📅 إدارة الجلسات", "🔍 بحث وتقارير"]
choice = st.sidebar.radio("انتقل إلى:", menu)

# --- 1. لوحة التحكم ---
if choice == "🏠 لوحة التحكم":
    st.title("📊 ملخص الإدارة القانونية")
    col1, col2 = st.columns(2)
    
    total_cases = pd.read_sql_query("SELECT COUNT(*) FROM cases", conn).iloc[0,0]
    col1.metric("إجمالي القضايا", total_cases)
    
    st.subheader("🗓️ أحدث الجلسات")
    query = "SELECT cases.case_no, sessions.session_date, sessions.decision FROM sessions JOIN cases ON cases.id = sessions.case_id ORDER BY sessions.id DESC LIMIT 5"
    latest_sessions = pd.read_sql_query(query, conn)
    st.table(latest_sessions)

# --- 2. إضافة قضية جديدة ---
elif choice == "➕ إضافة قضية جديدة":
    st.title("📝 تسجيل قضية")
    with st.form("case_form"):
        col1, col2 = st.columns(2)
        with col1:
            case_no = st.text_input("رقم القضية")
            year = st.text_input("السنة")
            court = st.text_input("المحكمة")
        with col2:
            opponent = st.text_input("اسم الخصم")
            case_type = st.selectbox("النوع", ["إداري", "مدني", "عمالي", "تأديب"])
            status = st.selectbox("الحالة", ["متداولة", "محجوزة", "منتهية"])
        
        subject = st.text_area("الموضوع")
        if st.form_submit_button("حفظ"):
            c.execute("INSERT INTO cases (case_no, year, court, opponent, case_type, subject, status) VALUES (?,?,?,?,?,?,?)", 
                      (case_no, year, court, opponent, case_type, subject, status))
            conn.commit()
            st.success("تم الحفظ")

# --- 3. إدارة الجلسات ---
elif choice == "📅 إدارة الجلسات":
    st.title("📅 الجلسات")
    cases_df = pd.read_sql_query("SELECT id, case_no FROM cases", conn)
    if not cases_df.empty:
        case_id = st.selectbox("اختر القضية", cases_df['id'], format_func=lambda x: cases_df[cases_df['id']==x]['case_no'].values[0])
        
        with st.expander("➕ إضافة جلسة"):
            s_date = st.date_input("تاريخ الجلسة")
            s_req = st.text_input("المطلوب")
            s_dec = st.text_area("القرار")
            if st.button("حفظ الجلسة"):
                c.execute("INSERT INTO sessions (case_id, session_date, requirements, decision) VALUES (?,?,?,?)", (int(case_id), s_date, s_req, s_dec))
                conn.commit()
                st.info("تمت الإضافة")
        
        # تم تصحيح السطر الذي سبب المشكلة هنا
        history_query = f"SELECT session_date, requirements, decision FROM sessions WHERE case_id = {int(case_id)} ORDER BY session_date DESC"
        history = pd.read_sql_query(history_query, conn)
        st.dataframe(history)

# --- 4. البحث ---
elif choice == "🔍 بحث وتقارير":
    st.title("🔍 البحث")
    search = st.text_input("رقم القضية أو الخصم")
    if search:
        res = pd.read_sql_query(f"SELECT * FROM cases WHERE case_no LIKE '%{search}%' OR opponent LIKE '%{search}%'", conn)
    else:
        res = pd.read_sql_query("SELECT * FROM cases", conn)
    st.dataframe(res)

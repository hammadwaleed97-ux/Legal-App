import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# --- إعدادات الصفحة ---
st.set_page_config(page_title="نظام الإدارة القانونية", layout="wide", initial_sidebar_state="expanded")

# --- إدارة قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('legal_management.db')
    c = conn.cursor()
    # جدول القضايا الأساسي
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  case_no TEXT, 
                  year TEXT,
                  court TEXT, 
                  opponent TEXT, 
                  case_type TEXT, 
                  subject TEXT,
                  status TEXT)''')
    # جدول الجلسات
    c.execute('''CREATE TABLE IF NOT EXISTS sessions 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  case_id INTEGER, 
                  session_date DATE, 
                  requirements TEXT, 
                  decision TEXT,
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
    
    col1, col2, col3 = st.columns(3)
    total_cases = pd.read_sql_query("SELECT COUNT(*) FROM cases", conn).iloc[0,0]
    upcoming_sessions = pd.read_sql_query(f"SELECT COUNT(*) FROM sessions WHERE session_date >= '{datetime.now().date()}'", conn).iloc[0,0]
    
    col1.metric("إجمالي القضايا", total_cases)
    col2.metric("جلسات قادمة", upcoming_sessions)
    col3.metric("الحالة", "متصل")

    st.subheader("🗓️ أحدث الجلسات المضافة")
    latest_sessions = pd.read_sql_query("""
        SELECT cases.case_no, sessions.session_date, sessions.decision 
        FROM sessions 
        JOIN cases ON cases.id = sessions.case_id 
        ORDER BY sessions.id DESC LIMIT 5""", conn)
    st.table(latest_sessions)

# --- 2. إضافة قضية جديدة ---
elif choice == "➕ إضافة قضية جديدة":
    st.title("📝 تسجيل قضية جديدة")
    with st.form("case_form"):
        col1, col2 = st.columns(2)
        with col1:
            case_no = st.text_input("رقم القضية")
            year = st.text_input("السنة القضائية")
            court = st.text_input("المحكمة / الدائرة")
        with col2:
            opponent = st.text_input("اسم الخصم")
            case_type = st.selectbox("نوع القضية", ["مدني", "إداري", "عمالي", "تأديب", "جنح", "أخرى"])
            status = st.selectbox("حالة القضية", ["متداولة", "محجوزة للحكم", "منتهية"])
        
        subject = st.text_area("موضوع القضية")
        
        submit = st.form_submit_button("حفظ القضية في النظام")
        
        if submit:
            if case_no and opponent:
                c.execute("INSERT INTO cases (case_no, year, court, opponent, case_type, subject, status) VALUES (?,?,?,?,?,?,?)", 
                          (case_no, year, court, opponent, case_type, subject, status))
                conn.commit()
                st.success(f"تم تسجيل القضية رقم {case_no} بنجاح!")
            else:
                st.error("يرجى إدخال رقم القضية واسم الخصم على الأقل.")

# --- 3. إدارة الجلسات ---
elif choice == "📅 إدارة الجلسات":
    st.title("⚖️ متابعة الجلسات والقرارات")
    
    # اختيار القضية أولاً
    cases_df = pd.read_sql_query("SELECT id, case_no || ' لعام ' || year as case_desc FROM cases", conn)
    if not cases_df.empty:
        selected_case_desc = st.selectbox("اختر القضية لإضافة جلسة لها", cases_df['case_desc'])
        case_id = cases_df[cases_df['case_desc'] == selected_case_desc]['id'].values[0]
        
        with st.expander("➕ إضافة جلسة جديدة لهذه القضية"):
            s_date = st.date_input("تاريخ الجلسة")
            s_req = st.text_input("المطلوب للجلسة")
            s_dec = st.text_area("قرار الجلسة (في حال انتهت)")
            if st.button("حفظ الجلسة"):
                c.execute("INSERT INTO sessions (case_id, session_date, requirements, decision) VALUES (?,?,?,?)", 
                          (int(case_id), s_date, s_req, s_dec))
                conn.commit()
                st.info("تمت إضافة الجلسة بنجاح")
        
        st.subheader("📜 تاريخ جلسات هذه القضية")
        history = pd.read_sql_query(f"SELECT session_date, requirements, decision FROM sessions WHERE case_id

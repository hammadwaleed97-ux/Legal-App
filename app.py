import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# --- إعدادات الصفحة ---
st.set_page_config(page_title="نظام الإدارة القانونية", layout="wide", initial_sidebar_state="collapsed")

# تطبيق تنسيق CSS لجعل الأزرار تبدو كقائمة احترافية ومحاذاة النصوص
st.markdown("""
    <style>
    div.row-widget.stButton > button {
        width: 100%;
        border-radius: 20px;
        border: 1px solid #4CAF50;
        color: #4CAF50;
        background-color: white;
        transition: all 0.3s ease;
    }
    div.row-widget.stButton > button:hover {
        background-color: #4CAF50;
        color: white;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .reportview-container .main .block-container{
        padding-top: 1rem;
    }
    /* تحسين محاذاة النص العربي */
    body, p, div, h1, h2, h3, h4, h5, h6 {
        direction: rtl;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

# --- إدارة قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('legal_management.db', check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON") # تفعيل حظر حذف الأب في حال وجود أبناء
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  case_no TEXT, year TEXT, court TEXT, opponent TEXT, 
                  case_type TEXT, subject TEXT, status TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sessions 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  case_id INTEGER, session_date DATE, requirements TEXT, decision TEXT,
                  FOREIGN KEY(case_id) REFERENCES cases(id) ON DELETE CASCADE)''') # الحذف المتتالي للجلسات عند حذف القضية
    conn.commit()
    return conn

conn = init_db()
c = conn.cursor()

# --- إدارة الحالة (Navigation) ---
if 'menu_option' not in st.session_state:
    st.session_state['menu_option'] = 'dashboard'

# --- القائمة الرئيسية في الأعلى ---
st.write("---")
col_title, col1, col2, col3, col4 = st.columns([2, 1, 1, 1, 1])

with col_title:
    st.markdown("### ⚖️ القائمة الرئيسية")

with col1:
    if st.button("🏠 لوحة التحكم"):
        st.session_state['menu_option'] = 'dashboard'
with col2:
    if st.button("➕ إضافة قضية"):
        st.session_state['menu_option'] = 'add_case'
with col3:
    if st.button("📅 إدارة الجلسات"):
        st.session_state['menu_option'] = 'manage_sessions'
with col4:
    if st.button("🔍 بحث وإدارة"):
        st.session_state['menu_option'] = 'search_and_manage'
st.write("---")


# --- التنفيذ بناءً على الخيار المحدد ---

# --- 1. لوحة التحكم ---
if st.session_state['menu_option'] == 'dashboard':
    st

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import io

# --- 1. إعدادات الصفحة الرسمية ---
st.set_page_config(page_title="نظام الشئون القانونية - البحيرة", layout="wide")

# دالة هندسية لإجبار الوورد على الاتجاه العربي (يمين لليسار) ومنع القلب
def make_docx_rtl(doc):
    for section in doc.sections:
        sectPr = section._sectPr
        bidi = OxmlElement('w:bidi')
        bidi.set(qn('w:val'), '1')
        sectPr.append(bidi)
    
    for paragraph in doc.paragraphs:
        p_pr = paragraph._element.get_or_add_pPr()
        p_bidi = OxmlElement('w:bidi')
        p_bidi.set(qn('w:val'), '1')
        p_pr.append(p_bidi)
        paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT

def set_table_rtl(table):
    tblPr = table._element.xpath('w:tblPr')[0]
    bidi = OxmlElement('w:bidi')
    bidi.set(qn('w:val'), '1')
    tblPr.append(bidi)

# --- 2. قاعدة البيانات (هيكلة شاملة) ---
def init_db():
    conn = sqlite3.connect('legal_beheira_v6_pro.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  c_type TEXT, c_no TEXT, c_year TEXT, court TEXT, circuit TEXT,
                  plaintiff TEXT, defendant TEXT, subject TEXT, 
                  lawyer TEXT, last_proc TEXT, appeal_deadline DATE, reg_date DATE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sessions 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, case_id INTEGER, 
                  s_date DATE, decision TEXT)''')
    conn.commit()
    return conn

conn = init_db()

# --- 3. الواجهة الرئيسية ---
st.markdown("<h2 style='text-align: center;'>⚖️ الهيئة القومية للتأمين الاجتماعي</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>منطقة البحيرة - الإدارة العامة للشئون القانونية</h4>", unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'dash'

m = st.columns(4)
if m[0].button("🏠 الرئيسية والبحث"): st.session_state.page = 'dash'
if m[1].button("➕ قيد دعوى/طعن"): st.session_state.page = 'add'
if m[2].button("📅 الجلسات والتفاصيل"): st.session_state.page = 'sess'
if m[3].button("📄 التقارير الرسمية"): st.session_state.page = 'rep'

st.divider()

# --- 4. الصفحات ---

if st.session_state.page == 'dash':
    st.subheader("🔔 لوحة التنبيهات والبحث")
    today = datetime.now().date()
    
    c1, c2 = st.columns(2)
    with c1:
        # عرض تنبيهات الجلسات ببيانات كاملة (رقم، سنة، محكمة)
        df_s = pd.read_sql(f"SELECT c.c_no, c.c_year, c.court, s.s_date FROM sessions s JOIN cases c ON s.case_id = c.id WHERE s.s_date BETWEEN '{today}' AND '{(today + timedelta(days=7))}'", conn)
        if not df_s.empty:
            for _, r in df_s.iterrows():
                st.warning(f"🗓️ جلسة: {r['c_no']} / {r['c_year']} - {r['court']} (يوم {r['s_date']})")
        else: st.info("لا توجد جلسات عاجلة هذا الأسبوع")

    with c2:
        df_a = pd.read_sql(f"SELECT c_no, c_year, appeal_deadline FROM cases WHERE appeal_deadline BETWEEN '{today}' AND '{(today + timedelta(days=10))}'", conn)
        if not df_a.empty:
            for _, r in df_a.iterrows():
                st.error(f"🚨 طعن أوشك على الانتهاء: {r['c_no']} / {r['c_year']} بتاريخ {r['appeal_deadline']}")

    st.divider()
    search = st.text_input("🔍 ابحث (برقم القضية، المحامي، أو المدعي)")
    sql = "SELECT c_no as 'رقم القضية', c_year as 'السنة', c_type as 'النوع', plaintiff as 'المدعي', lawyer as 'المحامي', last_proc as 'آخر إجراء' FROM cases"
    if search:
        sql += f" WHERE c_no LIKE '%{search}%' OR lawyer LIKE '%{search}%' OR plaintiff LIKE '%{search}%'"
    df = pd.read_sql(sql, conn)
    if not df.empty:
        df.insert(0, 'م', range(1, len(df)+1))
        st.table(df)

elif st.session_state.page == 'add':
    st.subheader("📝 قيد ملف قانوني جديد")
    
    # التحقق من التكرار "قبل" الحفظ
    c_no = st.text_input("رقم القضية")
    c_yr = st.text_input("السنة")
    
    blocked = False
    if c_no and c_yr:
        check = pd.read_sql(f"SELECT id FROM cases WHERE c_no='{c_no}' AND c_year='{c_yr}'", conn)
        if not check.empty:
            st.error(f"⚠️ خطأ: القضية {c_no} لعام {c_yr} موجودة مسبقاً! النظام لن يسمح بتكرارها.")
            blocked = True

    with st.form("add_form"):
        ctype = st.selectbox("نوع القيد", ["دعوى", "طعن"])
        ct = st.text_input("المح

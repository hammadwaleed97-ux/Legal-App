import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io

# --- إعدادات الصفحة ---
st.set_page_config(page_title="نظام الإدارة القانونية", layout="wide")

# تنسيق الواجهة لجعلها تبدو كبرنامج احترافي
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #f0f2f6;
        border: 1px solid #d1d5db;
    }
    .main-title {
        text-align: center;
        color: #1e3a8a;
        margin-bottom: 20px;
    }
    div[data-testid="stVerticalBlock"] > div:has(div.stButton) {
        text-align: center;
    }
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
    c.execute('''CREATE TABLE IF NOT EXISTS sessions 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, case_id INTEGER, 
                  session_date DATE, decision TEXT)''')
    conn.commit()
    return conn

conn = init_db()
c = conn.cursor()

# --- وظيفة إنشاء ملف Word ---
def create_word_report(df, lawyer_name, date_from, date_to):
    doc = Document()
    
    # رأس الصفحة (اللوجو والبيانات)
    header = doc.sections[0].header
    p = header.paragraphs[0]
    p.text = "الهيئة القومية للتأمين الاجتماعي\nالادارة العامة للشئون القانونية\nمنطقة البحيرة"
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # العنوان الرئيسي
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run(f"\nبيان بالدعاوى المتداولة طرف الأستاذ / {lawyer_name}")
    run.bold = True
    run.font.size = Pt(14)
    
    doc.add_paragraph(f"عن الفترة من {date_from} حتى {date_to}").alignment = WD_ALIGN_PARAGRAPH.CENTER

    # إنشاء الجدول
    table = doc.add_table(rows=1, cols=9)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    headers = ['م', 'رقم الدعوى / سنة', 'المحكمة', 'الدائرة', 'المدعي', 'المدعى عليه', 'موضوع الدعوى', 'آخر إجراء', 'المحامي المختص']
    
    for i, h in enumerate(headers):
        hdr_cells[i].text = h

    for index, row in df.iterrows():
        row_cells = table.add_row().cells
        row_cells[0].text = str(index + 1)
        row_cells[1].text = f"{row['case_no']} / {row['year']}"
        row_cells[2].text = str(row['court'])
        row_cells[3].text = str(row['circuit'])
        row_cells[4].text = str(row['plaintiff'])
        row_cells[5].text = str(row['defendant'])
        row_cells[6].text = str(row['subject'])
        row_cells[7].text = str(row['status']) # آخر إجراء
        row_cells[8].text = str(row['lawyer'])

    # تحويل الملف إلى Bytes
    target = io.BytesIO()
    doc.save(target)
    return target.getvalue()

# --- القائمة العلوية (بدلاً من الجانبية) ---
st.markdown("<h1 class='main-title'>⚖️ نظام إدارة قضايا الإدارة القانونية</h1>", unsafe_allow_html=True)
menu_cols = st.columns(4)
with menu_cols[0]: btn_dash = st.button("🏠 لوحة التحكم")
with menu_cols[1]: btn_add = st.button("➕ إضافة قضية")
with menu_cols[2]: btn_sessions = st.button("📅 الجلسات")
with menu_cols[3]: btn_reports = st.button("📄 التقارير والحذف")

# إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = 'dash'
if btn_dash: st.session_state.page = 'dash'
if btn_add: st.session_state.page = 'add'
if btn_sessions: st.session_state.page = 'sessions'
if btn_reports: st.session_state.page = 'reports'

# --- 1. لوحة التحكم ---
if st.session_state.page == 'dash':
    total = pd.read_sql_query("SELECT COUNT(*) FROM cases", conn).iloc[0,0]
    st.metric("إجمالي القضايا المسجلة", total)
    st.write("---")
    st.subheader("🗓️ أحدث القضايا المضافة")
    latest = pd.read_sql_query("SELECT case_no, plaintiff, court FROM cases ORDER BY id DESC LIMIT 5", conn)
    st.table(latest)

# --- 2. إضافة قضية ---
elif st.session_state.page == 'add':
    st.subheader("📝 إدخال بيانات دعوى جديدة")
    with st.form("add_form"):
        c1, c2, c3 = st.columns(3)
        case_no = c1.text_input("رقم الدعوى")
        year = c2.text_input("السنة")
        court = c3.text_input("المحكمة")
        
        c4, c5, c6 = st.columns(3)
        circuit = c4.text_input("الدائرة")
        plaintiff = c5.text_input("المدعي")
        defendant = c6.text_input("المدعى عليه")
        
        subject = st.text_area("موضوع الدعوى")
        lawyer = st.text_input("المحامي المختص")
        status = st.text_input("آخر إجراء / الحالة")
        date_added = st.date_input("تاريخ التسجيل بالنظام", datetime.now())
        
        if st.form_submit_button("حفظ البيانات"):
            c.execute("""INSERT INTO cases (case_no, year, court, circuit, plaintiff, defendant, subject, lawyer, status, created_at) 
                         VALUES (?,?,?,?,?,?,?,?,?,?)""", 
                      (case_no, year, court, circuit, plaintiff, defendant, subject, lawyer, status, date_added))
            conn.commit()
            st.success("تم الحفظ بنجاح")

# --- 4. التقارير وإدارة البيانات ---
elif st.session_state.page == 'reports':
    st.subheader("📑 استخراج بيان الدعاوى (Word)")
    
    col_f, col_t = st.columns(2)
    d_from = col_f.date_input("من تاريخ", datetime(2026, 1, 1))
    d_to = col_t.date_input("إلى تاريخ", datetime.now())
    l_name = st.text_input("اسم المحامي المختص لاستخراج البيان")
    
    if st.button("🔍 عرض التقرير"):
        query = f"SELECT * FROM cases WHERE created_at BETWEEN '{d_from}' AND '{d_to}'"
        if l_name:
            query += f" AND lawyer LIKE '%{l_name}%'"
        
        df_report = pd.read_sql_query(query, conn)
        if not df_report.empty:
            st.dataframe(df_report)
            
            word_file = create_word_report(df_report, l_name if l_name else "جميع المحامين", d_from, d_to)
            st.download_button(
                label="📥 تحميل التقرير بصيغة Word",
                data=word_file,
                file_name=f"تقرير_قضايا_{l_name}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        else:
            st.warning("لا توجد بيانات خلال هذه الفترة.")

    st.write("---")
    st.subheader("🗑️ حذف قضية")
    all_cases = pd.read_sql_query("SELECT id, case_no, year FROM cases", conn)
    if not all_cases.empty:
        to_delete = st.selectbox("اختر القضية للحذف", all_cases['id'], format_func=lambda x: f"رقم {all_cases[all_cases['id']==x]['case_no'].values[0]} لسنة {all_cases[all_cases['id']==x]['year'].values[0]}")
        if st.button("❌ حذف نهائي", type="primary"):
            c.execute(f"DELETE FROM cases WHERE id={to_delete}")
            conn.commit()
            st.success("تم الحذف")
            st.rerun()

# (باقي كود الجلسات بنفس المنطق السابق)

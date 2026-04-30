import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
import io

# --- إعدادات الصفحة ---
st.set_page_config(page_title="نظام الإدارة القانونية - البحيرة", layout="wide")

# دالة لتحديد اتجاه الجدول في الوورد ليكون من اليمين لليسار
def set_rtl(table):
    tblPr = table._element.xpath('w:tblPr')[0]
    tblWInd = tblPr.xpath('w:tblWInd')
    if not tblWInd:
        from docx.oxml import OxmlElement
        bidi = OxmlElement('w:bidi')
        bidi.set(qn('w:val'), '1')
        tblPr.append(bidi)

# --- قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('legal_management.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, case_no TEXT, year TEXT, 
                  court TEXT, circuit TEXT, plaintiff TEXT, defendant TEXT, 
                  subject TEXT, lawyer TEXT, status TEXT, appeal_deadline DATE, created_at DATE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sessions 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, case_id INTEGER, 
                  session_date DATE, decision TEXT)''')
    conn.commit()
    return conn

conn = init_db()

# --- وظيفة إنشاء التقرير (ضبط الاتجاه) ---
def create_styled_report(df, lawyer_name, d1, d2):
    doc = Document()
    # ضبط اللغة العربية للمستند
    style = doc.styles['Normal']
    style.font.name = 'Arial'
    style.element.rPr.append(OxmlElement('w:lang', {qn('w:val'): 'ar-SA'}))

    header = doc.add_paragraph()
    header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    header.add_run("الهيئة القومية للتأمين الاجتماعي\nالادارة العامة للشئون القانونية\nمنطقة البحيرة").bold = True

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.add_run(f"\nبيان بالدعاوى المتداولة طرف الأستاذ / {lawyer_name}").bold = True
    doc.add_paragraph(f"عن الفترة من {d1} حتى {d2}").alignment = WD_ALIGN_PARAGRAPH.CENTER

    table = doc.add_table(rows=1, cols=9)
    table.style = 'Table Grid'
    set_rtl(table) # ضبط الجدول ليكون من اليمين لليسار
    
    headers = ['م', 'رقم الدعوى/سنة', 'المحكمة', 'الدائرة', 'المدعي', 'المدعى عليه', 'الموضوع', 'الإجراء', 'المحامي']
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    for idx, row in df.iterrows():
        cells = table.add_row().cells
        cells[0].text = str(idx + 1)
        cells[1].text = f"{row['case_no']} / {row['year']}"
        cells[2].text = str(row['court'])
        cells[3].text = str(row['circuit'])
        cells[4].text = str(row['plaintiff'])
        cells[5].text = str(row['defendant'])
        cells[6].text = str(row['subject'])
        cells[7].text = str(row['status'])
        cells[8].text = str(row['lawyer'])
        for cell in cells: cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    out = io.BytesIO()
    doc.save(out)
    return out.getvalue()

# --- واجهة المستخدم ---
st.markdown("<h1 style='text-align: center;'>⚖️ الإدارة القانونية - منطقة البحيرة</h1>", unsafe_allow_html=True)

menu = st.columns(4)
if 'page' not in st.session_state: st.session_state.page = 'dash'

if menu[0].button("🏠 لوحة التحكم"): st.session_state.page = 'dash'
if menu[1].button("➕ إضافة قضية"): st.session_state.page = 'add'
if menu[2].button("📅 الجلسات"): st.session_state.pg = 'sessions'
if menu[3].button("📄 التقارير"): st.session_state.page = 'reports'

# --- 1. لوحة التحكم (التنبيهات والملخص) ---
if st.session_state.page == 'dash':
    st.subheader("🔔 تنبيهات المواعيد الهامة")
    today = datetime.now().date()
    
    # تنبيه الجلسات (خلال أسبوع)
    next_week = today + timedelta(days=7)
    alert_sessions = pd.read_sql(f"""
        SELECT c.case_no, c.year, s.session_date 
        FROM sessions s JOIN cases c ON s.case_id = c.id 
        WHERE s.session_date BETWEEN '{today}' AND '{next_week}'""", conn)
    
    if not alert_sessions.empty:
        for _, row in alert_sessions.iterrows():
            st.warning(f"⚠️ جلسة قادمة: قضية {row['case_no']}/{row['year']} بتاريخ {row['session_date']}")
    
    # تنبيه الطعون (خلال 10 أيام)
    deadline_limit = today + timedelta(days=10)
    alert_appeals = pd.read_sql(f"SELECT case_no, year, appeal_deadline FROM cases WHERE appeal_deadline BETWEEN '{today}' AND '{deadline_limit}'", conn)
    if not alert_appeals.empty:
        for _, row in alert_appeals.iterrows():
            st.error(f"🚨 ميعاد طعن وشيك: قضية {row['case_no']}/{row['year']} آخر ميعاد {row['appeal_deadline']}")

    st.markdown("---")
    st.subheader("📊 ملخص القضايا")
    df_display = pd.read_sql("SELECT id, case_no as 'رقم الدعوى', year as 'السنة', court as 'المحكمة', plaintiff as 'المدعي', lawyer as 'المحامي' FROM cases", conn)
    
    if not df_display.empty:
        for idx, row in df_display.iterrows():
            col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 1, 1])
            col1.write(row['رقم الدعوى'])
            col2.write(row['المحكمة'])
            col3.write(row['المحامي'])
            if col4.button("✏️ تعديل", key=f"edit_{row['id']}"):
                st.session_state.edit_id = row['id']
                st.session_state.page = 'edit'
                st.rerun()
            if col5.button("🗑️ حذف", key=f"del_{row['id']}"):
                conn.execute(f"DELETE FROM cases WHERE id={row['id']}")
                conn.commit()
                st.success("تم الحذف")
                st.rerun()
    else:
        st.info("لا توجد قضايا مسجلة.")

# --- 2. إضافة قضية ---
elif st.session_state.page == 'add':
    st.subheader("📝 إضافة دعوى جديدة")
    with st.form("add_form"):
        c1, c2, c3 = st.columns(3)
        no = c1.text_input("رقم الدعوى")
        yr = c2.text_input("السنة")
        ct = c3.text_input("المحكمة")
        cir = st.text_input("الدائرة")
        pl = st.text_input("المدعي")
        df = st.text_input("المدعى عليه")
        sub = st.text_area("الموضوع")
        law = st.text_input("المحامي المختص")
        stt = st.text_input("آخر إجراء")
        appeal = st.date_input("ميعاد الطعن (إن وجد)", value=None)
        
        if st.form_submit_button("حفظ القضية"):
            conn.execute("INSERT INTO cases (case_no, year, court, circuit, plaintiff, defendant, subject, lawyer, status, appeal_deadline, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                         (no, yr, ct, cir, pl, df, sub, law, stt, appeal, datetime.now().date()))
            conn.commit()
            st.success("تم الحفظ بنجاح")

# --- 3. الجلسات (تم إصلاح العرض) ---
elif st.session_state.pg == 'sessions':
    st.subheader("📅 إدارة الجلسات والقرارات")
    all_cases = pd.read_sql("SELECT id, case_no, year FROM cases", conn)
    if not all_cases.empty:
        case_options = {row['id']: f"{row['case_no']} / {row['year']}" for _, row in all_cases.iterrows()}
        selected_case = st.selectbox("اختر القضية", options=case_options.keys(), format_func=lambda x: case_options[x])
        
        with st.expander("➕ إضافة قرار جلسة جديد"):
            s_date = st.date_input("تاريخ الجلسة")
            s_dec = st.text_area("قرار الجلسة")
            if st.button("حفظ القرار"):
                conn.execute("INSERT INTO sessions (case_id, session_date, decision) VALUES (?,?,?)", (selected_case, s_date, s_dec))
                conn.commit()
                st.success("تم تسجيل القرار")
        
        st.write("📜 سجل جلسات القضية المختارة:")
        sessions_df = pd.read_sql(f"SELECT session_date as 'التاريخ', decision as 'القرار' FROM sessions WHERE case_id={selected_case}", conn)
        st.table(sessions_df)

# --- 4. التقارير ---
elif st.session_state.page == 'reports':
    st.subheader("📄 تقارير الوورد الرسمية")
    d1 = st.date_input("من تاريخ", datetime(2026, 1, 1))
    d2 = st.date_input("إلى تاريخ")
    lawyer = st.text_input("اسم المحامي (اتركه فارغاً للكل)")
    
    if st.button("توليد ملف الوورد"):
        query = f"SELECT * FROM cases WHERE created_at BETWEEN '{d1}' AND '{d2}'"
        if lawyer: query += f" AND lawyer LIKE '%{lawyer}%'"
        res = pd.read_sql(query, conn)
        
        if not res.empty:
            doc_bytes = create_styled_report(res, lawyer if lawyer else "جميع الزملاء", d1, d2)
            st.download_button("📥 تحميل التقرير", doc_bytes, f"report_{datetime.now().strftime('%Y%m%d')}.docx")
        else:
            st.warning("لا توجد بيانات لهذه الفترة.")

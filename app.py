import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from docx import Document
import io

# 1. إعدادات أساسية
st.set_page_config(page_title="نظام الإدارة القانونية", layout="wide")
st.markdown("<h1 style='text-align:center;'>⚖️ نظام قضايا الإدارة القانونية</h1>", unsafe_allow_html=True)

# 2. إنشاء وتحديث قاعدة البيانات
def get_conn():
    conn = sqlite3.connect('legal_management.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, case_no TEXT, year TEXT, 
                  court TEXT, circuit TEXT, plaintiff TEXT, defendant TEXT, 
                  subject TEXT, lawyer TEXT, status TEXT, created_at DATE)''')
    # إضافة الأعمدة الناقصة لضمان عدم حدوث DatabaseError
    cols = [i[1] for i in c.execute("PRAGMA table_info(cases)").fetchall()]
    for col in ['circuit', 'plaintiff', 'defendant', 'lawyer', 'created_at']:
        if col not in cols:
            c.execute(f"ALTER TABLE cases ADD COLUMN {col} TEXT")
    conn.commit()
    return conn

conn = get_conn()

# 3. وظيفة استخراج ملف الوورد
def make_doc(df, name, d1, d2):
    doc = Document()
    doc.add_paragraph("الهيئة القومية للتأمين الاجتماعي\nالادارة القانونية").bold = True
    doc.add_heading(f"بيان بالدعاوى طرف الأستاذ / {name}", 1)
    doc.add_paragraph(f"عن الفترة من {d1} حتى {d2}")
    
    table = doc.add_table(rows=1, cols=9)
    table.style = 'Table Grid'
    headers = ['م', 'رقم الدعوى', 'المحكمة', 'الدائرة', 'المدعي', 'المدعى عليه', 'الموضوع', 'آخر إجراء', 'المحامي']
    for i, h in enumerate(headers): table.rows[0].cells[i].text = h
    
    for i, r in df.iterrows():
        row_cells = table.add_row().cells
        row_cells[0].text = str(i + 1)
        row_cells[1].text = f"{r.get('case_no','')} / {r.get('year','')}"
        row_cells[2].text = str(r.get('court',''))
        row_cells[3].text = str(r.get('circuit',''))
        row_cells[4].text = str(r.get('plaintiff',''))
        row_cells[5].text = str(r.get('defendant',''))
        row_cells[6].text = str(r.get('subject',''))
        row_cells[7].text = str(r.get('status',''))
        row_cells[8].text = str(r.get('lawyer',''))
        
    out = io.BytesIO()
    doc.save(out)
    return out.getvalue()

# 4. أزرار التنقل (بشكل عرضي)
menu = st.columns(4)
if 'pg' not in st.session_state: st.session_state.pg = 'dash'

if menu[0].button("🏠 لوحة التحكم"): st.session_state.pg = 'dash'
if menu[1].button("➕ إضافة قضية"): st.session_state.pg = 'add'
if menu[2].button("📅 الجلسات"): st.session_state.pg = 'sessions'
if menu[3].button("📄 التقارير"): st.session_state.pg = 'rep'

# --- الصفحات ---
if st.session_state.pg == 'dash':
    st.subheader("📊 ملخص القضايا")
    df_all = pd.read_sql("SELECT case_no, year, court FROM cases", conn)
    st.write(f"إجمالي القضايا: {len(df_all)}")
    st.table(df_all.tail(5))

elif st.session_state.pg == 'add':
    with st.form("add"):
        c1, c2, c3 = st.columns(3)
        no = c1.text_input("رقم الدعوى")
        yr = c2.text_input("السنة")
        ct = c3.text_input("المحكمة")
        cir = st.text_input("الدائرة")
        pl = st.text_input("المدعي")
        df = st.text_input("المدعى عليه")
        sub = st.text_area("الموضوع")
        law = st.text_input("المحامي")
        stt = st.text_input("آخر إجراء")
        if st.form_submit_button("حفظ"):
            conn.execute("INSERT INTO cases (case_no, year, court, circuit, plaintiff, defendant, subject, lawyer, status, created_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
                         (no, yr, ct, cir, pl, df, sub, law, stt, datetime.now().date()))
            conn.commit()
            st.success("تم الحفظ")

elif st.session_state.pg == 'rep':
    st.subheader("📄 استخراج تقرير ورد")
    d1 = st.date_input("من", datetime(2026,1,1))
    d2 = st.date_input("إلى")
    name = st.text_input("اسم الأستاذ")
    if st.button("توليد التقرير"):
        query = f"SELECT * FROM cases WHERE created_at BETWEEN '{d1}' AND '{d2}'"
        if name: query += f" AND lawyer LIKE '%{name}%'"
        res = pd.read_sql(query, conn)
        if not res.empty:
            st.dataframe(res)
            doc = make_doc(res, name, d1, d2)
            st.download_button("📥 تحميل ملف Word", doc, "report.docx")
        else: st.warning("لا توجد بيانات")

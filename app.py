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
st.set_page_config(page_title="نظام الشئون القانونية - البحيرة", layout="wide")

def set_table_rtl(table):
    tblPr = table._element.xpath('w:tblPr')[0]
    bidi = OxmlElement('w:bidi')
    bidi.set(qn('w:val'), '1')
    tblPr.append(bidi)

# --- 2. قاعدة البيانات (علاج شامل لكل الخانات) ---
def init_db():
    conn = sqlite3.connect('legal_beheira_final.db', check_same_thread=False)
    c = conn.cursor()
    # إنشاء الجدول الأساسي بكل التفاصيل
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  c_type TEXT, c_no TEXT, c_year TEXT, court TEXT, circuit TEXT,
                  plaintiff TEXT, defendant TEXT, subject TEXT, 
                  lawyer TEXT, last_proc TEXT, appeal_deadline DATE)''')
    
    # علاج "العك" - التأكد من وجود كل الأعمدة في حالة وجود قاعدة قديمة
    existing_cols = [col[1] for col in c.execute("PRAGMA table_info(cases)").fetchall()]
    needed_cols = {
        'c_type': 'TEXT', 'circuit': 'TEXT', 'plaintiff': 'TEXT', 
        'defendant': 'TEXT', 'subject': 'TEXT', 'last_proc': 'TEXT', 
        'appeal_deadline': 'DATE'
    }
    for col, dtype in needed_cols.items():
        if col not in existing_cols:
            c.execute(f"ALTER TABLE cases ADD COLUMN {col} {dtype}")
    
    c.execute('''CREATE TABLE IF NOT EXISTS sessions 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, case_id INTEGER, 
                  s_date DATE, decision TEXT)''')
    conn.commit()
    return conn

conn = init_db()

# --- 3. تصميم الواجهة ---
st.markdown("<h2 style='text-align: center; color: #1e3a8a;'>⚖️ الإدارة العامة للشئون القانونية - ديوان عام منطقة البحيرة</h2>", unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'dash'

# أزرار التنقل الأساسية
m = st.columns(4)
if m[0].button("🏠 الرئيسية والتنبيهات"): st.session_state.page = 'dash'
if m[1].button("➕ إضافة (دعوى/طعن)"): st.session_state.page = 'add'
if m[2].button("📅 الجلسات والتعديل"): st.session_state.page = 'sess'
if m[3].button("📄 التقارير الرسمية"): st.session_state.page = 'rep'

st.divider()

# --- 4. الصفحات ---

if st.session_state.page == 'dash':
    st.subheader("🔔 تنبيهات المواعيد القانونية")
    today = datetime.now().date()
    
    c1, c2 = st.columns(2)
    with c1:
        st.info("🗓️ جلسات قادمة (7 أيام)")
        df_s = pd.read_sql(f"SELECT c.c_no, s.s_date FROM sessions s JOIN cases c ON s.case_id = c.id WHERE s.s_date BETWEEN '{today}' AND '{(today + timedelta(days=7))}'", conn)
        if not df_s.empty: st.warning(f"يوجد {len(df_s)} جلسات")
        else: st.write("لا يوجد")
    with c2:
        st.error("🚨 مواعيد طعن وشيكة")
        df_a = pd.read_sql(f"SELECT c_no, appeal_deadline FROM cases WHERE appeal_deadline BETWEEN '{today}' AND '{(today + timedelta(days=10))}'", conn)
        if not df_a.empty: st.error(f"يوجد {len(df_a)} طعون")
        else: st.write("لا يوجد")

    st.divider()
    st.subheader("🔍 البحث والملخص")
    df_all = pd.read_sql("SELECT id, c_type as 'النوع', c_no as 'الرقم', c_year as 'السنة', subject as 'الموضوع', lawyer as 'المحامي' FROM cases", conn)
    st.dataframe(df_all, use_container_width=True)

elif st.session_state.page == 'add':
    with st.form("add_case"):
        st.subheader("📝 تسجيل بيانات جديدة")
        ctype = st.selectbox("نوع القيد", ["دعوى", "طعن"])
        col1, col2, col3 = st.columns(3)
        no = col1.text_input("رقم القضية")
        yr = col2.text_input("السنة")
        ct = col3.text_input("المحكمة")
        cir = st.text_input("الدائرة")
        p_name = st.text_input("المدعي / المستأنف")
        d_name = st.text_input("المدعى عليه / المستأنف ضده")
        subj = st.text_area("موضوع الدعوى بالتفصيل")
        law = st.text_input("المحامي المختص")
        last = st.text_input("آخر إجراء اتخذ")
        ap_date = st.date_input("ميعاد الطعن", value=None)
        
        if st.form_submit_button("حفظ بالنظام"):
            conn.execute("INSERT INTO cases (c_type, c_no, c_year, court, circuit, plaintiff, defendant, subject, lawyer, last_proc, appeal_deadline) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                         (ctype, no, yr, ct, cir, p_name, d_name, subj, law, last, ap_date))
            conn.commit()
            st.success("تم الحفظ")

elif st.session_state.page == 'sess':
    st.subheader("📅 إدارة الجلسات وتعديل القرارات")
    cases = pd.read_sql("SELECT id, c_no, c_year FROM cases", conn)
    if not cases.empty:
        target = st.selectbox("اختر القضية", cases['id'], format_func=lambda x: f"قضية {cases[cases['id']==x]['c_no'].values[0]}")
        
        with st.expander("📝 إضافة قرار جلسة"):
            sd = st.date_input("التاريخ")
            dec = st.text_area("القرار")
            if st.button("حفظ"):
                conn.execute("INSERT INTO sessions (case_id, s_date, decision) VALUES (?,?,?)", (int(target), sd, dec))
                conn.commit()
                st.rerun()

        st.write("🔄 القرارات السابقة (تعديل مباشر):")
        hist = pd.read_sql(f"SELECT * FROM sessions WHERE case_id={target} ORDER BY s_date DESC", conn)
        for _, row in hist.iterrows():
            new_dec = st.text_area(f"قرار {row['s_date']}", value=row['decision'], key=f"e_{row['id']}")
            c_ed1, c_ed2 = st.columns(2)
            if c_ed1.button("💾 حفظ التعديل", key=f"b_{row['id']}"):
                conn.execute("UPDATE sessions SET decision=? WHERE id=?", (new_dec, row['id']))
                conn.commit()
                st.success("تم التحديث")
            if c_ed2.button("🗑️ حذف", key=f"d_{row['id']}"):
                conn.execute(f"DELETE FROM sessions WHERE id={row['id']}")
                conn.commit()
                st.rerun()

elif st.session_state.page == 'rep':
    st.subheader("📄 التقارير الرسمية (Word)")
    rtype = st.radio("نوع التقرير", ["بيان بالدعاوى", "بيان بالطعون"])
    l_filter = st.text_input("فلترة باسم المحامي (اختياري)")
    
    if st.button("توليد التقرير"):
        search_type = "دعوى" if "دعاوى" in rtype else "طعن"
        q = f"SELECT * FROM cases WHERE c_type='{search_type}'"
        if l_filter: q += f" AND lawyer LIKE '%{l_filter}%'"
        df_rep = pd.read_sql(q, conn)
        
        if not df_rep.empty:
            doc = Document()
            # ترويسة
            h = doc.add_paragraph()
            h.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            h.add_run("الهيئة القومية للتأمين الاجتماعي\nمنطقة البحيرة - الشئون القانونية").bold = True
            
            doc.add_heading(rtype, 1).alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            table = doc.add_table(rows=1, cols=7)
            table.style = 'Table Grid'
            set_table_rtl(table)
            hdrs = ['رقم القضية', 'المحكمة', 'المدعي', 'المدعى عليه', 'الموضوع', 'آخر إجراء', 'المحامي']
            for i, val in enumerate(hdrs): table.rows[0].cells[i].text = val
            
            for _, r in df_rep.iterrows():
                row = table.add_row().cells
                row[0].text = f"{r['c_no']} / {r['c_year']}"
                row[1].text = str(r['court'])
                row[2].text = str(r['plaintiff'])
                row[3].text = str(r['defendant'])
                row[4].text = str(r['subject'])
                row[5].text = str(r['last_proc'])
                row[6].text = str(r['lawyer'])
            
            buf = io.BytesIO()
            doc.save(buf)
            st.download_button("📥 تحميل التقرير", buf.getvalue(), "بيان_رسمي.docx")

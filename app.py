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

# دالة ضبط اتجاه الجدول ونصوص الوورد للعربية (RTL)
def set_table_rtl(table):
    tblPr = table._element.xpath('w:tblPr')[0]
    bidi = OxmlElement('w:bidi')
    bidi.set(qn('w:val'), '1')
    tblPr.append(bidi)

# --- 2. قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('legal_beheira_final_v4.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  c_type TEXT, c_no TEXT, c_year TEXT, court TEXT, circuit TEXT,
                  plaintiff TEXT, defendant TEXT, subject TEXT, 
                  lawyer TEXT, last_proc TEXT, appeal_deadline DATE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sessions 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, case_id INTEGER, 
                  s_date DATE, decision TEXT)''')
    conn.commit()
    return conn

conn = init_db()

# --- 3. الواجهة ---
st.markdown("<h2 style='text-align: center; color: #1e3a8a;'>⚖️ الهيئة القومية للتأمين الاجتماعي</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>منطقة البحيرة - الإدارة العامة للشئون القانونية</h4>", unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'dash'

m = st.columns(4)
if m[0].button("🏠 الرئيسية والتنبيهات"): st.session_state.page = 'dash'
if m[1].button("➕ إضافة (دعوى/طعن)"): st.session_state.page = 'add'
if m[2].button("📅 الجلسات والتفاصيل"): st.session_state.page = 'sess'
if m[3].button("📄 التقارير الرسمية"): st.session_state.page = 'rep'

st.divider()

# --- 4. الصفحات ---

if st.session_state.page == 'dash':
    st.subheader("🔔 التنبيهات والبحث")
    today = datetime.now().date()
    
    col_a, col_b = st.columns(2)
    with col_a:
        df_s = pd.read_sql(f"SELECT c.c_no, s.s_date FROM sessions s JOIN cases c ON s.case_id = c.id WHERE s.s_date BETWEEN '{today}' AND '{(today + timedelta(days=7))}'", conn)
        if not df_s.empty:
            st.warning(f"🗓️ جلسات الأسبوع: {len(df_s)}")
        else: st.success("لا توجد جلسات وشيكة")

    with col_b:
        df_a = pd.read_sql(f"SELECT c_no, appeal_deadline FROM cases WHERE appeal_deadline BETWEEN '{today}' AND '{(today + timedelta(days=10))}'", conn)
        if not df_a.empty:
            st.error(f"🚨 طعون تنتهي قريباً: {len(df_a)}")
        else: st.success("لا توجد طعون عاجلة")

    st.divider()
    # خانة البحث (تم إصلاحها لتعمل فورياً)
    search_q = st.text_input("🔍 ابحث برقم القضية أو اسم المدعي")
    
    sql = "SELECT id, c_no as 'الرقم', c_year as 'السنة', c_type as 'النوع', plaintiff as 'المدعي', subject as 'الموضوع', last_proc as 'آخر إجراء', lawyer as 'المحامي المختص' FROM cases"
    if search_q:
        sql += f" WHERE c_no LIKE '%{search_q}%' OR plaintiff LIKE '%{search_q}%'"
    
    df_all = pd.read_sql(sql, conn)
    if not df_all.empty:
        # عرض "م" بدل الـ ID
        df_all.insert(0, 'م', range(1, 1 + len(df_all)))
        st.table(df_all.drop(columns=['id']))
    else:
        st.info("لا توجد بيانات مطابقة للبحث")

elif st.session_state.page == 'add':
    with st.form("add_case"):
        st.subheader("📝 قيد جديد")
        ctype = st.selectbox("نوع القيد", ["دعوى", "طعن"])
        c1, c2 = st.columns(2)
        no = c1.text_input("رقم القضية")
        yr = c2.text_input("السنة")
        
        ct = st.text_input("المحكمة")
        p_name = st.text_input("المدعي")
        subj = st.text_area("موضوع الدعوى")
        law = st.text_input("المحامي المختص")
        last = st.text_input("آخر إجراء اتخذ")
        ap_date = st.date_input("ميعاد الطعن", value=None)
        
        if st.form_submit_button("حفظ بالنظام"):
            # منع التكرار الحقيقي (Blocker)
            check = pd.read_sql(f"SELECT id FROM cases WHERE c_no='{no}' AND c_year='{yr}'", conn)
            if not check.empty:
                st.error(f"❌ خطأ: القضية رقم {no} لعام {yr} مسجلة بالفعل! لن يتم التكرار.")
            elif not no or not yr:
                st.warning("برجاء إدخال الرقم والسنة")
            else:
                conn.execute("INSERT INTO cases (c_type, c_no, c_year, court, plaintiff, subject, lawyer, last_proc, appeal_deadline) VALUES (?,?,?,?,?,?,?,?,?)",
                             (ctype, no, yr, ct, p_name, subj, law, last, ap_date))
                conn.commit()
                st.success("✅ تم الحفظ بنجاح")

elif st.session_state.page == 'sess':
    st.subheader("📂 ملفات القضايا والجلسات")
    cases = pd.read_sql("SELECT id, c_no, c_year, plaintiff, lawyer, last_proc FROM cases", conn)
    if not cases.empty:
        choice = st.selectbox("اختر القضية", cases['id'], format_func=lambda x: f"رقم {cases[cases['id']==x]['c_no'].values[0]} - {cases[cases['id']==x]['plaintiff'].values[0]}")
        
        c_data = pd.read_sql(f"SELECT * FROM cases WHERE id={choice}", conn).iloc[0]
        st.info(f"👤 **المحامي:** {c_data['lawyer']} | **آخر إجراء:** {c_data['last_proc']}")
        
        with st.expander("📝 إضافة جلسة"):
            sd = st.date_input("التاريخ")
            dec = st.text_area("القرار")
            if st.button("حفظ"):
                conn.execute("INSERT INTO sessions (case_id, s_date, decision) VALUES (?,?,?)", (int(choice), sd, dec))
                conn.commit()
                st.rerun()

        st.write("📜 السجل تاريخي:")
        hist = pd.read_sql(f"SELECT * FROM sessions WHERE case_id={choice} ORDER BY s_date DESC", conn)
        for _, row in hist.iterrows():
            st.text_area(f"جلسة {row['s_date']}", value=row['decision'], disabled=True)

elif st.session_state.page == 'rep':
    st.subheader("📄 توليد التقارير الرسمية")
    c1, c2, c3 = st.columns(3)
    
    # التقارير المنفصلة (3 خانات)
    rep_all = c1.button("📑 تقرير شامل (دعاوى وطعون)")
    rep_cases = c2.button("📂 تقرير الدعاوى فقط")
    rep_appeals = c3.button("⚖️ تقرير الطعون فقط")
    
    target_type = None
    if rep_all: target_type = "الكل"
    if rep_cases: target_type = "دعوى"
    if rep_appeals: target_type = "طعن"
    
    if target_type:
        sql = "SELECT * FROM cases"
        if target_type != "الكل": sql += f" WHERE c_type='{target_type}'"
        df_rep = pd.read_sql(sql, conn)
        
        if not df_rep.empty:
            doc = Document()
            h = doc.add_paragraph()
            h.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            h.add_run("الهيئة القومية للتأمين الاجتماعي\nالإدارة العامة للشئون القانونية - البحيرة").bold = True
            
            table = doc.add_table(rows=1, cols=7)
            table.style = 'Table Grid'
            set_table_rtl(table)
            hdrs = ['م', 'رقم القضية', 'النوع', 'المدعي', 'الموضوع', 'آخر إجراء', 'المحامي المختص']
            for i, val in enumerate(hdrs): table.rows[0].cells[i].text = val
            
            for i, r in enumerate(df_rep.itertuples()):
                row = table.add_row().cells
                row[0].text = str(i+1)
                row[1].text = f"{r.c_no} / {r.c_year}"
                row[2].text = str(r.c_type)
                row[3].text = str(r.plaintiff)
                row[4].text = str(r.subject)
                row[5].text = str(r.last_proc)
                row[6].text = str(r.lawyer)
                
            buf = io.BytesIO()
            doc.save(buf)
            st.download_button(f"📥 تحميل {target_type}", buf.getvalue(), f"report_{target_type}.docx")

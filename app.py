import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import io

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="نظام الشئون القانونية - البحيرة", layout="wide")

# دالة سحرية لضبط الوورد ليكون عربي 100% ومن اليمين لليسار
def force_rtl_and_arabic(doc):
    for section in doc.sections:
        # ضبط اتجاه الصفحة لليمين
        sectPr = section._sectPr
        bidi = OxmlElement('w:bidi')
        bidi.set(qn('w:val'), '1')
        sectPr.append(bidi)
    
    # ضبط كل فقرة في المستند
    for paragraph in doc.paragraphs:
        p_pr = paragraph._element.get_or_add_pPr()
        p_bidi = OxmlElement('w:bidi')
        p_bidi.set(qn('w:val'), '1')
        p_pr.append(p_bidi)
        paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT

def set_table_rtl_and_width(table):
    # جعل الجدول من اليمين لليسار
    tblPr = table._element.xpath('w:tblPr')[0]
    bidi = OxmlElement('w:bidi')
    bidi.set(qn('w:val'), '1')
    tblPr.append(bidi)
    # جعل الجدول يملأ عرض الصفحة 100%
    tblW = OxmlElement('w:tblW')
    tblW.set(qn('w:type'), 'dxa')
    tblW.set(qn('w:w'), '9000') # عرض تقريبي يملأ الصفحة A4
    tblPr.append(tblW)

# --- 2. قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('legal_beheira_v7.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  c_type TEXT, c_no TEXT, c_year TEXT, court TEXT, 
                  plaintiff TEXT, subject TEXT, lawyer TEXT, 
                  last_proc TEXT, appeal_deadline DATE, reg_date DATE)''')
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

# --- 4. معالجة الصفحات ---

if st.session_state.page == 'dash':
    st.subheader("🔍 البحث السريع")
    search = st.text_input("ابحث برقم القضية أو اسم المدعي")
    sql = "SELECT c_no as 'الرقم', c_year as 'السنة', c_type as 'النوع', plaintiff as 'المدعي', lawyer as 'المحامي', last_proc as 'آخر إجراء' FROM cases"
    if search:
        sql += f" WHERE c_no LIKE '%{search}%' OR plaintiff LIKE '%{search}%'"
    df = pd.read_sql(sql, conn)
    if not df.empty:
        df.insert(0, 'م', range(1, len(df)+1))
        st.table(df)

elif st.session_state.page == 'add':
    st.subheader("📝 قيد ملف جديد")
    c_no = st.text_input("رقم القضية")
    c_yr = st.text_input("السنة")
    
    # حظر التكرار الحقيقي
    is_dup = False
    if c_no and c_yr:
        check = pd.read_sql(f"SELECT id FROM cases WHERE c_no='{c_no}' AND c_year='{c_yr}'", conn)
        if not check.empty:
            st.error(f"❌ خطأ: القضية {c_no} لعام {c_yr} مسجلة بالفعل!")
            is_dup = True

    with st.form("add_form"):
        ctype = st.selectbox("النوع", ["دعوى", "طعن"])
        ct = st.text_input("المحكمة")
        pl = st.text_input("المدعي")
        sub = st.text_area("الموضوع")
        law = st.text_input("المحامي المختص")
        last = st.text_input("آخر إجراء")
        ap_d = st.date_input("ميعاد الطعن", value=None)
        reg_d = st.date_input("تاريخ القيد", value=datetime.now().date())
        
        if st.form_submit_button("حفظ", disabled=is_dup):
            conn.execute("INSERT INTO cases (c_type, c_no, c_year, court, plaintiff, subject, lawyer, last_proc, appeal_deadline, reg_date) VALUES (?,?,?,?,?,?,?,?,?,?)",
                         (ctype, c_no, c_yr, ct, pl, sub, law, last, ap_d, reg_d))
            conn.commit()
            st.success("تم الحفظ")

elif st.session_state.page == 'rep':
    st.subheader("📄 توليد التقارير")
    col1, col2 = st.columns(2)
    d_f = col1.date_input("من تاريخ")
    d_t = col2.date_input("إلى تاريخ")
    law_name = st.text_input("اسم المحامي (ليظهر في العنوان)")
    
    c1, c2, c3 = st.columns(3)
    r_type = None
    if c1.button("📑 تقرير شامل"): r_type, r_txt = "الكل", "الدعاوى والطعون"
    if c2.button("📂 تقرير الدعاوى"): r_type, r_txt = "دعوى", "الدعاوى"
    if c3.button("⚖️ تقرير الطعون"): r_type, r_txt = "طعن", "الطعون"
    
    if r_type:
        sql = "SELECT * FROM cases WHERE 1=1"
        if r_type != "الكل": sql += f" AND c_type='{r_type}'"
        if d_f and d_t: sql += f" AND reg_date BETWEEN '{d_f}' AND '{d_t}'"
        
        df_rep = pd.read_sql(sql, conn)
        if not df_rep.empty:
            doc = Document()
            force_rtl_and_arabic(doc)
            
            # الترويسة
            h = doc.add_paragraph()
            h.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            h.add_run("الهيئة القومية للتأمين الاجتماعي\nالإدارة العامة للشئون القانونية - البحيرة").bold = True
            
            # العنوان المطلوب
            title = doc.add_paragraph()
            title.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = title.add_run(f"\nبيان ب{r_txt} المتداولة طرف الأستاذ/ {law_name}")
            run.bold = True
            run.font.size = Pt(14)
            
            table = doc.add_table(rows=1, cols=7)
            table.style = 'Table Grid'
            set_table_rtl_and_width(table)
            
            hdrs = ['م', 'رقم القضية', 'المحكمة', 'المدعي', 'الموضوع', 'آخر إجراء', 'المحامي']
            for i, val in enumerate(hdrs):
                cell = table.rows[0].cells[i]
                cell.text = val
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            for i, r in enumerate(df_rep.itertuples()):
                row = table.add_row().cells
                row[0].text = str(i+1)
                row[1].text = f"{r.c_no} / {r.c_year}"
                row[2].text = str(r.court)
                row[3].text = str(r.plaintiff)
                row[4].text = str(r.subject)
                row[5].text = str(r.last_proc)
                row[6].text = str(r.lawyer)
                for cell in row: cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            buf = io.BytesIO()
            doc.save(buf)
            st.download_button(f"📥 تحميل التقرير", buf.getvalue(), "Report.docx")

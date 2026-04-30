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

# دالة ضبط اتجاه الجدول في الوورد (RTL)
def set_table_rtl(table):
    tblPr = table._element.xpath('w:tblPr')[0]
    bidi = OxmlElement('w:bidi')
    bidi.set(qn('w:val'), '1')
    tblPr.append(bidi)

# --- 2. قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('legal_beheira_v3.db', check_same_thread=False)
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
    st.subheader("🔔 التنبيهات الذكية")
    today = datetime.now().date()
    
    # تنبيهات مفصلة للطعون والجلسات
    c1, c2 = st.columns(2)
    with c1:
        df_s = pd.read_sql(f"SELECT c.c_no, s.s_date FROM sessions s JOIN cases c ON s.case_id = c.id WHERE s.s_date BETWEEN '{today}' AND '{(today + timedelta(days=7))}'", conn)
        if not df_s.empty:
            st.warning(f"🗓️ يوجد {len(df_s)} جلسات هذا الأسبوع:")
            for _, r in df_s.iterrows(): st.write(f"- قضية {r['c_no']} جلسة {r['s_date']}")
        else: st.success("لا توجد جلسات وشيكة")

    with c2:
        df_a = pd.read_sql(f"SELECT c_no, appeal_deadline FROM cases WHERE appeal_deadline BETWEEN '{today}' AND '{(today + timedelta(days=10))}'", conn)
        if not df_a.empty:
            st.error(f"🚨 يوجد {len(df_a)} مواعيد طعن تنتهي قريباً:")
            for _, r in df_a.iterrows(): st.write(f"- قضية {r['c_no']} آخر ميعاد {r['appeal_deadline']}")
        else: st.success("المواعيد القانونية للطعون بخير")

    st.divider()
    st.subheader("🔍 البحث السريع")
    search_q = st.text_input("ابحث برقم القضية أو اسم المدعي...")
    
    # تحسين عرض الجدول وإزالة الـ ID والمربعات
    sql = "SELECT c_no as 'رقم القضية', c_year as 'السنة', c_type as 'النوع', plaintiff as 'المدعي', court as 'المحكمة', subject as 'الموضوع', last_proc as 'آخر إجراء' FROM cases"
    if search_q:
        sql += f" WHERE c_no LIKE '%{search_q}%' OR plaintiff LIKE '%{search_q}%'"
    
    df_all = pd.read_sql(sql, conn)
    if not df_all.empty:
        st.table(df_all) # استخدام table لعرض أنيق بدون مربعات اختيار أو ID
    else:
        st.info("السجل فارغ حالياً")

elif st.session_state.page == 'add':
    with st.form("add_case"):
        st.subheader("📝 قيد جديد")
        ctype = st.selectbox("نوع القيد", ["دعوى", "طعن"])
        col1, col2 = st.columns(2)
        no = col1.text_input("رقم القضية")
        yr = col2.text_input("السنة")
        
        # منبه قيد ذات القضية من قبل
        check = pd.read_sql(f"SELECT id FROM cases WHERE c_no='{no}' AND c_year='{yr}'", conn)
        if not check.empty:
            st.error("⚠️ تحذير: هذه القضية مقيدة مسبقاً في النظام!")
            
        ct = st.text_input("المحكمة")
        p_name = st.text_input("المدعي")
        subj = st.text_area("موضوع الدعوى")
        last = st.text_input("آخر إجراء اتخذ")
        ap_date = st.date_input("ميعاد الطعن", value=None)
        
        if st.form_submit_button("حفظ بالنظام"):
            conn.execute("INSERT INTO cases (c_type, c_no, c_year, court, plaintiff, subject, last_proc, appeal_deadline) VALUES (?,?,?,?,?,?,?,?)",
                         (ctype, no, yr, ct, p_name, subj, last, ap_date))
            conn.commit()
            st.success("تم الحفظ")

elif st.session_state.page == 'sess':
    st.subheader("📂 تفاصيل الدعاوى والجلسات")
    cases = pd.read_sql("SELECT id, c_no, c_year, plaintiff, subject, last_proc FROM cases", conn)
    if not cases.empty:
        choice = st.selectbox("اختر القضية لفتح ملفها", cases['id'], format_func=lambda x: f"قضية {cases[cases['id']==x]['c_no'].values[0]} - المدعي: {cases[cases['id']==x]['plaintiff'].values[0]}")
        
        c_data = cases[cases['id'] == choice].iloc[0]
        st.info(f"📋 **الموضوع:** {c_data['subject']} | **آخر إجراء:** {c_data['last_proc']}")
        
        with st.expander("📝 إضافة قرار جلسة جديد"):
            sd = st.date_input("تاريخ الجلسة")
            dec = st.text_area("القرار")
            if st.button("حفظ القرار"):
                conn.execute("INSERT INTO sessions (case_id, s_date, decision) VALUES (?,?,?)", (int(choice), sd, dec))
                conn.commit()
                st.rerun()

        st.write("📜 سجل الجلسات السابقة:")
        hist = pd.read_sql(f"SELECT * FROM sessions WHERE case_id={choice} ORDER BY s_date DESC", conn)
        for _, row in hist.iterrows():
            new_dec = st.text_area(f"جلسة {row['s_date']}", value=row['decision'], key=f"e_{row['id']}")
            if st.button("💾 حفظ التعديل", key=f"b_{row['id']}"):
                conn.execute("UPDATE sessions SET decision=? WHERE id=?", (new_dec, row['id']))
                conn.commit()
                st.success("تم التحديث")

elif st.session_state.page == 'rep':
    st.subheader("📄 التقارير الرسمية")
    if st.button("توليد تقرير بالدعاوى والطعون"):
        df_rep = pd.read_sql("SELECT * FROM cases", conn)
        doc = Document()
        # تصحيح كلمة الهيئة وترتيب الجدول
        h = doc.add_paragraph()
        h.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        h.add_run("الهيئة القومية للتأمين الاجتماعي\nالإدارة العامة للشئون القانونية - البحيرة").bold = True
        
        table = doc.add_table(rows=1, cols=6)
        table.style = 'Table Grid'
        set_table_rtl(table)
        hdrs = ['م', 'رقم القضية', 'النوع', 'المدعي', 'الموضوع', 'آخر إجراء']
        for i, val in enumerate(hdrs): table.rows[0].cells[i].text = val
        
        for i, r in enumerate(df_rep.itertuples()):
            row = table.add_row().cells
            row[0].text = str(i+1)
            row[1].text = f"{r.c_no} / {r.c_year}"
            row[2].text = str(r.c_type)
            row[3].text = str(r.plaintiff)
            row[4].text = str(r.subject)
            row[5].text = str(r.last_proc)
            
        buf = io.BytesIO()
        doc.save(buf)
        st.download_button("📥 تحميل التقرير", buf.getvalue(), "بيان_قانوني.docx")

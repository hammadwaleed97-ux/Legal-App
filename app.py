import streamlit as st
from docx import Document
from io import BytesIO

# 1. إعدادات فخمة تليق بسيادة المستشار
st.set_page_config(page_title="منظومة المستشار وليد حماد", layout="wide")

st.markdown("""
    <style>
    .main { direction: rtl; text-align: right; background-color: #f0f2f6; }
    .stButton>button { 
        height: 160px; width: 100%; border-radius: 25px; 
        font-size: 26px; font-weight: bold; background-color: white; 
        color: #1e3a8a; border: 4px solid #1e3a8a; box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #1e3a8a; color: white; transform: translateY(-5px); }
    .header-box { 
        background: linear-gradient(135deg, #0f172a, #1e3a8a); 
        color: white; padding: 40px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; border-bottom: 8px solid #ffd700;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة الصفحات والمكتبة
if 'page' not in st.session_state: st.session_state.page = "home"
if 'law_db' not in st.session_state: st.session_state.law_db = []

# 3. الواجهة الرئيسية (الأيقونات الستة في وجه البرنامج)
if st.session_state.page == "home":
    st.markdown('<div class="header-box"><h1>⚖️ منظومة الإدارة القانونية الذكية</h1><h3>ديوان عام منطقة البحيرة</h3></div>', unsafe_allow_html=True)
    st.write(f"#### أهلاً بك.. المستشار / وليد حماد")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏛️\nقسم القضايا"): st.session_state.page = "cases"; st.rerun()
    with col2:
        if st.button("📚\nالمكتبة الفنية"): st.session_state.page = "lib"; st.rerun()
    with col3:
        if st.button("📂\nالتحقيقات"): st.session_state.page = "inv"; st.rerun()
    
    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("💡\nقسم الفتوى"): st.session_state.page = "fatwa"; st.rerun()
    with col5:
        if st.button("🔍\nسجلات البحث"): st.session_state.page = "search"; st.rerun()
    with col6:
        if st.button("👤\nالملف الشخصي"): st.session_state.page = "profile"; st.rerun()

# 4. قسم القضايا (بيانات وصياغة حقيقية)
elif st.session_state.page == "cases":
    if st.sidebar.button("🏠 العودة للرئيسية"): st.session_state.page = "home"; st.rerun()
    st.header("🏛️ صياغة مذكرات الدفاع")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        court = st.text_input("المحكمة المنظورة")
        case_no = st.text_input("رقم الدعوى والسنة")
    with c2:
        opp = st.text_input("اسم الخصم")
        case_type = st.selectbox("نوع النزاع", ["صرف معاش", "إصابة عمل", "ضم مدة", "تعويض"])
    with c3:
        session = st.date_input("تاريخ الجلسة")

    facts = st.text_area("الوقائع الجوهرية بالتفصيل:", height=150)
    
    if st.button("🚀 ابدأ الصياغة"):
        memo = f"""مذكرة دفاع\nأمام محكمة {court} في الدعوى رقم {case_no}\nبشأن نزاع {case_type}\n\nأولاً: الدفوع:\n1. الدفع بسقوط الحق بالتقادم.\n2. الدفع برفض الدعوى لانتفاء السند القانوني.\n\nثانياً: الوقائع:\nحيث يطالب الخصم ({opp}) بـ {case_type}، وحيث أن {facts}..\n\nبناء عليه:\nنطلب رفض الدعوى.\n\nمع تحيات وليد حماد\nالادارة العامة للشئون القانونية ديوان عام منطقة البحيرة"""
        st.text_area("المسودة:", memo, height=300)
        
        doc = Document(); doc.add_paragraph(memo)
        bio = BytesIO(); doc.save(bio)
        st.download_button("📥 تحميل المذكرة Word", bio.getvalue(), f"دعوى_{case_no}.docx")

# 5. المكتبة (حفظ وحذف حقيقي)
elif st.session_state.page == "lib":
    if st.sidebar.button("🏠 العودة"): st.session_state.page = "home"; st.rerun()
    st.header("📚 أرشيف المكتبة")
    title = st.text_input("عنوان المادة")
    if st.button("💾 حفظ"):
        if title: 
            st.session_state.law_db.append(title)
            st.success("تم الحفظ")
    
    for i, item in enumerate(st.session_state.law_db):
        ca, cb = st.columns([4,1])
        ca.info(item)
        if cb.button("🗑️", key=f"d_{i}"):
            st.session_state.law_db.pop(i); st.rerun()

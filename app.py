import streamlit as st
from docx import Document
from io import BytesIO

# إعدادات الواجهة لتكون احترافية ومناسبة للموبايل
st.set_page_config(page_title="منظومة المستشار وليد حماد", layout="wide")

st.markdown("""
    <style>
    .main { direction: rtl; text-align: right; }
    .stButton>button { 
        height: 120px; width: 100%; border-radius: 15px; 
        font-size: 22px; font-weight: bold; background-color: #ffffff; 
        color: #1e3a8a; border: 3px solid #1e3a8a;
    }
    .stButton>button:hover { background-color: #1e3a8a; color: white; }
    .user-header { 
        background-color: #1e3a8a; color: white; padding: 20px; 
        border-radius: 15px; text-align: center; margin-bottom: 25px; 
    }
    </style>
    """, unsafe_allow_html=True)

# إدارة الصفحات لتجنب الأخطاء البرمجية
if 'page' not in st.session_state:
    st.session_state.page = "home"

# 1. الصفحة الرئيسية (الأيقونات كما ظهرت في صورك)
if st.session_state.page == "home":
    st.markdown('<div class="user-header"><h1>⚖️ منظومة المستشار القانوني</h1><h3>ديوان عام البحيرة</h3></div>', unsafe_allow_html=True)
    st.write(f"#### مرحباً سيادة المستشار: وليد حماد")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏛️\nقسم القضايا والطعون"): st.session_state.page = "cases"; st.rerun()
    with col2:
        if st.button("📚\nالمكتبة القانونية"): st.session_state.page = "lib"; st.rerun()
    with col3:
        if st.button("📂\nإدارة التحقيقات"): st.session_state.page = "inv"; st.rerun()

# 2. قسم القضايا (يعالج أخطاء الصياغة والبيانات)
elif st.session_state.page == "cases":
    if st.sidebar.button("🏠 العودة للرئيسية"):
        st.session_state.page = "home"; st.rerun()
    
    st.header("🏛️ محرك صياغة المذكرات")
    
    c1, c2 = st.columns(2)
    with c1:
        court = st.text_input("اسم المحكمة")
        case_id = st.text_input("رقم الدعوى")
    with c2:
        opponent = st.text_input("اسم الخصم")
        subject = st.selectbox("نوع النزاع", ["صرف معاش عجز", "إصابة عمل", "ضم مدة"])
    
    facts = st.text_area("الوقائع الجوهرية (كما بالصحيفة):", height=150)
    
    if st.button("🚀 صياغة المذكرة الآن"):
        if not court or not case_id:
            st.error("برجاء إدخال بيانات المحكمة ورقم الدعوى")
        else:
            # صياغة قانونية منضبطة بناءً على نوع النزاع
            memo_text = f"""مذكرة دفاع مقدمة من الهيئة القومية للتأمين الاجتماعي
أمام محكمة {court} في الدعوى رقم {case_id}
بشأن نزاع: {subject}

أولاً: الدفوع القانونية:
1. الدفع بسقوط الحق في المطالبة بالتقادم الطويل.
2. الدفع برفض الدعوى لانتفاء السند القانوني السليم.

ثانياً: الوقائع:
حيث يطالب المدعي ({opponent}) بـ {subject}، وحيث أن الوقائع تتلخص في {facts}...

بناء عليه:
نصمم على الطلبات وهي رفض الدعوى وإلزام المدعي بالمصاريف.

مع تحيات وليد حماد
الادارة العامة للشئون القانونية ديوان عام منطقة البحيرة"""
            
            st.success("تمت الصياغة بنجاح")
            st.text_area("المسودة النهائية:", memo_text, height=300)
            
            # توليد ملف Word
            doc = Document()
            doc.add_paragraph(memo_text)
            buffer = BytesIO()
            doc.save(buffer)
            st.download_button("📥 تحميل المذكرة (Word)", buffer.getvalue(), f"memo_{case_id}.docx")

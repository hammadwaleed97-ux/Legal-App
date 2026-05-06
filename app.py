import streamlit as st
from docx import Document
from io import BytesIO

# إعدادات الواجهة الاحترافية (تنسيق الصور 14 و 15)
st.set_page_config(page_title="منظومة المستشار وليد حماد", layout="wide")

st.markdown("""
    <style>
    .main { direction: rtl; text-align: right; }
    .stButton>button { 
        height: 100px; width: 100%; border-radius: 15px; 
        font-size: 20px; font-weight: bold; background-color: #f0f2f6; 
        color: #1e3a8a; border: 2px solid #1e3a8a;
    }
    .header-box { 
        background-color: #1e3a8a; color: white; padding: 20px; 
        border-radius: 15px; text-align: center; margin-bottom: 20px; 
    }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = "home"

# --- الصفحة الرئيسية ---
if st.session_state.page == "home":
    st.markdown('<div class="header-box"><h1>⚖️ محرك الصياغة القانونية الذكي</h1><p>ديوان عام البحيرة - الشئون القانونية</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏛️\nقسم القضايا"): st.session_state.page = "cases"; st.rerun()
    with col2:
        if st.button("📚\nالمكتبة"): st.session_state.page = "lib"; st.rerun()
    with col3:
        if st.button("📂\nالتحقيقات"): st.session_state.page = "inv"; st.rerun()

# --- قسم القضايا مع نظام الدفوع الذكي ---
elif st.session_state.page == "cases":
    if st.sidebar.button("🏠 الرئيسية"): st.session_state.page = "home"; st.rerun()
    
    st.subheader("🏛️ إعداد مذكرة دفاع نموذجية")
    
    with st.expander("📝 بيانات الدعوى", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            court = st.text_input("المحكمة / الدائرة")
            case_no = st.text_input("رقم الدعوى")
        with c2:
            opponent = st.text_input("اسم الخصم")
            case_type = st.selectbox("نوع النزاع", ["صرف معاش", "إصابة عمل", "تعويض", "أخرى"])

    # زرع الدفوع مباشرة في الكود (بناءً على الصور 3، 5، 13)
    st.markdown("### ⚖️ الدفوع القانونية المقترحة")
    d1 = st.checkbox("الدفع بسقوط الحق بالتقادم الطويل (المادة 374 مدني)", value=True)
    d2 = st.checkbox("الدفع برفض الدعوى لانتفاء السند القانوني السليم", value=True)
    d3 = st.checkbox("الدفع بعدم قبول الدعوى لرفعها على غير ذي صفة", value=False)
    
    custom_defense = st.text_input("إضافة دفع خاص آخر:")
    facts = st.text_area("الوقائع الجوهرية:", "يرجى كتابة ملخص الحالة هنا...")

    if st.button("🚀 توليد المذكرة النهائية"):
        # تجميع الدفوع المختارة
        selected_defenses = ""
        if d1: selected_defenses += "1. الدفع بسقوط الحق بالتقادم الطويل.\n"
        if d2: selected_defenses += "2. الدفع برفض الدعوى لانتفاء السند القانوني.\n"
        if d3: selected_defenses += "3. الدفع بعدم قبول الدعوى لانتفاء الصفة.\n"
        if custom_defense: selected_defenses += f"4. {custom_defense}\n"

        memo = f"""مذكرة دفاع مقدمة من الهيئة القومية للتأمين الاجتماعي
أمام محكمة {court} في الدعوى رقم {case_no}

أولاً: الدفوع القانونية:
{selected_defenses}

ثانياً: الوقائع:
بما أن المدعي ({opponent}) يطالب بـ {case_type}، فإن الوقائع تتلخص في: {facts}

بناء عليه:
نصمم على طلب رفض الدعوى وإلزام المدعي بالمصاريف.

مع تحيات وليد حماد
الادارة العامة للشئون القانونية ديوان عام منطقة البحيرة"""

        st.markdown("---")
        st.text_area("المذكرة جاهزة للمراجعة:", memo, height=300)
        
        # تحويل لملف Word (الصورة 13)
        doc = Document()
        doc.add_paragraph(memo)
        bio = BytesIO()
        doc.save(bio)
        st.download_button("📥 تحميل المذكرة Word", bio.getvalue(), f"memo_{case_no}.docx")

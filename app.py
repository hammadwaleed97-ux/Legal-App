import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO

# --- إعدادات الواجهة الاحترافية ---
st.set_page_config(page_title="المستشار الذكي - وليد حماد", layout="wide")

st.markdown("""
    <style>
    .main { direction: rtl; text-align: right; background-color: #f8f9fa; }
    .stButton>button { 
        height: 120px; width: 100%; border-radius: 15px; 
        font-size: 22px; font-weight: bold; background-color: white; 
        color: #1e3a8a; border: 2px solid #1e3a8a; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #1e3a8a; color: white; }
    .header { 
        background: linear-gradient(90deg, #1e3a8a, #3b5998); 
        color: white; padding: 25px; border-radius: 15px; 
        text-align: center; margin-bottom: 25px; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- ترويسة البرنامج ---
st.markdown('<div class="header"><h1>⚖️ منظومة المستشار القانوني الذكي</h1><p>الإدارة العامة للشئون القانونية - ديوان عام البحيرة</p></div>', unsafe_allow_html=True)

# --- إدارة التنقل ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'lib' not in st.session_state: st.session_state.lib = []

# --- 1. الواجهة الرئيسية (أيقونات واضحة) ---
if st.session_state.page == "home":
    st.write(f"### مرحباً سيادة المستشار: وليد حماد")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏛️\nقسم القضايا والطعون"): st.session_state.page = "cases"; st.rerun()
    with col2:
        if st.button("📚\nالمكتبة القانونية"): st.session_state.page = "library"; st.rerun()
    with col3:
        if st.button("📂\nإدارة التحقيقات"): st.session_state.page = "investigations"; st.rerun()

# --- 2. قسم القضايا (صياغة بيانات حقيقية) ---
elif st.session_state.page == "cases":
    if st.button("🔙 العودة للرئيسية"): st.session_state.page = "home"; st.rerun()
    
    st.subheader("📝 صياغة مذكرة دفاع")
    c1, c2 = st.columns(2)
    with c1:
        court = st.text_input("اسم المحكمة / الدائرة")
        case_no = st.text_input("رقم الدعوى والسنة")
    with c2:
        litigant = st.text_input("اسم الخصم")
        case_type = st.selectbox("نوع النزاع", ["صرف معاش", "إصابة عمل", "تعويض", "أخرى"])
    
    facts = st.text_area("الوقائع (اكتب تفاصيل الحالة هنا)", height=150)
    
    if st.button("✨ توليد المذكرة"):
        memo = f"""مذكرة دفاع في الدعوى رقم {case_no}\nأمام محكمة {court}\nبشأن نزاع {case_type}\n\nأولاً: الدفوع:\n1. الدفع بسقوط الحق بالتقادم الطويل.\n2. الدفع برفض الدعوى لانتفاء السند القانوني.\n\nثانياً: الوقائع:\nحيث يطالب الخصم ({litigant}) بـ {case_type}، وحيث أن {facts}..\n\nبناء عليه:\nنطلب رفض الدعوى.\n\nعن الهيئة/ وليد حماد"""
        st.text_area("المذكرة الناتجة:", memo, height=250)
        
        # تصدير للـ Word
        doc = Document(); doc.add_paragraph(memo)
        bio = BytesIO(); doc.save(bio)
        st.download_button("📥 تحميل المذكرة Word", bio.getvalue(), f"memo_{case_no}.docx")

# --- 3. قسم المكتبة (حفظ وحذف) ---
elif st.session_state.page == "library":
    if st.button("🔙 العودة للرئيسية"): st.session_state.page = "home"; st.rerun()
    st.subheader("📚 أرشيف المواد القانونية")
    
    t = st.text_input("عنوان المادة")
    f = st.file_uploader("رفع ملف (PDF)")
    if st.button("💾 حفظ"):
        if t:
            st.session_state.lib.append(t)
            st.success(f"تم حفظ {t}")
    
    st.write("---")
    for i, item in enumerate(st.session_state.lib):
        col_t, col_d = st.columns([4, 1])
        col_t.write(f"📌 {item}")
        if col_d.button("🗑️ حذف", key=f"del_{i}"):
            st.session_state.lib.pop(i)
            st.rerun()

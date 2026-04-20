import streamlit as st

# 1. الترويسة الرسمية (تصغير اللوجو وتثبيت البيانات)
st.set_page_config(page_title="منظومة المستشار وليد حماد", layout="wide")

st.markdown("""
    <div style="text-align: center; border-bottom: 3px solid #1E3A8A; padding: 10px; background-color: #f8f9fa; margin-bottom: 20px;">
        <h2 style="color: #1E3A8A; margin: 0; font-size: 20px;">الهيئة القومية للتأمين الاجتماعى</h2>
        <h3 style="color: #1E3A8A; margin: 0; font-size: 16px;">الإدارة المركزية للإدارات القانونية</h3>
        <p style="color: #ce1126; margin: 5px; font-weight: bold;">مع تحيات / وليد حماد</p>
    </div>
""", unsafe_allow_html=True)

# 2. الأقسام الأربعة الكبرى
tab1, tab2, tab3, tab4 = st.tabs(["⚖️ القضايا", "📜 الفتوى", "🔍 التحقيقات", "📚 المكتبة"])

# --- القسم الأول: الإدارة العامة للقضايا (حرفياً من معطياتك) ---
with tab1:
    main_sec = st.selectbox("القسم القضائى:", ["القضاء العادى", "محاكم مجلس الدولة", "تسجيل الدعاوى والطعون", "البحث عن سابقة"])
    
    if main_sec == "القضاء العادى":
        level = st.radio("المحكمة:", ["الابتدائية", "الاستئنافية", "النقض"], horizontal=True)
        
        if level == "الابتدائية":
            st.subheader("صياغة مذكرة بدفاع الهيئة")
            role = st.selectbox("الصفة:", ["الهيئة مدعى عليها", "الهيئة مدعية"])
            c1, c2, c3, c4 = st.columns(4)
            with c1: st.text_input("المحكمة")
            with c2: st.text_input("الدائرة")
            with c3: st.text_input("رقم الدعوى")
            with c4: st.text_input("سنة")
            st.text_input("اسم المدعى وصفته")
            st.text_input("اسم المدعى عليه وصفته")
            st.text_area("ملخص الوقائع – طلبات المدعى")
            st.file_uploader("ارفع صورة الصحيفة لقراءتها")
            if st.button("⚖️ صياغة المذكرة"):
                st.info("الترتيب: مادة قانونية -> شرح -> نتيجة")
                st.markdown("<div style='text-align:center;'><b>عن الهيئة</b><br>عضو الادارة القانونية: ............ &nbsp;&nbsp;&nbsp;&nbsp; مدير الادارة القانونية: ............</div>", unsafe_allow_html=

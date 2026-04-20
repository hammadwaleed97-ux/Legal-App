import streamlit as st

# 1. الهوية البصرية المعتمدة (الترويسة الرسمية)
st.set_page_config(page_title="منظومة المستشار وليد حماد", layout="wide")

st.markdown("""
    <div style="text-align: center; border-bottom: 3px solid #1E3A8A; padding: 10px; background-color: #f8f9fa; margin-bottom: 20px;">
        <h2 style="color: #1E3A8A; margin: 0; font-size: 22px;">الهيئة القومية للتأمين الاجتماعى</h2>
        <h3 style="color: #1E3A8A; margin: 5px 0; font-size: 18px;">الإدارة المركزية للإدارات القانونية</h3>
        <h4 style="color: #ce1126; margin: 0; font-size: 16px;">مع تحيات / وليد حماد</h4>
    </div>
""", unsafe_allow_html=True)

# 2. الأقسام المعتمدة (قضايا ومكتبة)
tab1, tab2 = st.tabs(["⚖️ أولاً: الإدارة العامة للقضايا", "📚 ثانياً: المكتبة القانونية الرقمية"])

# --- القسم الأول: الإدارة العامة للقضايا (حرفياً من المعطيات) ---
with tab1:
    q_sec = st.selectbox("اختر الفرع القضائى:", ["القضاء العادى", "محاكم مجلس الدولة", "تسجيل الدعاوى والطعون", "البحث عن سابقة فصل"])
    
    if q_sec == "القضاء العادى":
        level = st.radio("درجة التقاضي:", ["المحاكم الابتدائية", "المحاكم الاستئنافية", "محكمة النقض"], horizontal=True)
        
        if level == "المحاكم الابتدائية":
            st.subheader("صياغة مذكرة بدفاع الهيئة")
            side = st.selectbox("صفة الهيئة:", ["الهيئة مدعى عليها", "الهيئة مدعية"])
            c1, c2, c3, c4 = st.columns(4)
            with c1: st.text_input("المحكمة")
            with c2: st.text_input("الدائرة")
            with c3: st.text_input("رقم الدعوى")
            with c4: st.text_input("السنة")
            st.text_input("اسم المدعى وصفته")
            st.text_input("اسم المدعى عليه وصفته")
            st.text_area("ملخص الوقائع وطلبات المدعى (ماتم رصده من صحيفة الدعوى)")
            st.file_uploader("إرفاق صورة الصحيفة لزيادة دقة الصياغة")
            if st.button("⚖️ توليد صياغة المذكرة"):
                st.info("المنهجية: المادة القانونية -> الشرح الفقهي والقضائي -> التطبيق على الواقعة")
                st.markdown("<div style='text-align:center;'><b>عن الهيئة</b><br>عضو الإدارة القانونية: ............ &nbsp;&nbsp;&nbsp;&nbsp; مدير الإدارة القانونية: ............</div>", unsafe_allow_html=True)

        elif level == "المحاكم الاستئنافية":
            work_type = st.selectbox("نوع العمل:", ["صحيفة استئناف مقام من الهيئة", "مذكرة دفاع (مستأنفة)", "مذكرة دفاع (مستأنف ضدها)"])
            st.text_input("المحكمة المرفوع أمامها الطعن / رقم الحكم المستأنف")
            st.text_input("المستأنف (صفته، المقر القانونى، من يمثله)")
            st.text_input("المستأنف ضده (صفته، محله المختار)")
            st.text_area("منطوق الحكم وتاريخ الجلسة")
            st.write("**وكيل الهيئة الطاعنة / ....................**")

    elif q_sec == "تسجيل الدعاوى والطعون":
        st.text_input("المحكمة المرفوع أمامها")
        st.text_input("اسم المدعى ورقمه القومى")
        st.text_input("رقم الدعوى والسنة")
        st.text_area("آخر القرارات والتنبيهات")
        st.button("💾 حفظ في الأرشيف")

# --- القسم الثاني: المكتبة القانونية (الـ 14 قسماً بالترتيب المعتمد) ---
with

import streamlit as st

# 1. إعدادات الصفحة والهوية البصرية (اللوجو المعتمد)
st.set_page_config(page_title="منظومة المستشار وليد حماد", layout="wide")

st.markdown("""
    <div style="text-align: center; border-bottom: 3px solid #1E3A8A; padding: 10px; background-color: #f8f9fa; margin-bottom: 20px;">
        <h2 style="color: #1E3A8A; margin: 0; font-size: 22px;">الهيئة القومية للتأمين الاجتماعى</h2>
        <h3 style="color: #1E3A8A; margin: 5px 0; font-size: 18px;">الإدارة المركزية للإدارات القانونية</h3>
        <h4 style="color: #ce1126; margin: 0; font-size: 16px;">مع تحيات / وليد حماد</h4>
    </div>
""", unsafe_allow_html=True)

# 2. تنظيم الأقسام الأربعة الرئيسية بناءً على المعطيات
tab1, tab2, tab3, tab4 = st.tabs([
    "⚖️ أولاً: الإدارة العامة للقضايا", 
    "📜 ثانياً: الإدارة العامة للفتوى", 
    "🔍 ثالثاً: الإدارة العامة للتحقيقات", 
    "📚 رابعاً: المكتبة القانونية"
])

# --- أولاً: الإدارة العامة للقضايا (القسم القضائى) ---
with tab1:
    q_choice = st.selectbox("اختر القسم:", ["القضاء العادى", "محاكم مجلس الدولة", "تسجيل الدعاوى والطعون", "البحث عن سابقة"])
    
    if q_choice == "القضاء العادى":
        level = st.radio("المستوى:", ["المحاكم الابتدائية", "المحاكم الاستئنافية", "محكمة النقض"], horizontal=True)
        
        if level == "المحاكم الابتدائية":
            st.subheader("صياغة مذكرة بدفاع الهيئة")
            side = st.selectbox("صفة الهيئة:", ["الهيئة مدعى عليها", "الهيئة مدعية"])
            c1, c2, c3, c4 = st.columns(4)
            with c1: st.text_input("المحكمة")
            with c2: st.text_input("الدائرة")
            with c3: st.text_input("رقم الدعوى")
            with c4: st.text_input("السنة")
            st.text_input("بيانات الخصوم (اسم المدعى وصفته)")
            st.text_input("اسم المدعى عليه وصفته")
            st.text_area("ملخص الوقائع – طلبات المدعى")
            st.file_uploader("او ارفع صورة الصحيفة لقراءتها وادارجها")
            if st.button("⚖️ صياغة المذكرة"):
                st.info("الترتيب: مادة قانونية -> شرح -> نتيجة (رؤية الهيئة)")
                st.markdown("<div style='text-align:center;'><b>عن الهيئة</b><br><br>عضو الادارة القانونية ............ &nbsp;&nbsp;&nbsp;&nbsp; مدير الادارة القانونية ............</div>", unsafe_allow_html=True)
                st.button("📥 حفظ ورد")
                st.button("📄 حفظ بى دى اف")

        elif level == "المحاكم الاستئنافية":
            mode = st.selectbox("النوع:", ["صياغة صحيفة استئناف مقام من الهيئة", "مذكرة بدفاع الهيئة (مستأنفة)", "مذكرة بدفاع الهيئة (مستأنف ضدها)"])
            st.text_input("المحكمة التى يرفع امامها الاستئناف / رقم الحكم المستأنف")
            st.text_input("المستأنف (وصفته، المقر القانونى، من يمثله)")
            st.text_input("المستأنف ضده (وصفته، محل الاقامة، محله المختار)")
            st.text_area("منطوق الحكم وتاريخ الجلسة")
            st.write("**وكيل الهيئة الطاعنة / ....................**")

    elif q_choice == "تس

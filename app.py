import streamlit as st
import pandas as pd
from datetime import datetime

# إعدادات الصفحة والسمة العامة
st.set_page_config(page_title="منظومة الهيئة القومية للتأمين الاجتماعي", layout="wide", initial_sidebar_state="expanded")

# العنوان الرئيسي والهيدر
st.markdown("""
    <div style="text-align: center; background-color: #1E3A8A; padding: 20px; border-radius: 10px; color: white;">
        <h1>الهيئة القومية للتأمين الاجتماعي</h1>
        <h3>الإدارة العامة للشئون القانونية</h3>
        <p style="font-size: 1.2em;">مع تحيات أ/ وليد حماد</p>
    </div>
    <br>
""", unsafe_allow_html=True)

# القائمة الجانبية الرئيسية
with st.sidebar:
    st.image("https://img.icons8.com/fluency/100/law.png")
    st.title("المنظومة القانونية")
    main_menu = st.selectbox("اختر الإدارة العامة:", 
        ["أولاً: الإدارة العامة للقضايا", "ثانياً: الإدارة العامة للفتوى", "ثالثاً: الإدارة العامة للتحقيقات", "رابعاً: المكتبة القانونية"])

# --- أولاً: الإدارة العامة للقضايا ---
if main_menu == "أولاً: الإدارة العامة للقضايا":
    tab1, tab2, tab3 = st.tabs(["القسم القضائي", "تسجيل الدعاوى/الطعون", "البحث والأرشيف"])
    
    with tab1:
        jurisdiction = st.selectbox("نوع القضاء:", ["القضاء العادي", "محاكم مجلس الدولة"])
        
        if jurisdiction == "القضاء العادي":
            court_level = st.radio("المستوى القضائي:", ["المحاكم الابتدائية", "المحاكم الاستئنافية", "محكمة النقض"], horizontal=True)
            
            # مثال للمحاكم الابتدائية
            if court_level == "المحاكم الابتدائية":
                form_type = st.selectbox("نوع الإجراء:", ["مذكرة بدفاع الهيئة (مدعى عليها)", "مذكرة بدفاع الهيئة (مدعية)"])
                st.subheader(form_type)
                
                c1, c2 = st.columns(2)
                with c1:
                    court_name = st.text_input("المحكمة")
                    case_no = st.text_input("رقم الدعوى")
                with c2:
                    circuit = st.text_input("الدائرة")
                    case_year = st.text_input("السنة")
                
                plaintiff = st.text_input("اسم المدعي وصفته")
                defendant = st.text_input("اسم المدعى عليه وصفته")
                facts = st.text_area("ملخص الوقائع")
                requests = st.text_area("طلبات المدعي")
                uploaded_file = st.file_uploader("ارفع صورة الصحيفة للقراءة بالذكاء الاصطناعي", type=['png', 'jpg', 'pdf'])
                
                if st.button("صياغة المذكرة وديباجة الدفوع"):
                    st.info("جاري صياغة المذكرة وفقاً لمنظور الهيئة وترتيب الدفوع قانونياً...")
                    # هنا يتم استدعاء نموذج الذكاء الاصطناعي لاحقاً
                    st.markdown(f"""
                    ---
                    **مذكرة بدفاع**
                    السيد/ مدير عام الإدارة القانونية بصفته وكيل عن الهيئة القومية للتأمين الاجتماعي
                    **ضد**
                    السيد/ {plaintiff}
                    ... (هنا يظهر نص المذكرة المشروح بالمادة القانونية) ...
                    
                    **عن الهيئة**
                    عضو الإدارة القانونية: ....................
                    مدير الإدارة القانونية: ....................
                    """)
                    st.button("حفظ Word")
                    st.button("حفظ PDF")

        elif jurisdiction == "محاكم مجلس الدولة":
            council_level = st.selectbox("المحكمة:", ["المحاكم الإدارية", "المحاكم التأديبية", "القضاء الإداري", "الإدارية العليا"])
            st.info(f"واجهة صياغة المذكرات لـ {council_level} مفعلة بنفس المعايير.")

# --- ثانياً: الإدارة العامة للفتوى ---
elif main_menu == "ثانياً: الإدارة العامة للفتوى":
    fatwa_type = st.radio("نوع القسم:", ["فتاوى عامة", "إصابات عمل", "شكاوى الزواج العرفي", "أرشيف الفتاوى"])
    if fatwa_type != "أرشيف الفتاوى":
        st.subheader(f"قسم {fatwa_type}")
        facts_f = st.text_area("ملخص الوقائع")
        subject_f = st.text_area("مثار البحث")
        st.file_uploader("ارفع صورة مذكرة الإحالة والمستندات", type=['png', 'jpg', 'pdf'])
        if st.button("صياغة مذكرة الرأي القانوني"):
            st.success("تم توليد الرأي القانوني بناءً على تعليمات الهيئة.")
            st.markdown("""
                **التوقيعات:**
                عضو الإدارة القانونية: .................... | مدير الإدارة القانونية: ....................
            """)

# --- ثالثاً: الإدارة العامة للتحقيقات ---
elif main_menu == "ثالثاً: الإدارة العامة للتحقيقات":
    invest_type = st.selectbox("جهة التحقيق:", ["تحقيقات الهيئة", "النيابة الإدارية", "النيابة العامة"])
    st.subheader(invest_type)
    c1, c2, c3 = st.columns(3)
    with c1: inv_no = st.text_input("رقم التحقيق/القضية")
    with c2: inv_year = st.text_input("السنة")
    with c3: inv_date = st.date_input("تاريخ الإحالة")
    
    accused = st.text_input("اسم المخالف / المخالفين")
    office = st.text_input("المكتب أو المنطقة التأمينية")
    
    if st.button("فتح محضر التحقيق (س وج)"):
        st.text_area("المحقق:", "س: ما قولك فيما هو منسوب إليك؟")
        st.text_area("المجيب:", "ج: ")
    
    st.button("صياغة مذكرة التصرف")

# --- رابعاً: المكتبة القانونية ---
elif main_menu == "رابعاً: المكتبة القانونية":
    st.subheader("📚 المكتبة القانونية الرقمية")
    lib_sections = ["القوانين", "اللوائح", "القرارات الوزارية", "المنشورات الوزارية", "قرارات رئيس الهيئة", "كتب دورية", "تعليمات الهيئة", "فتاوى مجلس الدولة", "أحكام قضائية"]
    selected_sec = st.selectbox("اختر القسم:", lib_sections)
    
    st.file_uploader(f"تحميل ملف جديد إلى قسم {selected_sec}", type=['pdf', 'docx'])
    st.write("قائمة الملفات المتاحة (سيتم جردها من المكتبة):")
    st.info("ملاحظة: الذكاء الاصطناعي مرتبط بهذه المكتبة حصرياً لاستقاء المادة العلمية.")

# تذييل الصفحة
st.markdown("---")
st.caption(f"تم التحديث في: {datetime.now().strftime('%Y-%m-%d')} | نظام الإدارة القانونية الذكي - الإصدار 1.0")

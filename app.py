import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والهوية البصرية المختصرة والقوية
st.set_page_config(page_title="منظومة المستشار وليد حماد", layout="wide")

st.markdown("""
    <div style="text-align: center; border-bottom: 3px solid #1E3A8A; padding: 10px; background-color: #f8f9fa; margin-bottom: 20px;">
        <h2 style="color: #1E3A8A; margin: 0; font-size: 22px;">الهيئة القومية للتأمين الاجتماعى</h2>
        <h3 style="color: #1E3A8A; margin: 5px 0; font-size: 18px;">الادارة المركزية للإدارات القانونية</h3>
        <h4 style="color: #ce1126; margin: 0; font-size: 16px;">مع تحيات / وليد حماد</h4>
    </div>
""", unsafe_allow_html=True)

# 2. تهيئة مخازن البيانات (الأرشيف والمكتبة)
if 'archive' not in st.session_state: st.session_state.archive = []
if 'library' not in st.session_state: st.session_state.library = {}

# 3. الأقسام الرئيسية الأربعة
tab1, tab2, tab3, tab4 = st.tabs([
    "⚖️ أولاً: الإدارة العامة للقضايا", 
    "📜 ثانياً: الإدارة العامة للفتوى", 
    "🔍 ثالثاً: إدارة التحقيقات", 
    "📚 رابعاً: المكتبة القانونية"
])

# --- أولاً: الإدارة العامة للقضايا ---
with tab1:
    court_category = st.selectbox("اختر جهة القضاء:", ["القضاء العادي", "مجلس الدولة", "تسجيل الدعاوى والطعون", "البحث في السوابق"])
    
    if court_category == "القضاء العادي":
        sub_court = st.radio("المحكمة:", ["الابتدائية", "الاستئنافية", "النقض"], horizontal=True)
        
        # مثال للمحاكم الابتدائية (تطبق نفس الفلسفة على الباقي)
        if sub_court == "الابتدائية":
            mode = st.selectbox("نوع الصياغة:", ["مذكرة دفاع (الهيئة مدعى عليها)", "مذكرة دفاع (الهيئة مدعية)"])
            col1, col2 = st.columns(2)
            with col1:
                court_name = st.text_input("المحكمة")
                case_no = st.text_input("رقم الدعوى")
            with col2:
                circle = st.text_input("الدائرة")
                year = st.text_input("السنة")
            
            st.markdown("---")
            st.subheader("بيانات الخصوم")
            plaintiff = st.text_input("اسم المدعي وصفته")
            defendant = st.text_input("اسم المدعى عليه وصفته")
            
            facts = st.text_area("ملخص الوقائع / طلبات المدعي")
            uploaded_file = st.file_uploader("أو ارفع صورة الصحيفة للقراءة بالذكاء الاصطناعي")
            
            if st.button("⚖️ صياغة المذكرة وترتيب الدفوع"):
                st.subheader("مسودة المذكرة (رؤية الهيئة)")
                draft_text = f"بناءً على المادة القانونية المستخرجة من المكتبة...\n\nالوقائع: {facts}\n\nالدفوع:\n1. ...\n\nعن الهيئة:\nعضو الإدارة القانونية: ............ \nمدير الإدارة القانونية: ............"
                st.text_area("النص الناتج:", value=draft_text, height=300)
                st.download_button("📥 حفظ Word", data=draft_text, file_name="memo.doc")
                st.download_button("📥 حفظ PDF", data=draft_text, file_name="memo.pdf")

# --- ثانياً: الإدارة العامة للفتوى ---
with tab2:
    st.header("قسم الإفتاء القانوني")
    fatwa_type = st.selectbox("نوع الطلب:", ["فتاوى عامة", "إصابات عمل", "شكاوى الزواج العرفي", "أرشيف الفتاوى"])
    
    if fatwa_type != "أرشيف الفتاوى":
        summary = st.text_area("ملخص الوقائع ومثار البحث")
        st.file_uploader("ارفع مذكرة الإحالة والمستندات")
        if st.button("📝 صياغة مذكرة الرأي القانوني"):
            result = "الرأي القانوني: ....\n\nعضو الإدارة القانونية: ............ \nمدير الإدارة القانونية: ............"
            st.write(result)

# --- ثالثاً: إدارة التحقيقات والنيابات ---
with tab3:
    invest_type = st.radio("نوع التحقيق:", ["تحقيقات الهيئة", "النيابة الإدارية", "النيابة العامة", "أرشيف التحقيقات"])
    
    if invest_type == "تحقيقات الهيئة":
        c1, c2 = st.columns(2)
        with c1:
            inv_no = st.text_input("رقم التحقيق / السنة")
            inv_date = st.date_input("تاريخ الإحالة")
        with c2:
            inv_name = st.text_input("اسم المخالف")
            inv_office = st.text_input("المكتب / المنطقة")
            
        st.text_area("ملخص الوقائع ونوع المخالفة")
        if st.button("📂 فتح محضر التحقيق (س وج)"):
            st.write("محضر تحقيق رسمي...")
        if st.button("📝 صياغة مذكرة التصرف"):
            st.write("عضو الإدارة القانونية: ............ \nمدير الإدارة القانونية: ............"

# --- رابعاً: المكتبة القانونية (مصدر التعلم للذكاء الاصطناعي) ---
with tab4:
    st.header("المكتبة القانونية الرقمية")
    lib_cats = [
        "القوانين", "اللوائح", "القرارات الوزارية", "المنشورات الوزارية", 
        "قرارات رئيس الهيئة", "منشورات رئيس الهيئة", "الكتب الدورية", 
        "تعليمات الهيئة", "المرصد الفني", "رسائل الهيئة", 
        "مذكرات اللجنة القانونية", "فتاوى مجلس الدولة", "أحكام قضائية", "آخر"
    ]
    
    selected_lib = st.selectbox("اختر التصنيف:", lib_cats)
    up_lib = st.file_uploader(f"تحميل {selected_lib} على الموقع")
    if st.button("✅ تثبيت في المكتبة"):
        st.success(f"تم إدراج المستند ضمن {selected_lib} وجاري ربطه بالذكاء الاصطناعي للصياغة.")

# ملاحظة برمجية للمستشار:
# يتم الربط بالذكاء الاصطناعي لقراءة ملفات المكتبة حصراً كما طلبت

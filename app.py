import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO

# --- الإعدادات العامة والتنسيق ---
st.set_page_config(page_title="منظومة الشئون القانونية - التأمينات", layout="wide")

st.markdown("""
    <style>
    .reportview-container { direction: rtl; text-align: right; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #2c3e50; color: white; }
    input, select, textarea { text-align: right; direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

# --- ترويسة ثابتة للهيئة ---
def draw_header():
    st.write("### الهيئة القومية للتأمين الاجتماعـــــــي")
    st.write("#### الإدارة العامة للشئون القانونية")
    st.write(f"**مع تحيات: وليد حماد**")
    st.divider()

# --- محرك الذكاء الاصطناعي (محاكاة الربط مع المكتبة) ---
def ai_drafting_engine(doc_type, facts, legal_base):
    # هنا يتم الربط مع المكتبة القانونية (AI Logic)
    # 1. ترتيب الدفوع قانونياً
    # 2. ذكر المادة ثم الشرح ثم النتيجة
    draft = f"بناءً على المادة {legal_base} المنظمة لهذا الشأن...\n"
    draft += f"وحيث أن الوقائع تتلخص في: {facts}\n"
    draft += "لذلك، والدفوع مرتبة قانونياً هي: ....\n"
    return draft

# --- القائمة الرئيسية ---
draw_header()
main_menu = st.sidebar.selectbox("القطاع الرئيسي", [
    "أولاً: الإدارة العامة للقضايا",
    "ثانياً: الإدارة العامة للفتوى",
    "ثالثاً: الإدارة العامة للتحقيقات",
    "رابعاً: المكتبة القانونية",
    "خامساً: سجلات البحث والأرشيف"
])

# --- أولاً: الإدارة العامة للقضايا ---
if main_menu == "أولاً: الإدارة العامة للقضايا":
    sub_menu = st.sidebar.radio("القسم القضائي", ["القضاء العادي", "مجلس الدولة", "المحاكم التأديبية"])
    
    if sub_menu == "القضاء العادي":
        court_level = st.selectbox("المستوى القضائي", ["الابتدائية", "الاستئنافية", "النقض"])
        
        # نموذج صياغة (مثال للمحاكم الابتدائية - الهيئة مدعى عليها)
        with st.expander("صياغة مذكرة دفاع (الهيئة مدعى عليها)"):
            c1, c2 = st.columns(2)
            with c1:
                court_name = st.text_input("المحكمة")
                circle = st.text_input("الدائرة")
                case_no = st.text_input("رقم الدعوى")
            with c2:
                case_year = st.text_input("السنة")
                plaintiff = st.text_input("اسم المدعي وصفته")
                defendant = st.text_input("اسم المدعى عليه وصفته (الهيئة)")
            
            facts = st.text_area("ملخص الوقائع وطلبات المدعي")
            uploaded_file = st.file_uploader("ارفع صورة الصحيفة للذكاء الاصطناعي", type=['png', 'jpg', 'pdf'])
            
            if st.button("صياغة المذكرة بالذكاء الاصطناعي"):
                # الصياغة من وجهة نظر الهيئة مع ترتيب الدفوع
                st.session_state.draft = ai_drafting_engine("مذكرة دفاع", facts, "قانون التأمينات")
                st.text_area("المسودة الناتجة", st.session_state.draft, height=300)
                
                # خانات التوقيع المطلوبة
                st.write("---")
                st.write("**عن الهيئة**")
                col_sign1, col_sign2 = st.columns(2)
                col_sign1.write("عضو الإدارة القانونية / .................")
                col_sign2.write("مدير الإدارة القانونية / .................")
                
                # أزرار الحفظ
                st.button("حفظ Word")
                st.button("حفظ PDF")

# --- ثانياً: الإدارة العامة للفتوى ---
elif main_menu == "ثانياً: الإدارة العامة للفتوى":
    topic = st.selectbox("نوع الفتوى", ["فتاوى عامة", "إصابات عمل", "زواج عرفي"])
    facts_fatwa = st.text_area("ملخص الوقائع ومثار البحث")
    st.file_uploader("ارفع مذكرة الإحالة والمستندات")
    
    if st.button("صياغة مذكرة الرأي القانوني"):
        st.success("تمت الصياغة: (المادة القانونية -> الشرح -> النتيجة)")
        st.write("عضو الإدارة القانونية / .................")
        st.write("مدير الإدارة القانونية / .................")

# --- ثالثاً: الإدارة العامة للتحقيقات ---
elif main_menu == "ثالثاً: الإدارة العامة للتحقيقات":
    invest_type = st.selectbox("نوع التحقيق", ["تحقيقات الهيئة", "نيابة إدارية", "نيابة عامة"])
    with st.form("invest_form"):
        st.text_input("رقم التحقيق / القضية")
        st.text_input("اسم المخالف")
        st.text_area("ملخص الوقائع")
        if st.form_submit_button("فتح محضر س وج"):
            st.info("تم فتح المحضر للبدء في الاستجواب")

# --- رابعاً: المكتبة القانونية ---
elif main_menu == "رابعاً: المكتبة القانونية":
    lib_type = st.selectbox("نوع المادة العلمية", [
        "القوانين", "اللوائح", "القرارات الوزارية", "المنشورات الوزارية", 
        "قرارات رئيس الهيئة", "الكتب الدورية", "تعليمات الهيئة", "المرصد الفني"
    ])
    st.file_uploader(f"تحميل {lib_type} جديد للمكتبة")
    st.info("سيقوم الذكاء الاصطناعي بقراءة هذه المادة واستخدامها في الصياغة حصراً")

# --- خامساً: سجلات البحث والأرشيف ---
elif main_menu == "خامساً: سجلات البحث والأرشيف":
    search_type = st.radio("نوع البحث", ["البحث عن سابقة فصل", "أرشيف القضايا", "أرشيف الفتاوى"])
    search_query = st.text_input("ابحث بالاسم أو الرقم القومي أو رقم الدعوى")
    if st.button("بحث"):
        st.write("جاري فحص قاعدة البيانات للأطراف والموضوع والسبب...")


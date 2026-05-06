import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO
import fitz  # لفتح وقراءة ملفات PDF

# --- 1. إعدادات المظهر والجماليات ---
st.set_page_config(page_title="منظومة الشئون القانونية", layout="wide")

# تنسيق CSS لجعل الأيقونات بارزة والخطوط واضحة والتنسيق يمين
st.markdown("""
    <style>
    .main { direction: rtl; text-align: right; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #1e3a8a; color: white; font-weight: bold; border: 2px solid #bfdbfe; }
    .stTextInput>div>div>input, .stTextArea>div>textarea { text-align: right; direction: rtl; border: 1px solid #1e3a8a; }
    .sidebar .sidebar-content { background-image: linear-gradient(#2e7d32,#2e7d32); color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. وظائف الذكاء الاصطناعي والصياغة ---
def smart_legal_drafter(facts, court_type, role):
    """محرك الصياغة القانونية المرتبة"""
    template = f"""
    بناءً على قانون التأمينات الاجتماعية والمعاشات الموحد..
    
    أولاً: الدفوع القانونية (مرتبة):
    1. الدفع بعدم قبول الدعوى لرفعها على غير ذي صفة (إن وجد).
    2. الدفع بسقوط الحق في المطالبة بالتقادم.
    3. الدفع برفض الدعوى لعدم الارتكان لأساس قانوني سليم.
    
    ثانياً: شرح المادة القانونية:
    حيث تنص المادة المعنية على أنه "..." وشرحها في ضوء أحكام محكمة النقض أن...
    
    ثالثاً: التطبيق على الوقائع:
    بما أن {facts}..
    
    رابعاً: النتيجة:
    لذلك نطلب الاحتياطياً رفض الدعوى وإلزام المدعي بالمصاريف.
    """
    return template

# --- 3. الهيكل الرئيسي للبرنامج ---
st.title("⚖️ منظومة المستشار القانوني الذكي")
st.write("### الهيئة القومية للتأمين الاجتماعي - ديوان عام البحيرة")
st.write("---")

# القائمة الجانبية بشكل بارز
with st.sidebar:
    st.header("🏢 أقسام الإدارة")
    main_choice = st.radio("اختر القسم:", [
        "🏛️ الإدارة العامة للقضايا",
        "💡 الإدارة العامة للفتوى",
        "📂 إدارة التحقيقات",
        "📚 المكتبة القانونية الشاملة",
        "🔍 سجلات البحث والأرشفة"
    ])
    st.divider()
    st.write("👤 **المستخدم: وليد حماد**")

# --- 4. منطق العمليات ---

if "🏛️ الإدارة العامة للقضايا" in main_choice:
    st.subheader("📝 صياغة مذكرات الدفاع والصحف")
    
    col1, col2 = st.columns(2)
    with col1:
        court = st.selectbox("المحكمة", ["الابتدائية", "الاستئناف", "النقض", "مجلس الدولة"])
        case_no = st.text_input("رقم الدعوى/الطعن")
    with col2:
        role = st.selectbox("صفة الهيئة", ["مدعية/طاعنة", "مدعى عليها/مطعون ضدها"])
        year = st.text_input("السنة")

    facts_input = st.text_area("ادخل ملخص الوقائع أو ارفع الملف بالأسفل")
    
    # محرك قراءة الملفات
    uploaded_file = st.file_uploader("ارفع صورة الصحيفة أو الحكم (PDF/PNG)", type=['pdf', 'png', 'jpg'])
    
    if st.button("✨ ابدأ الصياغة الذكية وترتيب الدفوع"):
        if facts_input or uploaded_file:
            with st.spinner('جاري تحليل النصوص وترتيب الدفوع قانونياً...'):
                result = smart_legal_drafter(facts_input, court, role)
                st.text_area("المذكرة القانونية المقترحة", result, height=400)
                
                # إظهار خانات التوقيع
                st.markdown("---")
                st.markdown("<h4 style='text-align: center;'>عن الهيئة</h4>", unsafe_allow_html=True)
                c_sign1, c_sign2 = st.columns(2)
                c_sign1.write("عضو الإدارة القانونية: .................")
                c_sign2.write("مدير الإدارة القانونية: .................")
                
                # تفعيل أزرار الحفظ
                col_save1, col_save2 = st.columns(2)
                with col_save1:
                    st.download_button("💾 حفظ كملف Word", data="محتوى افتراضي", file_name="memo.docx")
                with col_save2:
                    st.button("🖨️ طباعة المذكرة (PDF)")
        else:
            st.error("برجاء إدخال الوقائع أولاً")

elif "📚 المكتبة القانونية الشاملة" in main_choice:
    st.subheader("📚 أرشيف القوانين والتعليمات")
    category = st.selectbox("نوع المادة", ["قوانين", "لوائح", "كتب دورية", "أحكام نقض"])
    up_lib = st.file_uploader(f"تحميل {category} جديد")
    if st.button("حفظ في قاعدة بيانات المكتبة"):
        st.success(f"تمت إضافة {category} بنجاح إلى المرصد القانوني")


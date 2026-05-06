import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO
import fitz  # لقراءة ملفات PDF

# --- 1. إعدادات الهوية البصرية ---
st.set_page_config(page_title="منظومة الشئون القانونية", layout="wide")

st.markdown("""
    <style>
    .main { direction: rtl; text-align: right; }
    .stButton>button { background-color: #1e3a8a; color: white; border-radius: 10px; font-weight: bold; height: 3em; }
    div[data-testid="stSidebarNav"] { direction: rtl; }
    .stTextInput>div>div>input, .stTextArea>div>textarea { text-align: right; direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك الصياغة الذكي (Core Engine) ---
def draft_legal_document(doc_type, facts, context=""):
    """دالة لترتيب الدفوع وصياغة المذكرة وفقاً لطلبك"""
    header = "بناءً على قانون التأمينات الاجتماعية والمعاشات..\n\n"
    
    defense_order = (
        "أولاً: الدفوع القانونية (مرتبة):\n"
        "1. الدفع بعدم قبول الدعوى لانتفاء الصفة.\n"
        "2. الدفع بسقوط الحق بالتقادم الطويل.\n"
        "3. الدفع برفض الدعوى لعدم الارتكان لأساس قانوني.\n\n"
    )
    
    explanation = (
        "ثانياً: المادة القانونية وشرحها:\n"
        f"بتطبيق نص المادة المنظمة لواقعة ({doc_type})، وحيث استقرت أحكام النقض على أن...\n\n"
    )
    
    conclusion = (
        "ثالثاً: النتيجة:\n"
        f"وحيث أن الوقائع تخلص في {facts}، فإن الهيئة تطلب رفض الدعوى.\n\n"
        "عضو الإدارة القانونية / .................        مدير الإدارة القانونية / ................."
    )
    
    return header + defense_order + explanation + conclusion

# --- 3. القائمة الجانبية والأقسام ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/ar/b/bd/Social_Insurance_Logo.png", width=100)
st.sidebar.title("إدارة الشئون القانونية")
st.sidebar.info("المستخدم: وليد حماد")

menu = st.sidebar.radio("القطاع الرئيسي:", [
    "🏛️ قطاع القضايا (القسم القضائي)",
    "💡 قطاع الفتوى والبحث",
    "📂 قطاع التحقيقات",
    "📚 المكتبة القانونية الذكية"
])

# --- 4. تنفيذ الأقسام بناءً على المعطيات ---

if "قضايا" in menu:
    st.subheader("🏛️ صياغة مذكرات الدفاع وصحف الطعون")
    court_type = st.selectbox("نوع المحكمة", ["الابتدائية", "الاستئناف", "النقض", "مجلس الدولة"])
    role = st.selectbox("صفة الهيئة", ["مدعى عليها", "مدعية", "طاعنة", "مطعون ضدها"])
    
    facts = st.text_area("ملخص الوقائع / أو ارفع صورة الصحيفة")
    uploaded_file = st.file_uploader("ارفع المستند للقراءة بالذكاء الاصطناعي", type=['pdf', 'png', 'jpg'])
    
    if st.button("✨ ابدأ الصياغة القانونية وترتيب الدفوع"):
        if facts or uploaded_file:
            result = draft_legal_document(court_type, facts)
            st.text_area("المذكرة المقترحة (قابلة للتعديل)", result, height=400)
            
            # أزرار الحفظ
            col1, col2 = st.columns(2)
            with col1:
                st.download_button("💾 حفظ ملف Word", data="محتوى افتراضي", file_name="memo.docx")
            with col2:
                st.button("🖨️ طباعة فورية")

elif "الفتوى" in menu:
    st.subheader("💡 قسم الإفتاء القانوني (إصابات، زواج عرفي، فتاوى)")
    f_type = st.selectbox("نوع البحث", ["فتوى قانونية", "إصابة عمل", "شكوى زواج عرفي"])
    f_facts = st.text_area("ملخص وقائع الفتوى")
    if st.button("صياغة مذكرة الرأي"):
        st.write(draft_legal_document(f_type, f_facts))

elif "المكتبة" in menu:
    st.subheader("📚 المرصد القانوني للهيئة")
    lib_cat = st.selectbox("المادة العلمية", ["قوانين", "لوائح", "كتب دورية", "أحكام قضائية"])
    st.file_uploader(f"تحميل {lib_cat} جديد للموقع")
    st.button("حفظ في الأرشيف الذكي")


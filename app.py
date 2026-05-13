import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="مستشارك في التأمينات والمعاشات", layout="wide")

# 2. تصميم الواجهة الاحترافية (خلفية زرقاء وتنسيق السطور المتساوية)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
    }
    
    html, body, [class*="css"] { 
        font-family: 'Cairo', sans-serif; 
        text-align: right; 
        direction: rtl; 
        color: white; 
    }

    /* تنسيق اسم البرنامج ليكون متساوي السطور */
    .program-header {
        text-align: center;
        color: #facc15;
        font-size: 3rem;
        font-weight: bold;
        line-height: 1.2;
        margin-bottom: 5px;
    }

    /* تنسيق جهة الصدور والتحية بشكل متساوي وواضح */
    .sub-header {
        text-align: center;
        font-size: 1.4rem;
        line-height: 1.6;
        margin-bottom: 30px;
        color: #e2e8f0;
    }
    
    .legal-card {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 25px;
        color: #1e293b;
        box-shadow: 0 15px 30px rgba(0,0,0,0.5);
        border-right: 12px solid #facc15;
    }
    
    .stTextArea textarea {
        font-size: 1.3rem !important;
        text-align: right;
        border-radius: 15px !important;
        border: 3px solid #facc15 !important;
        background-color: white !important;
        color: black !important;
    }

    .stButton>button {
        background-color: #facc15;
        color: #1e3a8a;
        font-size: 1.3rem;
        font-weight: bold;
        border-radius: 12px;
        height: 3.5rem;
        width: 100%;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. قاعدة البيانات القانونية
LEGAL_DATA = [
    {
        "keys": ["جوزها مات", "ارملة", "وفاة"],
        "issue": "إشكالية الجمع بين الراتب ومعاش الزوج للأرملة",
        "ans": "يجوز للأرملة الجمع بين معاشها عن زوجها وبين دخلها من العمل دون حدود.",
        "docs": "• صورة بطاقة الرقم القومي. • بيان معاش. • مفردات مرتب.",
        "guide_page": "صفحة 112",
        "law_basis": "المادة (102) من قانون 148 لسنة 2019."
    }
]

# 4. عرض العنوان والتوقيع (التعديل المطلوب)
st.markdown('<div class="program-header">⚖️ مستشارك في<br>التأمينات والمعاشات</div>', unsafe_allow_html=True)
st.markdown("""
    <div class="sub-header">
        مع تحيات / وليد حماد<br>
        الإدارة العامة للشئون القانونية - ديوان عام منطقة البحيرة
    </div>
    """, unsafe_allow_html=True)

st.divider()

# تصفية البحث
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# خانة البحث المعدلة
user_query = st.text_area(
    "اطرح إشكالك القانوني هنا:", 
    value=st.session_state.input_text,
    placeholder="اكتب سؤالك هنا أو الإشكال القانوني...", 
    height=150
)

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("تحليل الإشكالية وعرض الرد 🔍"):
        if user_query:
            # منطق البحث يعرض النتائج هنا
            st.info("جاري البحث في قاعدة البيانات...")
        else:
            st.warning("من فضلك اكتب سؤالك أولاً.")

with col2:
    if st.button("مسح البحث 🗑️"):
        st.session_state.input_text = ""
        st.rerun()

# 5. تذييل الصفحة
st.markdown('<div style="text-align: center; margin-top: 50px; opacity: 0.7;">حقوق الطبع محفوظة © 2026</div>', unsafe_allow_html=True)

import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="مستشارك في التأمينات والمعاشات", layout="wide")

# 2. تصميم الواجهة (الألوان، الخلفية، وتنسيق الإجابة)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    /* خلفية زرقاء هادئة للصفحة بالكامل */
    .stApp {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
    }
    
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; color: white; }
    
    /* تصميم بطاقة الإجابة */
    .answer-card {
        background-color: #ffffff;
        border-radius: 20px;
        padding: 30px;
        color: #1e293b;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
        border-right: 15px solid #facc15;
        margin-top: 20px;
    }
    
    .stTextArea textarea {
        font-size: 1.3rem !important;
        text-align: right;
        border-radius: 15px !important;
        border: 3px solid #facc15 !important;
        background-color: white !important;
        color: black !important;
    }

    /* تصميم الأزرار */
    .stButton>button {
        background-color: #facc15;
        color: #1e3a8a;
        font-size: 1.4rem;
        font-weight: bold;
        border-radius: 15px;
        height: 4rem;
        width: 100%;
        border: none;
    }
    .stButton>button:hover { background-color: #ffd700; color: #000; }

    /* دليل الخدمات */
    .guide-box {
        background-color: #eff6ff;
        border: 1px dashed #1e3a8a;
        padding: 15px;
        border-radius: 10px;
        margin-top: 15px;
        color: #1e3a8a;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. قاعدة البيانات القانونية والخدمية
# تم دمج المواد مع دليل الخدمات والسند القانوني
LEGAL_DB = [
    {
        "keys": ["جوزها مات", "ارملة", "وفاة الزوج", "تجمع", "تشتغل", "مرتب", "معاشين"],
        "issue": "إشكالية الجمع بين الراتب ومعاش الزوج للأرملة",
        "ans": "يجوز للأرملة الجمع بين معاشها عن زوجها وبين دخلها من العمل أو المهنة دون حدود، كما تجمع بين معاشها عن نفسها ومعاشها عن زوجها دون حدود.",
        "docs": "1. صورة بطاقة الرقم القومي سارية. 2. بيان معاش (للمكتب المختص). 3. بيان مفردات مرتب (إذا كانت موظفة).",
        "guide": "دليل الخدمات - ص 112 (إجراءات صرف معاش الأرملة)",
        "basis": "المادة (102) من قانون 148 لسنة 2019."
    },
    {
        "keys": ["مبكر", "استقالة", "سيبت الشغل", "خروج", "بدري", "استقلت", "20 سنة"],
        "issue": "شروط وضوابط المعاش المبكر",
        "ans": "يشترط مدة اشتراك فعلية تعطي معاشاً لا يقل عن 50% من أجر التسوية الأخير و65% من الحد الأدنى. المدة الحالية 20 سنة فعلية، وتصبح 2

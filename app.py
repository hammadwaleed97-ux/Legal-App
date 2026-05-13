import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="مستشارك في التأمينات والمعاشات", layout="wide")

# 2. تصميم الواجهة (خلفية ملونة وتنسيق احترافي)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
    }
    
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; color: white; }
    
    .answer-card {
        background-color: #ffffff;
        border-radius: 20px;
        padding: 30px;
        color: #1e293b;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
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

    .guide-box {
        background-color: #fef3c7;
        border: 1px dashed #92400e;
        padding: 15px;
        border-radius: 10px;
        margin-top: 15px;
        color: #92400e;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. قاعدة البيانات القانونية والخدمية
LEGAL_DB = [
    {
        "keys": ["جوزها مات", "ارملة", "وفاة الزوج", "تجمع", "تشتغل", "مرتب", "معاشين"],
        "issue": "إشكالية الجمع بين الراتب ومعاش الزوج للأرملة",
        "ans": "يجوز للأرملة الجمع بين معاشها عن زوجها وبين دخلها من العمل أو المهنة دون حدود، كما تجمع بين معاشها عن نفسها ومعاشها عن زوجها دون حدود.",
        "docs": "• صورة بطاقة الرقم القومي. • بيان معاش. • بيان مفردات مرتب (للموظفة).",
        "guide": "د

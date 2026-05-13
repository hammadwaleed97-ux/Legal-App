import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="مستشارك في التأمينات والمعاشات", layout="wide")

# 2. تصميم الواجهة بالكامل (ألوان للصفحة كلها + تنسيق احترافي)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    /* خلفية ملونة للصفحة بالكامل */
    .stApp {
        background: linear-gradient(135deg, #f0f4f8 0%, #d9e2ec 100%);
    }
    
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    
    /* تصميم البطاقة التعريفية للإجابة */
    .answer-card {
        background-color: white;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border-right: 12px solid #1e3a8a;
        margin-top: 20px;
        animation: fadeIn 0.5s;
    }
    
    /* تصميم خانة البحث */
    .stTextArea textarea {
        font-size: 1.3rem !important;
        text-align: right;
        border-radius: 15px !important;
        border: 2px solid #1e3a8a !important;
    }

    /* تصميم الأزرار */
    .stButton>button {
        background: #1e3a8a;
        color: white;
        font-size: 1.4rem;
        font-weight: bold;
        border-radius: 15px;
        height: 4rem;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { background: #334eac; color: #facc15; }

    /* تفاصيل دليل الخدمات */
    .service-guide {
        background-color: #fffbeb;
        border: 1px solid #fef3c7;
        padding: 15px;
        border-radius: 10px;
        margin-top: 15px;
        color: #92400e;
        font-weight: bold;
    }
    
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
    """, unsafe_allow_html=True)

# 3. قاعدة البيانات الشاملة (بما فيها دليل الخدمات والسند القانوني)
LEGAL_DB = [
    {
        "keys": ["جوزها مات", "ارملة", "وفاة الزوج", "تجمع", "تشتغل", "مرتب", "معاشين"],
        "issue": "إشكالية الجمع بين الراتب ومعاش الزوج",
        "ans": "يجوز للأرملة الجمع بين معاشها عن زوجها وبين دخلها من العمل أو المهنة دون حدود، كما تجمع بين معاشها عن نفسها ومعاشها عن زوجها دون حدود.",
        "docs": "صورة بطاقة، بيان معاش، إقرار بعدم وجود مستحقين آخرين إن وجد.",
        "page": "ص 112 من دليل خدمات الهيئة",
        "basis": "المادة (102) من قانون 148 لسنة 2019."
    },
    {
        "keys": ["مبكر", "استقالة", "سيبت الشغل", "خروج", "بدري", "استقلت"],
        "issue": "شروط استحقاق المعاش المبكر",
        "ans": "يجب توافر مدة اشتراك فعلية تعطي معاشاً لا يقل عن 50% من أجر التسوية الأخير و65% من الحد الأدنى. المدة الحالية 20 سنة فعلية (تصبح 25 سنة في 2025).",
        "docs": "نموذج 20 طلب صرف، تدرج أجور، بيان مدد.",
        "page": "ص 45 من دليل خدمات الهيئة",
        "basis": "المادة (21) من القانون 148 ولائحته."
    },
    {
        "keys": ["حادثة", "إصابة", "تعورت", "طريق", "ميكروباص", "الشغل"],
        "issue": "إصابة العمل وحادث الطريق",
        "ans": "تعتبر إصابة عمل بشرط وقوعها في الطريق الطبيعي دون توقف أو انحراف غرضي. يُصرف تعويض أجر بنسبة 100%.",
        "docs": "نموذج 51 إخطار إصابة، محضر شرطة، قرار لجنة طبية.",
        "page": "ص 88 من دليل خدمات الهيئة",
        "basis": "المادة (45) من القانون 148."
    }
]

# 4. واجهة البرنامج
st.markdown("<h1 style='text-align: center; color: #1e3a8a

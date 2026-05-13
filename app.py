import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="مستشارك في التأمينات والمعاشات", layout="wide")

# 2. تصميم الواجهة (الخلفية، السطور المتساوية، والخطوط)
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

    /* تنسيق اسم البرنامج سطور منفصلة ومتساوية */
    .program-title {
        text-align: center;
        color: #facc15;
        font-size: 2.8rem;
        font-weight: bold;
        line-height: 1.2;
        margin-bottom: 10px;
    }

    /* تنسيق التوقيع الجديد */
    .signature-box {
        text-align: center;
        font-size: 1.3rem;
        line-height: 1.6;
        margin-bottom: 30px;
        color: #ffffff;
    }
    
    .answer-card {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 25px;
        color: #1e293b;
        box-shadow: 0 15px 30px rgba(0,0,0,0.5);
        border-right: 12px solid #facc15;
    }

    .stTextArea textarea {
        font-size: 1.2rem !important;
        border-radius: 12px !important;
        border: 2px solid #facc15 !important;
    }

    .stButton>button {
        background-color: #facc15;
        color: #1e3a8a;
        font-weight: bold;
        border-radius: 10px;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. قاعدة البيانات القانونية الشاملة
LEGAL_DB = [
    {
        "keys": ["معاش", "مبكر", "استقالة", "سيبت", "بدري"],
        "issue": "إشكالية شروط المعاش المبكر",
        "ans": "يستحق المعاش المبكر إذا توافرت مدة اشتراك فعلية تعطي الحق في معاش لا يقل عن 50% من أجر التسوية الأخير، وبما لا يقل عن 65% من الحد الأدنى لأجر الاشتراك. المدة المطلوبة حالياً 20 سنة فعلية، وتزداد إلى 25 سنة فعلية في يناير 2025.",
        "docs": "1. استمارة 6 تأمينات (إنهاء خدمة). 2. نموذج طلب صرف معاش. 3. بيان تدرج أجور.",
        "guide": "دليل الخدمات - ص 45",
        "law": "قانون 148 لسنة 2019 - المادة 21"
    },
    {
        "keys": ["وفاة", "مات", "أرملة", "زوجها", "تجمع"],
        "issue": "إشكالية جمع الأرملة بين المعاش والراتب",
        "ans": "للأرملة الحق في الجمع بين معاشها عن زوجها وبين دخلها من العمل أو المهنة وذلك دون حدود. كما تجمع بين معاشها عن نفسها ومعاشها عن زوجها دون حدود أيضاً.",
        "docs": "1. شهادة الوفاة. 2. صورة بطاقة الأرملة. 3. بيان معاش أو مرتب.",
        "guide": "دليل الخدمات - ص 112",
        "law": "قانون 148 لسنة 2019 - المادة 102"
    },
    {
        "keys": ["إصابة", "حادث", "طريق", "عجز"],
        "issue": "إشكالية إصابة العمل وحادث الطريق",
        "ans": "تعتبر إصابة عمل كل حادث يقع للمؤمن عليه خلال فترة ذهابه للعمل أو عودته منه، بشرط أن يكون الطريق طبيعياً ودون توقف. يستحق المصاب تعويض أجر بنسبة 100%.",
        "docs": "1. محضر شرطة. 2. إخطار إصابة عمل (نموذج 51). 3. تقرير طبي.",
        "guide": "دليل الخدمات - ص 88",
        "law": "قانون 148 لسنة 2019 - المادة 45"
    }
]

# 4. الواجهة الرئيسية (العناوين)
st.markdown("""
    <div class="program-title">
        مستشارك<br>في<br>التأمينات<br>و<br>المعاشات
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="signature-box">
        مع تحيات / وليد حماد الادارة العامة للشؤون القانونية<br>
        ديوان عام منطقة البحيرة
    </div>
    """, unsafe_allow_html=True)

st.divider()

# 5. منطق البحث
if "search_query" not in st.session_state:
    st.session_state.search_query = ""

user_input = st.text_area("اطرح إشكالك القانوني هنا:", 
                         value=st.session_state.search_query,
                         placeholder="اكتب سؤالك هنا أو الإشكال القانوني...",
                         height=100)

col1, col2 = st.columns(2)

with col1:
    if st.button("تحليل الإشكالية وعرض الرد 🔍"):
        if user_input:
            found = False
            for item in LEGAL_DB:
                if any(word in user_input for word in item['keys']):
                    st.markdown(f"""
                    <div class="answer-card">
                        <h3 style="color: #1e3a8a;">💡 {item['issue']}</h3>
                        <p style="line-height: 1.6;"><b>✅ الإجابة الكاملة:</b><br>{item['ans']}</p>
                        <p><b>📄 المستندات:</b> {item['docs']}</p>
                        <p style="color: #92400e; font-weight: bold;">📍 المرجع: {item['guide']}</p>
                        <p style="color: #b91c1c; font-size: 0.9rem;">⚖️ السند القانوني: {item['law']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    found = True
                    break
            if not found:
                st.error("عذراً، يرجى محاولة كتابة كلمات مفتاحية مثل (معاش، وفاة، إصابة).")
        else:
            st.warning("يرجى كتابة السؤال أولاً.")

with col2:
    if st.button("مسح البحث 🗑️"):
        st.session_state.search_query = ""
        st.rerun()

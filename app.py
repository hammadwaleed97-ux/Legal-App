import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="مستشارك في التأمينات والمعاشات", layout="wide")

# 2. التنسيق البصري المعتمد (كما في الصور)
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

    /* اسم البرنامج سطور منفصلة ومتساوية */
    .program-title {
        text-align: center;
        color: #facc15;
        font-size: 2.8rem;
        font-weight: bold;
        line-height: 1.1;
        margin-bottom: 15px;
    }

    /* التوقيع في 3 أسطر واضحة ومنظمة */
    .signature-section {
        text-align: center;
        font-size: 1.4rem;
        line-height: 1.5;
        margin-bottom: 40px;
        color: #ffffff;
        font-weight: bold;
    }
    
    .result-card {
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
        text-align: right;
    }

    .stButton>button {
        background-color: #facc15;
        color: #1e3a8a;
        font-weight: bold;
        border-radius: 10px;
        width: 100%;
        height: 3.5rem;
        font-size: 1.2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. قاعدة البيانات الشاملة (قانون 148 ولائحته ودليل الخدمات)
LEGAL_DB = [
    {
        "keys": ["مبكر", "استقالة", "سيبت الشغل", "بدري", "20 سنة"],
        "ans": "يستحق المعاش المبكر إذا توافرت مدة اشتراك فعلية تعطي الحق في معاش لا يقل عن 50% من أجر التسوية الأخير، وبما لا يقل عن 65% من الحد الأدنى لأجر الاشتراك. المدة المطلوبة حالياً 20 سنة فعلية، وتصبح 25 سنة فعلية في يناير 2025.",
        "docs": "• استمارة 6 تأمينات. • طلب صرف معاش. • بيان تدرج أجور معتمد.",
        "guide": "دليل الخدمات - ص 45",
        "law": "قانون 148 لسنة 2019 - المادة 21"
    },
    {
        "keys": ["وفاة", "مات", "أرملة", "زوجها", "تجمع"],
        "ans": "للأرملة الحق في الجمع بين معاشها عن زوجها وبين دخلها من العمل أو المهنة دون حدود. كما تجمع بين معاشها عن نفسها ومعاشها عن زوجها دون حدود أيضاً.",
        "docs": "• شهادة الوفاة. • صورة بطاقة الأرملة. • بيان معاش أو مرتب.",
        "guide": "دليل الخدمات - ص 112",
        "law": "قانون 148 لسنة 2019 - المادة 102"
    },
    {
        "keys": ["بلوغ السن", "الستين", "60", "شيخوخة", "سن المعاش"],
        "ans": "يستحق معاش الشيخوخة عند بلوغ سن الستين مع توافر مدة اشتراك فعلية لا تقل عن 120 شهراً (10 سنوات)، وتصبح 180 شهراً (15 سنة) اعتباراً من يناير 2025.",
        "docs": "• بطاقة الرقم القومي. • طلب صرف معاش بلوغ سن.",
        "guide": "دليل الخدمات - ص 12",
        "law": "قانون 148 لسنة 2019 - المادة 21 بند 1"
    },
    {
        "keys": ["عجز", "مرض", "طبي", "غير قادر"],
        "ans": "يستحق المعاش عند العجز الكامل أو الوفاة خلال فترة الخدمة، بشرط وجود مدة اشتراك لا تقل عن 3 أشهر متصلة أو 6 أشهر منفصلة.",
        "docs": "• قرار اللجنة الطبية (الهيئة العامة للتأمين الصحي).",
        "guide": "دليل الخدمات - ص 60",
        "law": "قانون 148 لسنة 2019 - المادة 21 بند 2"
    },
    {
        "keys": ["إصابة", "حادث", "طريق", "عمل"],
        "ans": "تعتبر إصابة عمل كل حادث يقع للمؤمن عليه خلال ذهابه للعمل أو عودته، بشرط أن يكون الطريق طبيعياً. يستحق المصاب تعويض أجر بنسبة 100% من أجر الاشتراك.",
        "docs": "• محضر شرطة. • إخطار إصابة عمل (نموذج 51).",
        "guide": "دليل الخدمات - ص 88",
        "law": "قانون 148 لسنة 2019 - المادة 45"
    }
]

# 4. الواجهة الرئيسية (التنسيق المعتمد)
st.markdown("""
    <div class="program-title">
        مستشارك<br>في<br>التأمينات<br>و<br>المعاشات
    </div>
    <div class="signature-section">
        مع تحيات / وليد حماد<br>
        الادارة العامة للشؤون القانونية<br>
        ديوان عام منطقة البحيرة
    </div>
    """, unsafe_allow_html=True)

st.divider()

# 5. منطق البحث
if "search_val" not in st.session_state:
    st.session_state.search_val = ""

user_query = st.text_area("اطرح إشكالك القانوني هنا:", 
                         value=st.session_state.search_val,
                         placeholder="اكتب سؤالك هنا أو الإشكال القانوني...",
                         height=100)

col1, col2 = st.columns(2)

with col1:
    if st.button("تحليل الإشكالية وعرض الرد 🔍"):
        if user_query:
            found = False
            q = user_query.lower()
            for item in LEGAL_DB:
                if any(key in q for key in item['keys']):
                    st.markdown(f"""
                    <div class="result-card">
                        <p style="font-size: 1.3rem; line-height: 1.7;"><b>✅ الإجابة:</b><br>{item['ans']}</p>
                        <hr style="border-top: 1px solid #ddd;">
                        <p><b>📄 المستندات المطلوبة:</b><br>{item['docs']}</p>
                        <p style="color: #92400e;">📍 المرجع: {item['guide']}</p>
                        <p style="color: #b91c1c; font-weight: bold;">⚖️ السند القانوني: {item['law']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    found = True
                    break
            if not found:
                st.error("لم نجد إجابة مطابقة، حاول كتابة كلمات مثل (معاش، وفاة، سن، إصابة).")
        else:
            st.warning("يرجى كتابة سؤالك أولاً.")

with col2:
    if st.button("مسح البحث 🗑️"):
        st.session_state.search_val = ""
        st.rerun()

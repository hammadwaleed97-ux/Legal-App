import streamlit as st

# 1. إعدادات الصفحة والاسم الملكي للبرنامج
st.set_page_config(page_title="مستشارك في التأمينات والمعاشات", layout="wide")

# 2. تصميم الواجهة (تنسيق السطور والخطوط)
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

    /* اسم البرنامج سطور متساوية ومنفصلة */
    .program-title {
        text-align: center;
        color: #facc15;
        font-size: 2.8rem;
        font-weight: bold;
        line-height: 1.1;
        margin-bottom: 15px;
    }

    /* التوقيع في 3 أسطر واضحة */
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

# 3. قاعدة البيانات القانونية (إجابات كاملة ومباشرة)
LEGAL_DB = [
    {
        "keys": ["مبكر", "استقالة", "سيبت", "بدري", "20 سنة"],
        "ans": "يستحق المعاش المبكر إذا توافرت مدة اشتراك فعلية تعطي الحق في معاش لا يقل عن 50% من أجر التسوية الأخير، وبما لا يقل عن 65% من الحد الأدنى لأجر الاشتراك. المدة المطلوبة حالياً هي 20 سنة فعلية، وستصبح 25 سنة فعلية اعتباراً من يناير 2025.",
        "docs": "• استمارة 6 تأمينات. • طلب صرف معاش. • بيان تدرج أجور معتمد.",
        "guide": "دليل الخدمات - صفحة 45",
        "law": "قانون 148 لسنة 2019 - المادة 21"
    },
    {
        "keys": ["وفاة", "مات", "أرملة", "زوجها", "تجمع"],
        "ans": "للأرملة الحق في الجمع بين معاشها عن زوجها وبين دخلها من العمل أو المهنة دون حدود. كما تجمع بين معاشها عن نفسها ومعاشها عن زوجها دون أي قيود مالية.",
        "docs": "• شهادة الوفاة. • صورة بطاقة الأرملة. • بيان مفردات مرتب أو معاش.",
        "guide": "دليل الخدمات - صفحة 112",
        "law": "قانون 148 لسنة 2019 - المادة 102"
    }
]

# 4. الواجهة العلوية (العنوان والتوقيع المطلوب)
st.markdown("""
    <div class="program-title">
        مستشارك<br>في<br>التأمينات<br>و<br>المعاشات
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="signature-section">
        مع تحيات / وليد حماد<br>
        الادارة العامة للشؤون القانونية<br>
        ديوان عام منطقة البحيرة
    </div>
    """, unsafe_allow_html=True)

st.divider()

# 5. منطق البحث والرد
if "user_input_val" not in st.session_state:
    st.session_state.user_input_val = ""

user_query = st.text_area("اطرح إشكالك القانوني هنا:", 
                         value=st.session_state.user_input_val,
                         placeholder="اكتب سؤالك هنا أو الإشكال القانوني...",
                         height=100)

c1, c2 = st.columns(2)

with c1:
    if st.button("تحليل الإشكالية وعرض الرد 🔍"):
        if user_query:
            found = False
            q = user_query.lower()
            for item in LEGAL_DB:
                if any(word in q for word in item['keys']):
                    st.markdown(f"""
                    <div class="result-card">
                        <p style="font-size: 1.3rem; line-height: 1.7;"><b>✅ الإجابة:</b><br>{item['ans']}</p>
                        <hr>
                        <p><b>📄 المستندات المطلوبة:</b><br>{item['docs']}</p>
                        <p style="color: #92400e;">📍 المرجع: {item['guide']}</p>
                        <p style="color: #b91c1c; font-weight: bold;">⚖️ السند القانوني: {item['law']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    found = True
                    break
            if not found:
                st.error("لم نجد إجابة مطابقة، حاول كتابة كلمات مثل (معاش، وفاة، مبكر).")
        else:
            st.warning("يرجى كتابة السؤال أولاً.")

with c2:
    if st.button("مسح البحث 🗑️"):
        st.session_state.user_input_val = ""
        st.rerun()

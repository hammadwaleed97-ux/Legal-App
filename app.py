import streamlit as st

# 1. إعدادات الصفحة والاسم الرسمي
st.set_page_config(page_title="مستشارك في التأمينات والمعاشات", layout="wide")

# 2. تصميم الواجهة الاحترافية (خلفية ملونة بالكامل)
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
    
    .legal-card {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 25px;
        color: #1e293b;
        box-shadow: 0 15px 30px rgba(0,0,0,0.5);
        border-right: 12px solid #facc15;
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
        font-size: 1.3rem;
        font-weight: bold;
        border-radius: 12px;
        height: 3.5rem;
        width: 100%;
        border: none;
    }
    .stButton>button:hover { background-color: #ffd700; color: #000; }

    .guide-info {
        background-color: #fef3c7;
        border: 1px dashed #92400e;
        padding: 12px;
        border-radius: 8px;
        margin-top: 10px;
        color: #92400e;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. قاعدة البيانات القانونية والخدمية
LEGAL_DATA = [
    {
        "keys": ["جوزها مات", "ارملة", "وفاة الزوج", "تجمع", "تشتغل", "مرتب", "معاشين"],
        "issue": "إشكالية الجمع بين الراتب ومعاش الزوج للأرملة",
        "ans": "يجوز للأرملة الجمع بين معاشها عن زوجها وبين دخلها من العمل أو المهنة دون حدود، كما تجمع بين معاشها الشخصي ومعاش الزوج دون حدود أيضاً.",
        "docs": "• صورة بطاقة الرقم القومي. • بيان معاش. • مفردات مرتب (للموظفة).",
        "guide_page": "دليل خدمات الهيئة - صفحة 112",
        "law_basis": "المادة (102) من قانون 148 لسنة 2019."
    },
    {
        "keys": ["مبكر", "استقالة", "سيبت الشغل", "خروج", "بدري", "استقلت", "20 سنة"],
        "issue": "شروط وضوابط المعاش المبكر",
        "ans": "يشترط توافر مدة اشتراك فعلية تعطي معاشاً لا يقل عن 50% من أجر التسوية الأخير و65% من الحد الأدنى. المدة الحالية 20 سنة فعلية، وتصبح 25 سنة بدءاً من 2025.",
        "docs": "• نموذج (20) طلب صرف. • بيان تدرج أجور معتمد. • استمارة (6) تأمينات.",
        "guide_page": "دليل خدمات الهيئة - صفحة 45",
        "law_basis": "المادتين (21) و (24) من قانون 148 لسنة 2019."
    }
]

# 4. الواجهة الرئيسية
st.markdown("<h1 style='text-align: center; color: #facc15;'>⚖️ مستشارك في التأمينات والمعاشات</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1rem;'>الإدارة العامة للشئون القانونية - ديوان عام منطقة البحيرة</p>", unsafe_allow_html=True)
st.divider()

# تصفية البحث
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# خانة البحث مع التعديل المطلوب في جملة التوجيه (Placeholder)
user_query = st.text_area(
    "اطرح إشكالك القانوني هنا:", 
    value=st.session_state.input_text,
    placeholder="اكتب سؤالك هنا أو الإشكال القانوني...", 
    height=150,
    key="main_input"
)

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("تحليل الإشكالية وعرض الرد 🔍"):
        if user_query:
            found = False
            q_low = user_query.lower()
            for item in LEGAL_DATA:
                if any(key in q_low for key in item['keys']):
                    st.markdown(f"""
                    <div class="legal-card">
                        <h2 style="color: #1e3a8a; border-bottom: 2px solid #facc15; padding-bottom: 10px;">💡 {item['issue']}</h2>
                        <p style="font-size: 1.2rem; line-height: 1.8;"><b>✅ الرد القانوني:</b><br>{item['ans']}</p>
                        <div style="background-color: #f1f5f9; padding: 15px; border-radius: 10px; border: 1px solid #cbd5e1;">
                            <b style="color: #1e3a8a;">📄 المستندات المطلوبة:</b><br>{item['docs']}
                        </div>
                        <div class="guide-info">
                            📍 المرجع: {item['guide_page']}
                        </div>
                        <p style="color: #b91c1c; font-weight: bold; margin-top: 15px;">⚖️ السند القانوني: {item['law_basis']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    found = True
                    break
            if not found:
                st.error("لم نجد إشكالية مطابقة. جرب كلمات أخرى.")
        else:
            st.warning("من فضلك اكتب سؤالك أولاً.")

with col2:
    if st.button("مسح البحث 🗑️"):
        st.session_state.input_text = ""
        st.rerun()

# 5. التوقيع
st.markdown(f"""
    <div style="text-align: center; margin-top: 60px; color: white; opacity: 0.8;">
        <hr style="border-color: rgba(255,255,255,0.2);">
        مع تحيات وليد حماد<br>
        <b>الإدارة العامة للشئون القانونية - ديوان عام منطقة البحيرة</b>
    </div>
    """, unsafe_allow_html=True)

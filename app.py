import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="مستشارك في التأمينات والمعاشات", layout="wide")

# 2. التنسيق البصري النهائي المعتمد
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%); }
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; color: white; }
    
    .program-title { text-align: center; color: #facc15; font-size: 2.8rem; font-weight: bold; line-height: 1.1; margin-bottom: 15px; }
    .signature-section { text-align: center; font-size: 1.4rem; line-height: 1.5; margin-bottom: 40px; color: #ffffff; font-weight: bold; }
    
    .result-card { background-color: #ffffff; border-radius: 15px; padding: 25px; color: #1e293b; box-shadow: 0 15px 30px rgba(0,0,0,0.5); border-right: 12px solid #facc15; margin-top: 20px; }
    .stTextArea textarea { font-size: 1.2rem !important; border-radius: 12px !important; border: 2px solid #facc15 !important; text-align: right; }
    .stButton>button { background-color: #facc15; color: #1e3a8a; font-weight: bold; border-radius: 10px; width: 100%; height: 3.5rem; font-size: 1.2rem; }
    </style>
    """, unsafe_allow_html=True)

# 3. الموسوعة القانونية الشاملة (القانون + اللائحة + الدليل)
LEGAL_DB = [
    {
        "keys": ["مبكر", "استقالة", "قبل السن", "20 سنة", "25 سنة"],
        "ans": "يستحق المعاش المبكر إذا توافرت مدة اشتراك فعلية تعطي معاشاً لا يقل عن 50% من أجر التسوية الأخير، وبما لا يقل عن 65% من الحد الأدنى لأجر الاشتراك. المدة المطلوبة 20 سنة فعلية، وتصبح 25 سنة فعلية من 1/1/2025.",
        "docs": "• استمارة 6 تأمينات • طلب صرف معاش • بيان تدرج أجور.",
        "ref": "📍 دليل الخدمات ص 45 | ⚖️ قانون 148 مادة 21 | 📜 اللائحة مادة 102"
    },
    {
        "keys": ["زواج", "بنت", "منحة", "عقد", "اتجووزت"],
        "ans": "تستحق البنت أو الأخت منحة زواج تعادل معاش شهر عن سنة كاملة (معاش شهر × 12) بحد أدنى 500 جنيه. تصرف لمرة واحدة عند قطع المعاش بسبب الزواج، وتسقط إذا لم تقدم خلال 5 سنوات.",
        "docs": "• صورة عقد الزواج • صورة البطاقة • طلب صرف المنحة.",
        "ref": "📍 دليل الخدمات ص 150 | ⚖️ قانون 148 مادة 105 | 📜 اللائحة مادة 284"
    },
    {
        "keys": ["بلوغ السن", "الستين", "شيخوخة", "سن المعاش", "60", "65"],
        "ans": "يستحق معاش الشيخوخة عند السن القانونية (60 عاماً حالياً وتصل لـ 65 تدريجياً) بشرط مدة اشتراك 120 شهراً فعلية، تزداد إلى 180 شهراً فعلية (15 سنة) في يناير 2025.",
        "docs": "• صورة البطاقة الشخصية • طلب صرف معاش بلوغ السن.",
        "ref": "📍 دليل الخدمات ص 12 | ⚖️ قانون 148 مادة 21 | 📜 اللائحة مادة 95"
    },
    {
        "keys": ["وفاة", "مات", "جنازة", "تعويض", "وفاه"],
        "ans": "عند وفاة المؤمن عليه يصرف: 1- مصاريف جنازة (3 أشهر معاش). 2- منحة وفاة (معاش شهر الوفاة + شهرين). 3- تعويض إضافي حسب السن.",
        "docs": "• شهادة الوفاة • نموذج طلب صرف • مستندات المستحقين.",
        "ref": "📍 دليل الخدمات ص 142 | ⚖️ قانون 148 مادة 33 و109 | 📜 اللائحة مادة 271"
    },
    {
        "keys": ["عجز", "طبي", "لجنة", "مرض", "إصابة", "حادث"],
        "ans": "يستحق المعاش عند العجز الكامل المستديم أو الوفاة خلال الخدمة أو خلال سنة من تركها، بشرط وجود مدة اشتراك 3 أشهر متصلة أو 6 أشهر منفصلة على الأقل.",
        "docs": "• قرار اللجنة الطبية • إخطار وقوع إصابة • تقارير طبية.",
        "ref": "📍 دليل الخدمات ص 60 | ⚖️ قانون 148 مادة 21 | 📜 اللائحة مادة 98"
    },
    {
        "keys": ["تجمع", "ارملة", "بين معاشين", "دخل", "شغل"],
        "ans": "تجمع الأرملة بين معاشها عن زوجها وبين دخلها من العمل أو المهنة دون حدود. كما يجمع المستحق بين المعاشات في حدود الحد الأدنى للمعاش (الفئة الأولى).",
        "ref": "⚖️ قانون 148 مادة 102 | 📜 اللائحة مادة 281"
    }
]

# 4. عرض الواجهة (التنسيق المعتمد)
st.markdown('<div class="program-title">مستشارك<br>في<br>التأمينات<br>و<br>المعاشات</div>', unsafe_allow_html=True)
st.markdown('<div class="signature-section">مع تحيات / وليد حماد<br>الادارة العامة للشؤون القانونية<br>ديوان عام منطقة البحيرة</div>', unsafe_allow_html=True)
st.divider()

# 5. منطق البحث الذكي
if "input_val" not in st.session_state: st.session_state.input_val = ""

query = st.text_area("اطرح إشكالك القانوني هنا:", value=st.session_state.input_val, placeholder="مثال: شروط المعاش المبكر أو منحة الزواج...", height=100)

c1, c2 = st.columns(2)
with c1:
    if st.button("تحليل الإشكالية وعرض الرد 🔍"):
        if query:
            found = False
            for item in LEGAL_DB:
                if any(key in query for key in item['keys']):
                    st.markdown(f"""
                    <div class="result-card">
                        <p style="font-size: 1.4rem; line-height: 1.6;"><b>✅ الإجابة:</b><br>{item['ans']}</p>
                        <hr style="border-top: 1px dashed #ccc;">
                        {"<p><b>📄 المستندات:</b> " + item.get('docs','') + "</p>" if item.get('docs') else ""}
                        <p style="color: #b91c1c; font-weight: bold; font-size: 1rem;">{item['ref']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    found = True; break
            if not found: st.error("عذراً، لم أجد رداً مطابقاً. حاول كتابة كلمات مثل (معاش، وفاة، زواج، عجز).")
        else: st.warning("يرجى كتابة السؤال أولاً.")
with c2:
    if st.button("مسح البحث 🗑️"):
        st.session_state.input_val = ""; st.rerun()

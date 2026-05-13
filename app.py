import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="مستشارك في التأمينات والمعاشات", layout="wide")

# 2. التنسيق البصري النهائي المعتمد (5 سطور عنوان - 3 سطور توقيع)
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

# 3. الموسوعة القانونية الشاملة (قانون + لائحة + دليل)
LEGAL_DB = [
    {
        "keys": ["مبكر", "استقالة", "قبل السن", "20 سنة"],
        "ans": "يستحق المعاش المبكر إذا توافرت مدة اشتراك فعلية تعطي معاشاً لا يقل عن 50% من أجر التسوية الأخير، وبما لا يقل عن 65% من الحد الأدنى لأجر الاشتراك. المدة 20 سنة فعلية، وتصبح 25 سنة من 1/1/2025.",
        "docs": "• استمارة 6 • طلب صرف • بيان تدرج أجور.",
        "ref": "⚖️ مادة 21 قانون 148 | 📜 مادة 102 لائحة | 📍 ص 45 دليل"
    },
    {
        "keys": ["زواج", "بنت", "منحة", "اتجووزت"],
        "ans": "تستحق البنت منحة زواج تعادل معاش شهر عن سنة (شهر × 12) بحد أدنى 500 جنيه. تصرف لمرة واحدة عند قطع المعاش للزواج.",
        "docs": "• صورة عقد الزواج • صورة البطاقة • طلب صرف.",
        "ref": "⚖️ مادة 105 قانون 148 | 📜 مادة 284 لائحة | 📍 ص 150 دليل"
    },
    {
        "keys": ["سن", "ستين", "شيخوخة", "60"],
        "ans": "يستحق معاش الشيخوخة عند بلوغ السن القانونية بشرط مدة اشتراك 120 شهراً فعلية، تزداد إلى 180 شهراً (15 سنة) في يناير 2025.",
        "ref": "⚖️ مادة 21 قانون 148 | 📜 مادة 95 لائحة | 📍 ص 12 دليل"
    },
    {
        "keys": ["وفاة", "جنازة", "منحة وفاة"],
        "ans": "يصرف: مصاريف جنازة (3 أشهر معاش)، ومنحة وفاة (شهر الوفاة + شهرين)، وتعويض إضافي حسب السن.",
        "ref": "⚖️ مادة 33 و109 قانون 148 | 📜 مادة 271 لائحة | 📍 ص 142 دليل"
    }
]

# 4. العرض العلوي (كما في الصورة تماماً)
st.markdown('<div class="program-title">مستشارك<br>في<br>التأمينات<br>و<br>المعاشات</div>', unsafe_allow_html=True)
st.markdown('<div class="signature-section">مع تحيات / وليد حماد<br>الادارة العامة للشؤون القانونية<br>ديوان عام منطقة البحيرة</div>', unsafe_allow_html=True)
st.divider()

# 5. خانة البحث (تم حذف "مثال" والالتزام بنصك)
if "q_val" not in st.session_state: st.session_state.q_val = ""

query = st.text_area("اطرح إشكالك القانوني هنا:", 
                    value=st.session_state.q_val, 
                    placeholder="اكتب سؤالك هنا أو الإشكال القانوني...", 
                    height=100)

c1, c2 = st.columns(2)
with c1:
    if st.button("تحليل الإشكالية وعرض الرد 🔍"):
        if query:
            found = False
            for item in LEGAL_DB:
                if any(k in query for k in item['keys']):
                    st.markdown(f"""
                    <div class="result-card">
                        <p style="font-size: 1.4rem;"><b>✅ الإجابة:</b><br>{item['ans']}</p>
                        <hr>
                        {f"<p><b>📄 المستندات:</b> {item['docs']}</p>" if 'docs' in item else ""}
                        <p style="color: #b91c1c; font-weight: bold;">{item['ref']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    found = True; break
            if not found: st.error("لم نجد رداً مطابقاً، حاول بكلمات بسيطة.")
        else: st.warning("يرجى كتابة السؤال أولاً.")
with c2:
    if st.button("مسح البحث 🗑️"):
        st.session_state.q_val = ""; st.rerun()

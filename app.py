import streamlit as st

# 1. التنسيق البصري الاحترافي (منع ظهور أي أكواد زائدة)
st.set_page_config(page_title="مستشارك التأميني الشامل", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%); }
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; color: white; }
    .program-title { text-align: center; color: #facc15; font-size: 2.5rem; font-weight: bold; line-height: 1.2; margin-bottom: 10px; }
    .signature-section { text-align: center; font-size: 1.3rem; line-height: 1.6; margin-bottom: 30px; color: #ffffff; font-weight: bold; }
    .result-card { background-color: #ffffff; border-radius: 15px; padding: 25px; color: #1e293b; border-right: 12px solid #facc15; box-shadow: 0 10px 20px rgba(0,0,0,0.3); }
    .ref-tag { background-color: #f1f5f9; padding: 10px; border-radius: 8px; margin-top: 15px; border-right: 5px solid #b91c1c; color: #b91c1c; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. واجهة العرض (التوقيع المعتمد)
st.markdown('<div class="program-title">مستشارك<br>في<br>التأمينات<br>و<br>المعاشات</div>', unsafe_allow_html=True)
st.markdown('<div class="signature-section">مع تحيات / وليد حماد<br>الادارة العامة للشؤون القانونية<br>ديوان عام منطقة البحيرة</div>', unsafe_allow_html=True)

# 3. الموسوعة القانونية الكبرى (قاعدة بيانات شاملة)
LEGAL_DB = [
    {
        "keys": ["مبكر", "استقالة", "سيبت"],
        "ans": "يستحق المعاش المبكر بتوافر مدة اشتراك فعلية تعطي معاشاً لا يقل عن 50% من أجر التسوية و65% من الحد الأدنى لأجر الاشتراك. المدة 20 سنة حالياً وتصبح 25 سنة من 2025.",
        "ref": "⚖️ مادة 21 قانون 148 | 📜 مادة 102 لائحة | 📍 ص 45 دليل"
    },
    {
        "keys": ["شيخوخة", "ستين", "60", "65", "سن"],
        "ans": "يستحق معاش الشيخوخة عند السن القانونية (60 حالياً وتصل لـ 65 تدريجياً) بشرط مدة اشتراك 120 شهراً فعلية، تزداد إلى 180 شهراً (15 سنة) في يناير 2025.",
        "ref": "⚖️ مادة 21 قانون 148 | 📜 مادة 95 لائحة | 📍 ص 12 دليل"
    },
    {
        "keys": ["إصابة", "حادث", "أثناء العمل", "طريق"],
        "ans": "إصابة العمل تشمل حوادث العمل والطريق والأمراض المهنية. يستحق المصاب تعويض أجر 100% طوال فترة العجز المؤقت.",
        "ref": "⚖️ مواد 45-51 قانون 148 | 📜 مواد 130-145 لائحة"
    },
    {
        "keys": ["وفاة", "مات", "جنازة", "منحة"],
        "ans": "عند الوفاة يصرف: نفقات جنازة (3 أشهر معاش)، منحة وفاة (شهر الوفاة + شهرين)، وتعويض إضافي حسب السن.",
        "ref": "⚖️ مادة 33 قانون 148 | 📜 مادة 271 لائحة | 📍 ص 142 دليل"
    },
    {
        "keys": ["زواج", "بنت", "منحة زواج"],
        "ans": "تستحق البنت منحة زواج تعادل معاش شهر عن سنة (12 شهر) بحد أدنى 500 جنيه عند قطع معاشها للزواج.",
        "ref": "⚖️ مادة 105 قانون 148 | 📜 مادة 284 لائحة"
    }
]

# 4. محرك البحث الذكي (نص البحث الخاص بك)
q = st.text_area("اطرح إشكالك القانوني هنا:", placeholder="اكتب سؤالك هنا أو الإشكال القانوني...", height=100)

if st.button("تحليل الإشكالية وعرض الرد 🔍"):
    if q:
        found = False
        for item in LEGAL_DB:
            if any(k in q for k in item["keys"]):
                st.markdown(f"""
                <div class="result-card">
                    <p style="font-size: 1.4rem; line-height: 1.7;"><b>✅ الإجابة:</b><br>{item['ans']}</p>
                    <div class="ref-tag">{item['ref']}</div>
                </div>
                """, unsafe_allow_html=True)
                found = True; break
        if not found: st.error("لم نجد رداً مطابقاً، حاول بكلمات مثل (معاش، وفاة، إصابة).")

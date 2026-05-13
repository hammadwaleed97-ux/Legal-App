import streamlit as st

# 1. إعدادات الصفحة والتنسيق البصري (5 سطور عنوان - 3 سطور توقيع)
st.set_page_config(page_title="مستشار التأمينات والمعاشات", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%); }
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; color: white; }
    .program-title { text-align: center; color: #facc15; font-size: 2.8rem; font-weight: bold; line-height: 1.1; margin-bottom: 10px; }
    .signature-section { text-align: center; font-size: 1.4rem; line-height: 1.5; margin-bottom: 30px; color: #ffffff; font-weight: bold; }
    .result-card { background-color: #ffffff; border-radius: 15px; padding: 25px; color: #1e293b; border-right: 12px solid #facc15; box-shadow: 0 10px 20px rgba(0,0,0,0.3); }
    .ref-style { color: #b91c1c; font-weight: bold; font-size: 0.95rem; margin-top: 15px; display: block; }
    </style>
    """, unsafe_allow_html=True)

# 2. واجهة البرنامج المعتمدة
st.markdown('<div class="program-title">مستشارك<br>في<br>التأمينات<br>و<br>المعاشات</div>', unsafe_allow_html=True)
st.markdown('<div class="signature-section">مع تحيات / وليد حماد<br>الادارة العامة للشؤون القانونية<br>ديوان عام منطقة البحيرة</div>', unsafe_allow_html=True)

# 3. قاعدة البيانات الموسعة (الموسوعة الشاملة)
LEGAL_DB = [
    {
        "keys": ["مبكر", "استقالة", "قبل السن"],
        "ans": "يشترط للمعاش المبكر مدة اشتراك فعلية تعطي معاشاً لا يقل عن 50% من أجر التسوية، وبما لا يقل عن 65% من الحد الأدنى لأجر الاشتراك. المدة 20 سنة فعلية، وتصبح 25 سنة بدءاً من 2025.",
        "ref": "⚖️ مادة 21 قانون 148 | 📜 مادة 102 لائحة | 📍 ص 45 دليل الخدمات"
    },
    {
        "keys": ["إصابة", "حادث", "أثناء العمل", "طريق"],
        "ans": "تعتبر إصابة عمل كل حادث يقع للمؤمن عليه أثناء تأدية عمله أو بسببه، أو في طريق ذهابه وإيابه. يستحق المصاب تعويض أجر بنسبة 100% من أجر الاشتراك طوال مدة عجز الموقت.",
        "ref": "⚖️ مواد 45-51 قانون 148 | 📜 مواد 130-145 لائحة"
    },
    {
        "keys": ["ارملة", "أرملة", "مستحقين", "بنت", "ابن", "والدين"],
        "ans": "يوزع المعاش على المستحقين (الأرملة، الأبناء، البنات، الوالدين، الإخوة) وفقاً للجدول رقم 7 الملحق بالقانون، مع مراعاة قواعد الجمع وشروط الاستحقاق لكل فئة.",
        "ref": "⚖️ مواد 98-108 قانون 148 | 📜 مواد 260-280 لائحة"
    },
    {
        "keys": ["دفعة واحدة", "تعويض", "مدة زائدة"],
        "ans": "يصرف تعويض الدفعة الواحدة في حالات عدم توافر شروط المعاش، ويحسب بنسبة 15% من الأجر السنوي عن كل سنة من سنوات مدة الاشتراك.",
        "ref": "⚖️ مادة 26 قانون 148 | 📜 مادة 115 لائحة"
    },
    {
        "keys": ["زواج", "منحة"],
        "ans": "تستحق البنت أو الأخت منحة زواج تساوي معاش شهر عن سنة (12 شهر) عند قطع المعاش بسبب الزواج، بحد أدنى 500 جنيه.",
        "ref": "⚖️ مادة 105 قانون 148 | 📜 مادة 284 لائحة"
    }
]

# 4. محرك البحث (التزام تام بنصك)
query = st.text_area("اطرح إشكالك القانوني هنا:", placeholder="اكتب سؤالك هنا أو الإشكال القانوني...", height=100)

if st.button("تحليل الإشكالية وعرض الرد 🔍"):
    if query:
        found = False
        for item in LEGAL_DB:
            if any(k in query for k in item["keys"]):
                st.markdown(f"""
                <div class="result-card">
                    <p style="font-size: 1.3rem;"><b>✅ الإجابة:</b><br>{item['ans']}</p>
                    <span class="ref-style">{item['ref']}</span>
                </div>
                """, unsafe_allow_html=True)
                found = True; break
        if not found: st.error("لم نجد إجابة مطابقة، حاول استخدام كلمات مثل (معاش، إصابة، زواج).")

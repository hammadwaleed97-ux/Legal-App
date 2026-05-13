import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="مستشارك في التأمينات والمعاشات", layout="wide")

# 2. التنسيق البصري المعتمد (ثابت كما في الصور)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%); }
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; color: white; }
    .program-title { text-align: center; color: #facc15; font-size: 2.8rem; font-weight: bold; line-height: 1.1; margin-bottom: 15px; }
    .signature-section { text-align: center; font-size: 1.4rem; line-height: 1.5; margin-bottom: 40px; color: #ffffff; font-weight: bold; }
    .result-card { background-color: #ffffff; border-radius: 15px; padding: 25px; color: #1e293b; box-shadow: 0 15px 30px rgba(0,0,0,0.5); border-right: 12px solid #facc15; }
    .stTextArea textarea { font-size: 1.2rem !important; border-radius: 12px !important; border: 2px solid #facc15 !important; text-align: right; }
    .stButton>button { background-color: #facc15; color: #1e3a8a; font-weight: bold; border-radius: 10px; width: 100%; height: 3.5rem; font-size: 1.2rem; }
    </style>
    """, unsafe_allow_html=True)

# 3. قاعدة البيانات القانونية الشاملة (القانون + اللائحة + الدليل)
LEGAL_DB = [
    {
        "keys": ["مبكر", "استقالة", "قبل السن", "بدري", "20 سنة"],
        "ans": "يستحق المعاش المبكر إذا توافرت مدة اشتراك فعلية تعطي معاشاً لا يقل عن 50% من أجر التسوية الأخير، وبما لا يقل عن 65% من الحد الأدنى لأجر الاشتراك. المدة المطلوبة حالياً 20 سنة فعلية، وتصبح 25 سنة في يناير 2025.",
        "docs": "• استمارة 6 تأمينات. • طلب صرف معاش. • بيان تدرج أجور.",
        "guide": "دليل الخدمات - ص 45", "law": "قانون 148 - المادة 21"
    },
    {
        "keys": ["بلوغ السن", "الستين", "60", "شيخوخة", "سن المعاش"],
        "ans": "يستحق معاش الشيخوخة عند بلوغ سن الستين مع توافر مدة اشتراك فعلية لا تقل عن 120 شهراً (10 سنوات)، وتصبح 180 شهراً (15 سنة) اعتباراً من يناير 2025.",
        "docs": "• صورة بطاقة الرقم القومي. • طلب صرف معاش بلوغ سن.",
        "guide": "دليل الخدمات - ص 12", "law": "قانون 148 - المادة 21 بند 1"
    },
    {
        "keys": ["منحة زواج", "بنت", "اتجووزت", "عقد قران", "الزواج"],
        "ans": "تستحق البنت أو الأخت منحة زواج تساوي معاشها المستحق عن شهر واحد مضروباً في 12 شهراً (سنة كاملة) بحد أدنى 500 جنيه، وتصرف لمرة واحدة فقط عند قطع المعاش للزواج.",
        "docs": "• صورة عقد الزواج. • صورة بطاقة الرقم القومي. • طلب صرف المنحة.",
        "guide": "دليل الخدمات - ص 150", "law": "قانون 148 - المادة 105"
    },
    {
        "keys": ["جنازة", "مصاريف جنازة", "توفى", "وفاة"],
        "ans": "تستحق نفقات جنازة بواقع معاش 3 أشهر، تصرف للأرمل أو الأرملة، فإذا لم يوجد صرفت لأرشد الأولاد، فإذا لم يوجد صرفت لمن يثبت قيامه بصرف نفقات الجنازة.",
        "docs": "• شهادة الوفاة. • طلب صرف مصاريف جنازة.",
        "guide": "دليل الخدمات - ص 142", "law": "قانون 148 - المادة 109"
    },
    {
        "keys": ["تجمع", "ارملة", "وفاة الزوج", "مرتب", "معاشين"],
        "ans": "تجمع الأرملة بين معاشها عن زوجها وبين دخلها من العمل أو المهنة دون حدود، كما تجمع بين معاشها الشخصي ومعاش الزوج دون قيود مالية.",
        "docs": "• مفردات مرتب. • بيان معاش. • صورة بطاقة.",
        "guide": "دليل الخدمات - ص 112", "law": "قانون 148 - المادة 102"
    }
]

# 4. الواجهة (العناوين والتوقيع)
st.markdown('<div class="program-title">مستشارك<br>في<br>التأمينات<br>و<br>المعاشات</div>', unsafe_allow_html=True)
st.markdown('<div class="signature-section">مع تحيات / وليد حماد<br>الادارة العامة للشؤون القانونية<br>ديوان عام منطقة البحيرة</div>', unsafe_allow_html=True)
st.divider()

# 5. البحث والرد
if "q_val" not in st.session_state: st.session_state.q_val = ""
u_input = st.text_area("اطرح إشكالك القانوني هنا:", value=st.session_state.q_val, placeholder="اكتب سؤالك هنا أو الإشكال القانوني...", height=100)

c1, c2 = st.columns(2)
with c1:
    if st.button("تحليل الإشكالية وعرض الرد 🔍"):
        if u_input:
            found = False
            for item in LEGAL_DB:
                if any(k in u_input for k in item['keys']):
                    st.markdown(f"""<div class="result-card"><p style="font-size: 1.3rem;"><b>✅ الإجابة:</b><br>{item['ans']}</p><hr><p><b>📄 المستندات:</b> {item['docs']}</p><p style="color:#92400e;">📍 {item['guide']}</p><p style="color:#b91c1c;">⚖️ {item['law']}</p></div>""", unsafe_allow_html=True)
                    found = True; break
            if not found: st.error("لم نجد إجابة مطابقة، حاول بكلمات مثل (زواج، جنازة، سن، معاش).")
        else: st.warning("يرجى كتابة السؤال أولاً.")
with c2:
    if st.button("مسح البحث 🗑️"):
        st.session_state.q_val = ""; st.rerun()

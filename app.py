import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="موسوعة الدفوع القانونية", layout="wide")

# 2. التنسيق الجمالي الرسمي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .defense-header {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
        padding: 35px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        border-bottom: 5px solid #d4af37;
    }
    .defense-card {
        background: #f9f9f9;
        padding: 25px;
        border-right: 10px solid #1e3799;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        height: 70px;
        font-size: 19px;
        font-weight: bold;
        background-color: #ffffff;
        color: #1e3799;
        border: 2px solid #d4af37;
        border-radius: 10px;
    }
    .stButton>button:hover {
        background-color: #d4af37;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. واجهة البرنامج (التوقيع الرسمي)
st.markdown("""
    <div class="defense-header">
        <h1>⚖️ الوجيز في الدفوع القانونية للهيئة</h1>
        <p style='font-size: 20px; font-weight: bold;'>
            مع تحيات وليد حماد <br>
            الادارة العامة للشؤون القانونية - ديوان عام منطقة البحيرة
        </p>
    </div>
    """, unsafe_allow_html=True)

# 4. قاعدة بيانات الدفوع القانونية
legal_defenses = [
    {
        "title": "الدفع بعدم قبول الدعوى لعدم اللجوء للجان الفض",
        "icon": "🚫",
        "defense": "ندفع بعدم قبول الدعوى لرفعها بغير الطريق الذي رسمه القانون لعدم اللجوء للجنة فض المنازعات المنصوص عليها بالمادة 148.",
        "law_article": "148",
        "law_text": "نصت المادة (148) من القانون رقم 148 لسنة 2019 على: 'تنشأ بالهيئة لجان لفض المنازعات الناشئة عن تطبيق أحكام هذا القانون، وتحدد اللائحة التنفيذية لهذا القانون تشكيلها ونظام عملها... ولا يجوز رفع الدعوى قبل مضي ستين يوماً من تاريخ تقديم الطلب للجنة'.",
        "reg_text": "مادة (363) من اللائحة التنفيذية: تلتزم الهيئة بإنشاء لجان فنية وقانونية للنظر في التظلمات قبل اللجوء للقضاء.",
        "tags": ["قبول", "فض منازعات", "إجراءات"]
    },
    {
        "title": "الدفع بسقوط الحق بالتقادم الخمسي",
        "icon": "⏳",
        "defense": "ندفع بسقوط حق المدعي في المطالبة بالمبالغ المتأخرة بالتقادم الخمسي طبقاً للمادة 144.",
        "law_article": "144",
        "law_text": "نصت المادة (144) من القانون على: 'يسقط حق الهيئة في مطالبة صاحب العمل أو المؤمن عليه بالمبالغ المستحقة لها بانقضاء خمس سنوات من تاريخ استحقاقها... كما يسقط حق المؤمن عليه أو المستحقين في المطالبة بالمبالغ المستحقة بانقضاء خمس سنوات من تاريخ الاستحقاق'.",
        "reg_text": "مادة (355) من اللائحة التنفيذية: تحدد إجراءات قطع التقادم عن طريق المطالبة الرسمية أو الكتاب المسجل.",
        "tags": ["تقادم", "خمس سنوات", "سقوط الحق"]
    },
    {
        "title": "الدفع بعدم توافر شروط المعاش المبكر",
        "icon": "🛑",
        "defense": "ندفع برفض الدعوى لعدم توافر مدة الاشتراك الفعلية أو عدم تحقيق نسبة الـ 50% من أجر التسوية الأخير.",
        "law_article": "21 بند 6",
        "law_text": "نصت المادة (21) بند 6 على ضرورة 'توافر مدة اشتراك فعلية تعطي الحق في معاش لا يقل عن 50% من أجر أو دخل التسوية الأخير، وبما لا يقل عن الحد الأدنى للمعاش'.",
        "reg_text": "مادة (102) فقرة (ح) من اللائحة: تشترط وجود مدة اشتراك فعلية لا تقل عن 240 شهراً (ستصبح 300 شهر في 2025).",
        "tags": ["مبكر", "رفض", "شروط"]
    },
    {
        "title": "الدفع بعدم الاختصاص الولائي",
        "icon": "🏛️",
        "defense": "ندفع بعدم اختصاص المحكمة ولائياً بنظر الدعوى لكون النزاع يدخل في اختصاص محاكم القضاء الإداري (مجلس الدولة).",
        "law_article": "أحكام عامة",
        "law_text": "وفقاً لقانون مجلس الدولة، تختص محاكم القضاء الإداري بالفصل في المنازعات المتعلقة بالموظفين العموميين والقرارات الإدارية الصادرة من الهيئة باعتبارها سلطة عامة.",
        "reg_text": "تطبق القواعد العامة للاختصاص القضائي المرتبطة بطبيعة العلاقة الوظيفية (قطاع عام / خاص).",
        "tags": ["اختصاص", "ولائي", "مجلس الدولة"]
    }
]

# 5. محرك البحث عن الدفوع
search_query = st.text_input("🔍 ابحث عن دفع قانوني معين (مثلاً: تقادم، فض منازعات، معاش مبكر)...").strip()

if search_query:
    results = [item for item in legal_defenses if search_query in item['title'] or any(tag in search_query for tag in item['tags'])]
    
    if results:
        for res in results:
            with st.container():
                st.markdown(f"""
                    <div class="defense-card">
                        <h2 style='color: #1e3799;'>{res['icon']} {res['title']}</h2>
                        <p style='font-size: 20px; color: #b21f1f;'><b>💡 الدفع:</b> {res['defense']}</p>
                        <hr>
                        <p style='font-size: 16px;'><b>⚖️ السند القانوني (مادة {res['law_article']}):</b> <br> {res['law_text']}</p>
                        <p style='font-size: 16px; color: #2c3e50;'><b>📄 سند اللائحة:</b> <br> {res['reg_text']}</p>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("لم يتم العثور على هذا الدفع في القاعدة الحالية.")

else:
    # عرض أيقونات الدفوع الرئيسية
    st.markdown("### 🏛️ قائمة الدفوع القانونية الجاهزة:")
    cols = st.columns(2)
    for idx, item in enumerate(legal_defenses):
        with cols[idx % 2]:
            if st.button(f"{item['icon']} {item['title']}", key=idx):
                st.markdown(f"""
                    <div class="defense-card">
                        <h3 style='color: #1e3799;'>{item['title']}</h3>
                        <p style='font-size: 20px; color: #b21f1f;'><b>💡 الدفع:</b> {item['defense']}</p>
                        <hr>
                        <p style='font-size: 17px;'><b>⚖️ نص المادة من القانون:</b> <br> {item['law_text']}</p>
                        <p style='font-size: 17px; color: #2c3e50;'><b>📖 نص المادة من اللائحة:</b> <br> {item['reg_text']}</p>
                    </div>
                """, unsafe_allow_html=True)

st.markdown("---")
st.caption("موسوعة الدفوع القانونية - الإصدار الخاص بالشؤون القانونية - البحيرة 2026")

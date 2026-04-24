import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="الوجيز الذكي في التأمينات والمعاشات", layout="wide")

# 2. التنسيق الجمالي (CSS) لضمان الفخامة وسهولة الاستخدام
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .hero-section {
        background: linear-gradient(135deg, #1e3799, #0984e3);
        color: white;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 25px;
    }
    .law-card {
        background: #ffffff;
        padding: 25px;
        border-right: 10px solid #d4af37;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        height: 80px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 15px;
        border: 2px solid #1e3799;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. واجهة البرنامج (توقيعك الرسمي لمرة واحدة في الأعلى)
st.markdown("""
    <div class="hero-section">
        <h1 style='margin:0;'>📚 الوجيز الذكي في التأمينات والمعاشات</h1>
        <p style='font-size: 22px; font-weight: bold; margin-top:10px;'>
            مع تحيات وليد حماد <br>
            الادارة العامة للشؤون القانونية - ديوان عام منطقة البحيرة
        </p>
    </div>
    """, unsafe_allow_html=True)

# 4. قاعدة البيانات الشاملة للمواضيع (مستخرجة من القانون 148 ولائحته)
legal_db = [
    {
        "title": "تأمين الشيخوخة (المعاش الطبيعي)",
        "icon": "👴",
        "explanation": "شروط استحقاق المعاش عند بلوغ السن القانوني مع توافر مدة اشتراك فعلية.",
        "law_text": "نصت المادة (21) من القانون رقم 148 لسنة 2019 على: 'يستحق المعاش عند بلوغ سن الشيخوخة مع توافر مدة اشتراك في تأمين الشيخوخة والعجز والوفاة لا تقل عن 180 شهراً، منها 120 شهراً فعلية على الأقل'.",
        "reg_ref": "المواد (102-103) من اللائحة التنفيذية.",
        "tags": ["سن", "ستين", "شيخوخة", "معاش"]
    },
    {
        "title": "منحة زواج البنات والأخوات",
        "icon": "💍",
        "explanation": "صرف مبلغ مالي يعادل معاش سنة كاملة للبنت أو الأخت عند زواجها لمرة واحدة.",
        "law_text": "نصت المادة (105) من القانون على: 'في حالة قطع معاش البنت أو الأخت للزواج تصرف لها منحة تساوى معاش سنة بحد أدنى مقدارة خمسمائة جنيه، ولا تصرف هذه المنحة إلا لمرة واحدة'.",
        "reg_ref": "المادة (281) من اللائحة التنفيذية.",
        "tags": ["زواج", "بنت", "أخت", "منحة"]
    },
    {
        "title": "إصابات العمل وحادث الطريق",
        "icon": "🚑",
        "explanation": "حقوق المؤمن عليه في حالة وقوع حادث أثناء العمل أو بسببه أو في الطريق المعتاد.",
        "law_text": "نصت المادة (45) من القانون على: 'إذا حالت الإصابة بين المؤمن عليه وبين أداء عمله، تؤدى الجهة المختصة بصرف تعويض الأجر خلال فترة تخلفه عن عمله بسببها تعويضاً يعادل أجره كاملاً'.",
        "reg_ref": "المواد (155-156) من اللائحة التنفيذية.",
        "tags": ["إصابة", "حادث", "عمل", "طريق"]
    },
    {
        "title": "المعاش المبكر",
        "icon": "⏱️",
        "explanation": "ضوابط إنهاء الخدمة قبل بلوغ سن المعاش والحصول على معاش شهري.",
        "law_text": "نصت المادة (21) بند 6 على: 'توافر مدة اشتراك فعلية تعطي الحق في معاش لا يقل عن 50% من أجر أو دخل التسوية الأخير، وبما لا يقل عن الحد الأدنى للمعاش'.",
        "reg_ref": "المادة (102) فقرة (ح) من اللائحة.",
        "tags": ["مبكر", "استقالة", "تسوية"]
    },
    {
        "title": "تأمين البطالة",
        "icon": "💼",
        "explanation": "صرف تعويض مادي للمؤمن عليه في حالة الفصل من العمل لغير الاستقالة.",
        "law_text": "نصت المادة (85) من القانون على: 'يستحق تعويض البطالة ابتداءً من اليوم الثامن لتاريخ انتهاء الخدمة أو عقد العمل بحسب الأحوال، ويكون التعويض بنسبة 75% من أجر الاشتراك'.",
        "reg_ref": "المادة (233) من اللائحة التنفيذية.",
        "tags": ["بطالة", "فصل", "تعويض"]
    },
    {
        "title": "نظام المكافأة",
        "icon": "💰",
        "explanation": "صرف مبلغ مقطوع عند نهاية الخدمة يمثل حصيلة الاشتراكات المدخرة.",
        "law_text": "نصت المادة (30) من القانون على: 'يستحق المؤمن عليه مكافأة بمبلغ بواقع شهر عن كل سنة من سنوات مدة الاشتراك في هذا التأمين، ويكون أجر حساب المكافأة هو أجر الاشتراك'.",
        "reg_ref": "المادة (119) من اللائحة التنفيذية.",
        "tags": ["مكافأة", "ادخار", "نهاية خدمة"]
    },
    {
        "title": "تأمين المرض",
        "icon": "🤒",
        "explanation": "حق العامل في تعويض الأجر أثناء فترات الإجازة المرضية والعلاج.",
        "law_text": "نصت المادة (76) من القانون على: 'يستحق المؤمن عليه المريض تعويضاً عن الأجر يعادل 75% من أجره اليومي المسدد عنه الاشتراكات لمدة تسعين يوماً، ويزداد إلى 85% للفترات التالية'.",
        "reg_ref": "المادة (210) من اللائحة التنفيذية.",
        "tags": ["مرض", "إجازة", "علاج"]
    }
]

# 5. محرك البحث الذكي (مفعل بالكامل)
search_query = st.text_input("🔍 ابحث عن الموضوع أو المادة (مثلاً: وفاة، إصابة، مكافأة، مادة 105)...").strip()

# 6. منطق البحث والعرض (Logic)
if search_query:
    results = [item for item in legal_db if search_query in item['title'] or search_query in item['law_text'] or any(tag in search_query for tag in item['tags'])]
    
    if results:
        st.markdown(f"#### تم العثور على ({len(results)}) نتيجة:")
        for res in results:
            st.markdown(f"""
                <div class="law-card">
                    <h2 style='color: #1e3799;'>{res['icon']} {res['title']}</h2>
                    <p style='font-size: 18px;'><b>الشرح القانوني:</b> {res['explanation']}</p>
                    <p style='color: #b21f1f; font-weight: bold;'>⚖️ {res['law_text']}</p>
                    <p style='color: #1e3799;'>📖 المرجع: {res['reg_ref']}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("لم يتم العثور على نتائج، حاول البحث بكلمة أخرى.")

else:
    # عرض الأيقونات (الرئيسية) في شبكة منظمة
    st.markdown("### 🌟 اختر القسم المطلوب للاطلاع على نص القانون:")
    cols = st.columns(3)
    for idx, item in enumerate(legal_db):
        with cols[idx % 3]:
            if st.button(f"{item['icon']} {item['title']}", key=idx):
                st.markdown(f"""
                    <div class="law-card">
                        <h3 style='color: #1e3799;'>{item['title']}</h3>
                        <p style='font-size: 18px;'><b>الشرح المبسط للمواطن:</b> {item['explanation']}</p>
                        <hr>
                        <p style='color: #b21f1f; font-weight: bold;'>📄 {item['law_text']}</p>
                        <p style='color: #1e3799;'>📚 مرجع اللائحة: {item['reg_ref']}</p>
                    </div>
                """, unsafe_allow_html=True)

st.markdown("---")
st.caption("الوجيز الذكي - جميع الحقوق محفوظة للإدارة القانونية بالبحيرة 2026")

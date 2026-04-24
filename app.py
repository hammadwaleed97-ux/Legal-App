import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="الوجيز الذكي في التأمينات والمعاشات", layout="wide")

# 2. التنسيق الجمالي (CSS)
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
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 25px;
    }
    .law-card {
        background: #fdfdfd;
        padding: 25px;
        border-right: 10px solid #d4af37;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    .stButton>button {
        width: 100%;
        height: 70px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 12px;
        border: 2px solid #1e3799;
        background-color: white;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1e3799;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. واجهة البرنامج المحدثة
st.markdown("""
    <div class="hero-section">
        <h1>📚 الوجيز الذكي في التأمينات والمعاشات</h1>
        <p style='font-size: 20px;'>
            مع تحيات وليد حماد <br>
            الادارة العامة للشؤون القانونية - ديوان عام منطقة البحيرة
        </p>
    </div>
    """, unsafe_allow_html=True)

# 4. قاعدة البيانات الشاملة (مستخرجة من ملفاتك)
legal_data = [
    {
        "title": "المعاش عند بلوغ السن",
        "icon": "👴",
        "explanation": "يستحق المؤمن عليه معاش الشيخوخة عند بلوغ سن الستين مع توافر مدة اشتراك لا تقل عن 15 سنة فعلية.",
        "law_article": "21",
        "law_text": "نصت المادة (21) من القانون على أن: 'يستحق المعاش عند بلوغ سن الشيخوخة مع توافر مدة اشتراك في تأمين الشيخوخة والعجز والوفاة لا تقل عن 180 شهراً، منها 120 شهراً فعلية على الأقل'.",
        "reg_article": "102",
        "tags": ["سن", "ستين", "معاش", "شيخوخة"]
    },
    {
        "title": "منحة زواج البنت",
        "icon": "💍",
        "explanation": "تصرف للبنت المستحقة للمعاش منحة نقدية عند زواجها لمرة واحدة.",
        "law_article": "105",
        "law_text": "نصت المادة (105) من القانون على أن: 'في حالة قطع معاش البنت أو الأخت للزواج تصرف لها منحة تساوى معاش سنة بحد أدنى مقدارة خمسمائة جنيه، ولا تصرف هذه المنحة إلا لمرة واحدة'.",
        "reg_article": "281",
        "tags": ["زواج", "بنت", "أخت", "منحة"]
    },
    {
        "title": "إصابة العمل",
        "icon": "🚑",
        "explanation": "تغطية كاملة للمصاب أثناء العمل أو بسببه بما في ذلك حوادث الطريق.",
        "law_article": "45",
        "law_text": "نصت المادة (45) من القانون على أن: 'إذا حالت الإصابة بين المؤمن عليه وبين أداء عمله، تؤدى الجهة المختصة بصرف تعويض الأجر خلال فترة تخلفه عن عمله بسببها تعويضاً يعادل أجره كاملاً'.",
        "reg_article": "155",
        "tags": ["إصابة", "حادث", "عمل", "طريق"]
    },
    {
        "title": "المعاش المبكر",
        "icon": "⏱️",
        "explanation": "الخروج للمعاش قبل السن القانوني وفق ضوابط حسابية محددة.",
        "law_article": "21 بند 6",
        "law_text": "نصت المادة (21) بند 6 على توافر مدة اشتراك فعلية تعطي الحق في معاش لا يقل عن 50% من أجر أو دخل التسوية الأخير، وبما لا يقل عن الحد الأدنى للمعاش.",
        "reg_article": "102 فقرة ح",
        "tags": ["مبكر", "استقالة", "تسوية"]
    }
]

# 5. تفعيل محرك البحث
search_query = st.text_input("🔍 ابحث عن الموضوع (اكتب مثلاً: زواج، سن، إصابة)...", "")

# 6. منطق العرض (Search Logic)
if search_query:
    results = [item for item in legal_data if search_query in item['title'] or any(tag in search_query for tag in item['tags'])]
    
    if results:
        for res in results:
            st.markdown(f"""
                <div class="law-card">
                    <h2 style='color: #1e3799;'>{res['icon']} {res['title']}</h2>
                    <p style='font-size: 18px;'><b>الشرح المبسط:</b> {res['explanation']}</p>
                    <p style='color: #d4af37; font-weight: bold;'>{res['law_text']}</p>
                    <p style='font-size: 14px; color: #7f8c8d;'>المرجع: مادة {res['law_article']} من القانون | مادة {res['reg_article']} من اللائحة</p>
                </div>
            """, unsafe_allow_html=True)
    else

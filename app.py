import streamlit as st

# 1. إعدادات الصفحة الرسمية
st.set_page_config(page_title="الوجيز الذكي في التأمينات والمعاشات", layout="wide")

# 2. التنسيق الجمالي الاحترافي (CSS)
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
        margin-bottom: 30px;
    }
    .law-card {
        background: #ffffff;
        padding: 25px;
        border-right: 10px solid #d4af37;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin-top: 15px;
        border: 1px solid #eee;
    }
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 12px;
        border: 2px solid #1e3799;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. واجهة البرنامج (تعديل العنوان والتوقيع حسب طلبك)
st.markdown("""
    <div class="hero-section">
        <h1 style='margin-bottom:10px;'>📚 الوجيز الذكي في التأمينات والمعاشات</h1>
        <p style='font-size: 22px; font-weight: bold;'>مع تحيات وليد حماد</p>
        <p style='font-size: 18px;'>الادارة العامة للشؤون القانونية - ديوان عام منطقة البحيرة</p>
    </div>
    """, unsafe_allow_html=True)

# 4. قاعدة البيانات الشاملة (نصوص حقيقية من الملفات)
legal_db = [
    {
        "title": "معاش الشيخوخة (السن القانوني)",
        "icon": "👴",
        "explanation": "استحقاق المعاش عند بلوغ سن الستين مع توافر مدة اشتراك كافية.",
        "full_text": "نصت المادة (21) من القانون رقم 148 لسنة 2019 على أن: 'يستحق المعاش عند بلوغ سن الشيخوخة مع توافر مدة اشتراك في تأمين الشيخوخة والعجز والوفاة لا تقل عن 180 شهراً منها 120 شهراً فعلية على الأقل'.",
        "reg_text": "مادة (102) من اللائحة التنفيذية: تفصل مدد الاشتراك الفعلية والمشتراة وقواعد حسابها.",
        "tags": ["سن", "ستين", "شيخوخة", "معاش"]
    },
    {
        "title": "منحة زواج البنات والأخوات",
        "icon": "💍",
        "explanation": "دعم نقدي يصرف لمرة واحدة عند زواج البنت المستحقة للمعاش.",
        "full_text": "نصت المادة (105) من القانون رقم 148 لسنة 2019 على أن: 'في حالة قطع معاش البنت أو الأخت للزواج تصرف لها منحة تساوى معاش سنة بحد أدنى مقدارة خمسمائة جنيه، ولا تصرف هذه المنحة إلا لمرة واحدة'.",
        "reg_text": "مادة (281) من اللائحة التنفيذية: تلتزم الهيئة بصرف المنحة بناءً على تقديم وثيقة الزواج الرسمية.",
        "tags": ["زواج", "بنت", "أخت", "فرح", "منحة"]
    },
    {
        "title": "إصابة العمل وحادث الطريق",
        "icon": "🚑",
        "explanation": "حقوق العامل عند تعرضه لحادث أثناء العمل أو في طريقه إليه.",
        "full_text": "نصت المادة (45) من القانون رقم 148 لسنة 2019 على أن: 'إذا حالت الإصابة بين المؤمن عليه وبين أداء عمله، تؤدى الجهة المختصة بصرف تعويض الأجر خلال فترة تخلفه عن عمله بسببها تعويضاً يعادل أجره كاملاً'.",
        "reg_text": "مادة (155) من اللائحة التنفيذية: يعتبر في حكم إصابة العمل الحادث الذي يقع للمؤمن عليه خلال فترة ذهابه لمباشرة عمله أو عودته منه.",
        "tags": ["إصابة", "حادث", "عمل", "طريق", "تعويض"]
    },
    {
        "title": "المعاش المبكر (الاستقالة)",
        "icon": "⏱️",
        "explanation": "ضوابط الخروج للمعاش قبل السن القانوني.",
        "full_text": "نصت المادة (21) بند (6) على: 'توافر مدة اشتراك فعلي تعطي الحق في معاش لا يقل عن 50% من أجر أو دخل التسوية الأخير، وبما لا يقل عن الحد الأدنى للمعاش المشار إليه بالمادة 24'.",
        "reg_text": "مادة (102) فقرة (ح) من اللائحة: تشترط ألا يقل المعاش عن 65% من الحد الأدنى لأجر الاشتراك في تاريخ استحقاق المعاش.",
        "tags": ["مبكر", "استقالة", "تسوية", "خروج"]
    }
]

# 5. تفعيل محرك البحث البرمجي
search_query = st.text_input("🔍 ابحث عن أي موضوع (اكتب مثلاً: زواج، سن، إصابة، استقالة)...").strip()

# 6. منطق البحث والعرض (Logic)
if search_query:
    # فلترة النتائج بناءً على العنوان أو الكلمات الدلالية
    results = [item for item in legal_db if search_query in item['title'] or any(tag in search_query for tag in item['tags'])]
    
    if results:
        st.markdown(f"#### نتائج البحث عن: {search_query}")
        for res in results:
            with st.container():
                st.markdown(f"""
                    <div class="law-card">
                        <h2 style='color: #1e3799;'>{res['icon']} {res['title']}</h2>
                        <p style='font-size: 18px;'><b>الشرح المبسط:</b> {res['explanation']}</p>
                        <p style='color: #b21f1f; font-weight: bold;'>📄 {res['full_text']}</p>
                        <p style='color: #1e3799;'>📚 {res['reg_text']}</p>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("عذراً، لم يتم العثور على نتائج لهذه الكلمة. حاول البحث بكلمات أبسط.")

else:
    # العرض الافتراضي للأقسام
    st.markdown("### 🌟 تصفح الأقسام الرئيسية:")
    cols = st.columns(2)
    for idx, item in enumerate(legal_db):
        with cols[idx % 2]:
            if st.button(f"{item['icon']} {item['title']}", key=idx):
                st.markdown(f"""
                    <div class="law-card">
                        <h3 style='color: #1e3799;'>{item['title']}</h3>
                        <p style='font-size: 18px;'><b>الشرح:</b> {item['explanation']}</p>
                        <p style='color: #b21f1f; font-weight: bold;'>⚖️ {item['full_text']}</p>
                        <p style='color: #1e3799;'>📖 {item['reg_text']}</p>
                    </div>
                """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>الوجيز الذكي - الإصدار القانوني المعتمد 2026</p>", unsafe_allow_html=True)

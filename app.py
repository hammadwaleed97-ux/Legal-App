import streamlit as st

# 1. إعدادات الصفحة الرسمية
st.set_page_config(page_title="الوجيز الذكي في التأمينات والمعاشات", layout="wide", page_icon="⚖️")

# 2. تصميم الواجهة (CSS) لتظهر بشكل فخم
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    /* تصميم الهيدر (العنوان) */
    .header-box {
        background: linear-gradient(135deg, #1e3799 0%, #0984e3 100%);
        color: white;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        margin-bottom: 40px;
    }
    
    /* تصميم الأزرار التفاعلية */
    .stButton>button {
        width: 100%;
        height: 100px;
        background-color: #ffffff;
        color: #2c3e50;
        border: 2px solid #d4af37; /* ذهبي */
        border-radius: 15px;
        font-size: 20px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton>button:hover {
        background-color: #d4af37;
        color: white;
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. واجهة البرنامج (Header)
st.markdown("""
    <div class="header-box">
        <h1 style='margin:0;'>📚 الوجيز الذكي في التأمينات والمعاشات</h1>
        <p style='font-size: 22px; margin-top:10px;'>موسوعة قانون 148 لسنة 2019 واللائحة التنفيذية</p>
        <p style='font-size: 16px; opacity: 0.9;'>تبسيط القانون.. حماية للحقوق</p>
    </div>
    """, unsafe_allow_html=True)

# 4. محرك البحث الذكي
st.markdown("### 🔍 ابحث في الموسوعة:")
search_query = st.text_input("", placeholder="اكتب كلمة للبحث (مثلاً: وفاة، زواج، إصابة، اشتراك)...")

# 5. قاعدة البيانات المرتبطة بملفاتك
legal_content = [
    {
        "title": "المعاش عند بلوغ السن",
        "icon": "👴",
        "explanation": "يستحق المعاش عند بلوغ سن الستين مع توافر مدة اشتراك لا تقل عن 180 شهراً (15 سنة) فعلياً. (تزيد لـ 20 سنة في 2025).",
        "law_ref": "مادة (21) من القانون",
        "reg_ref": "مادة (102) من اللائحة",
        "tags": ["سن", "ستين", "شيخوخة", "مدة"]
    },
    {
        "title": "منحة الزواج (بنت/أخت)",
        "icon": "💍",
        "explanation": "تصرف منحة زواج للبنت أو الأخت المستحقة للمعاش عند زواجها، قيمتها (معاش سنة) بحد أدنى 500 جنيه، وتصرف لمرة واحدة.",
        "law_ref": "مادة (105) من القانون",
        "reg_ref": "مادة (281) من اللائحة",
        "tags": ["بنت", "زواج", "أخت", "منحة"]
    },
    {
        "title": "إصابة العمل وحادث الطريق",
        "icon": "🚑",
        "explanation": "تشمل الحوادث أثناء العمل أو بسببه أو في الطريق الطبيعي للعمل. يستحق المصاب تعويض أجر يعادل 100% من أجره.",
        "law_ref": "مادة (45) من القانون",
        "reg_ref": "مادة (155) من اللائحة",
        "tags": ["إصابة", "حادث", "طريق", "علاج"]
    },
    {
        "title": "المعاش المبكر",
        "icon": "⏱️",
        "explanation": "يتطلب مدة اشتراك تعطي معاشاً لا يقل عن 50% من آخر أجر تسوية، وبمدة اشتراك فعلية لا تقل عن 20 سنة (تصبح 25 سنة في 2025).",
        "law_ref": "مادة (21) بند 6",
        "reg_ref": "مادة (102) فقرة ح",
        "tags": ["مبكر", "استقالة", "تسوية"]
    }
]

# 6. منطق عرض النتائج
if search_query:
    results = [item for item in legal_content if any(tag in search_query for tag in item['tags']) or search_query in item['title']]
    if results:
        for res in results:
            with

import streamlit as st

# 1. إعدادات الصفحة والاسم المختار
st.set_page_config(page_title="الوجيز الذكي في التأمينات والمعاشات", layout="wide")

# 2. لمسة الفخامة (CSS) لعمل واجهة تشبه التطبيقات العالمية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    /* الهيدر الفخم */
    .hero-section {
        background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
        color: white;
        padding: 50px 20px;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    /* تصميم البطاقات الذكية */
    .law-card {
        background: white;
        padding: 20px;
        border-right: 8px solid #d4af37;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        transition: 0.3s;
    }
    .law-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    .stButton>button {
        width: 100%;
        background-color: #f8f9fa;
        border: 2px solid #1a2a6c;
        border-radius: 15px;
        height: 60px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. العنوان الرئيسي الجذاب
st.markdown("""
    <div class="hero-section">
        <h1 style='font-size: 45px;'>📚 الوجيز الذكي في التأمينات والمعاشات</h1>
        <p style='font-size: 20px;'>كل ما يهم المواطن في قانون 148 ولائحته التنفيذية ببساطة ووضوح</p>
    </div>
    """, unsafe_allow_html=True)

# 4. محرك البحث الذكي (يظهر بوضوح في المنتصف)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    search_query = st.text_input("🔍 ابحث هنا عن أي موضوع (مثلاً: تعويض، وفاة، عجز، أرملة)...")

# 5. عرض المواضيع (الأيقونات)
st.markdown("### 🌟 تصفح أهم المواضيع:")
topics = [
    {"title": "المعاش الأساسي", "icon": "👴", "text": "شروط استحقاق معاش الشيخوخة ومدد الاشتراك المطلوبة."},
    {"title": "منح الورثة", "icon": "🎁", "text": "منحة الجنازة، منحة الموت، ومنحة زواج البنات."},
    {"title": "إصابة العمل", "icon": "🚑", "text": "حقوق المصاب وحالات حادث الطريق وتعويض الأجر."},
    {"title": "المستحقين", "icon": "👨‍👩‍👧", "text": "قواعد توزيع المعاش بين الأرامل والأبناء والوالدين."}
]

cols = st.columns(4)
for i, topic in enumerate(topics):
    with cols[i]:
        if st.button(f"{topic['icon']} {topic['title']}"):
            st.info(f"**{topic['title']}:** {topic['text']}")

# 6. منطق عرض "الشرح + المواد" (كما طلبت)
st.markdown("---")
if search_query:
    # هنا يتم البحث (مثال توضيحي)
    st.markdown(f"#### نتائج البحث عن '{search_query}':")
    # محاكاة لنتيجة بحث
    st.markdown(f"""
        <div class="law-card">
            <h3>📌 شرح مبسط:</h3>
            <p style='font-size: 18px;'>حقوقك التأمينية في هذا الموضوع تشمل كذا وكذا...</p>
            <hr>
            <p style='color: #b21f1f;'><b>⚖️ المادة الحاكمة:</b> مادة (123) من القانون 148 لسنة 2019</p>
            <p style='color: #1a2a6c;'><b>📄 نص اللائحة:</b> مادة (456) من اللائحة التنفيذية</p>
        </div>
    """, unsafe_allow_html=True)

# 7. الفوتر الفخم (التوقيع الرسمي)
st.markdown("""
    <div style='text-align: center; margin-top: 50px; padding: 20px; border-top: 2px solid #eee;'>
        <p style='color: #1a2a6c; font-size: 18px; font-weight: bold;'>تحيات الإدارة العامة للشئون القانونية</p>
        <p style='color: #d4af37; font-size: 20px; font-weight: bold;'>وليد حماد</p>
        <p style='color: #7f8c8d;'>منطقة البحيرة - الهيئة القومية للتأمين الاجتماعي</p>
    </div>
    """, unsafe_allow_html=True)

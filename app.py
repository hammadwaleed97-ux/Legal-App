import streamlit as st

# 1. إعدادات الصفحة الرسمية
st.set_page_config(page_title="الوجيز في الدفوع القانونية", layout="wide")

# 2. التنسيق الجمالي الرسمي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .hero-section {
        background: #1a2a6c;
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        border-bottom: 5px solid #d4af37;
    }
    .defense-box {
        background: #ffffff;
        padding: 25px;
        border: 1px solid #d1d1d1;
        border-right: 12px solid #b21f1f;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    .section-title { color: #1e3799; font-weight: bold; margin-top: 10px; border-bottom: 1px solid #eee; }
    .law-text { color: #b21f1f; font-style: italic; background: #fff5f5; padding: 10px; border-radius: 5px; }
    .explanation-text { color: #2c3e50; font-weight: bold; background: #f0f2f6; padding: 15px; border-right: 5px solid #27ae60; }
    </style>
    """, unsafe_allow_html=True)

# 3. واجهة البرنامج (توقيعك الرسمي)
st.markdown("""
    <div class="hero-section">
        <h1 style='margin:0;'>⚖️ الوجيز في الدفوع القانونية للهيئة</h1>
        <p style='font-size: 22px; font-weight: bold; margin-top:10px;'>
            مع تحيات وليد حماد <br>
            الادارة العامة للشؤون القانونية - ديوان عام منطقة البحيرة
        </p>
    </div>
    """, unsafe_allow_html=True)

# 4. قاعدة بيانات الدفوع (نصوص منضبطة من القانون واللائحة)
defense_db = [
    {
        "id": 1,
        "title": "الدفع بعدم قبول الدعوى لعدم اللجوء للجان فض المنازعات",
        "defense_statement": "ندفع بعدم قبول الدعوى لرفعها بغير الطريق الذى رسمه القانون لعدم اللجوء إلى لجان فض المنازعات المنصوص عليها بالمادة (148) من القانون 148 لسنة 2019.",
        "law_article": "المادة (148) من القانون:",
        "law_content": "تنشأ بالهيئة لجان لفض المنازعات الناشئة عن تطبيق أحكام هذا القانون... ولا يجوز رفع الدعوى قبل مضى ستين يوماً من تاريخ تقديم الطلب للجنة المشار إليها.",
        "reg_article": "المادة (363) من اللائحة:",
        "reg_content": "تنشأ لجنة أو أكثر بقرار من رئيس الهيئة لفض المنازعات... ويجب على أصحاب الشأن تقديم طلب تظلم للجنة قبل اللجوء للقضاء.",
        "commentary": "وترتيباً على ما تقدم؛ ولما كان المدعي قد أقام دعواه الماثلة دون الولوج إلى لجنة فض المنازعات المختصة، الأمر الذي يضحي معه قد خالف إجراءً جوهرياً رسمه القانون، مما يتعين معه على عدالة المحكمة الموقرة القضاء بعدم قبول الدعوى لرفعها بغير الطريق الذي رسمه القانون.",
        "tags": ["قبول", "فض", "إجراءات"]
    },
    {
        "id": 2,
        "title": "الدفع بسقوط الحق بالتقادم الخمسي",
        "defense_statement": "ندفع بسقوط حق المدعي في المطالبة بالمبالغ المتنازع عليها لمضي أكثر من خمس سنوات (التقادم الخمسي).",
        "law_article": "المادة (144) من القانون:",
        "law_content": "يسقط حق المؤمن عليه أو المستحقين في المطالبة بالمبالغ المستحقة بانقضاء خمس سنوات من تاريخ الاستحقاق.",
        "reg_article": "المادة (355) من اللائحة:",
        "reg_content": "ينقطع سريان مدة التقادم بالمطالبة بالحق بكتاب مسجل مصحوب بعلم الوصول أو بأي وسيلة من وسائل الإخطار القانونية.",
        "commentary": "وترتيباً على ما تقدم؛ يتضح لعدالة المحكمة الموقرة أن الحق المطالب به قد انقضى عليه أكثر من خمس سنوات دون وجود عذر قانوني أو مانع يحول دون المطالبة به، ولما كانت نصوص القانون صريحة في تقرير السقوط بالتقادم الخمسي، فإننا نلتمس القضاء بسقوط الحق بالتقادم.",
        "tags": ["تقادم", "سقوط", "خمس سنوات"]
    }
]

# 5. محرك البحث
query = st.text_input("🔍 ابحث عن الدفع المناسب لدعواك...")

# 6. منطق العرض
def display_defense(item):
    st.markdown(f"""
        <div class="defense-box">
            <h2 style='color: #1a2a6c;'>📌 {item['title']}</h2>
            <p style='font-size: 20px; color: #b21f1f; font-weight: bold;'>[ نص الدفع ]: {item['defense_statement']}</p>
            
            <div class="section-title">⚖️ أولاً: من القانون</div>
            <p class="law-text"><b>{item['law_article']}</b><br>{item['law_content']}</p>
            
            <div class="section-title">📜 ثانياً: من اللائحة التنفيذية</div>
            <p class="law-text"><b>{item['reg_article']}</b><br>{item['reg_content']}</p>
            
            <div class="section-title">🖋️ ثالثاً: التعقيب القانوني (الصياغة)</div>
            <div class="explanation-text">{item['commentary']}</div>
        </div>
    """, unsafe_allow_html=True)

if query:
    results = [i for i in defense_db if query in i['title'] or any(t in query for t in i['tags'])]
    for res in results:
        display_defense(res)
else:
    # عرض القائمة كأزرار أيقونية
    cols = st.columns(2)
    for idx, item in enumerate(defense_db):
        with cols[idx % 2]:
            if st.button(f"🔎 {item['title']}"):
                display_defense(item)

st.markdown("---")
st.caption("برنامج الدفوع القانونية المطور - نسخة الإدارة القانونية بالبحيرة")

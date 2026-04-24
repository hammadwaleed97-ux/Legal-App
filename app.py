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
        "tags": ["تقادم", "

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
        "law_text": "نصت المادة (105) من القانون على: 'في حالة قطع معاش البنت أو الأخت للزواج تصرف لها منحة تساوى معاش سنة

import streamlit as st
import json

# إعدادات الصفحة
st.set_page_config(page_title="المستشار القانوني الذكي - وليد حماد", layout="centered")

# تنسيق الواجهة (CSS) لجعل خانة السؤال والإجابة واضحة وكبيرة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .stTextArea textarea { font-size: 1.2rem !important; text-align: right; border: 2px solid #1e3a8a !important; }
    .answer-box { background-color: #f8fafc; border: 2px solid #e2e8f0; padding: 25px; border-radius: 15px; margin-top: 20px; text-align: right; min-height: 200px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); }
    .signature { text-align: center; color: #64748b; margin-top: 50px; font-weight: bold; }
    .stButton>button { width: 100%; background-color: #1e3a8a; color: white; height: 3rem; font-size: 1.2rem; }
    </style>
    """, unsafe_allow_html=True)

# رأس البرنامج
st.markdown("<h2 style='text-align: center; color: #1e3a8a;'>⚖️ محرك البحث القانوني المتخصص</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>قانون التأمينات الاجتماعية والمعاشات رقم 148 لسنة 2019 ولائحته التنفيذية</p>", unsafe_allow_html=True)

# وظيفة البحث في قاعدة البيانات الداخلية
def search_legal_db(query):
    # هنا يتم استيراد البيانات من ملف JSON (الذي سننشئه بالأسفل)
    try:
        with open('legal_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return "خطأ: قاعدة البيانات غير موجودة. تأكد من وجود ملف legal_data.json"

    query = query.lower()
    results = []
    
    for item in data:
        # البحث في السؤال، الإجابة، أو رقم المادة
        if query in item['question'].lower() or query in item['answer'].lower() or query in item['article']:
            res = f"<b>📌 المادة ({item['article']}): {item['question']}</b><br><br>"
            res += f"<b>✅ الإجابة القانونية:</b><br>{item['answer']}<br><br>"
            res += f"<b>📄 المستندات المطلوبة:</b><br>{item['documents']}<br><br>"
            res += f"<b>⚖️ السند:</b> {item['basis']}<br><hr>"
            results.append(res)
    
    if not results:
        return "عذراً، لم أجد نصاً مطابقاً في القانون أو اللائحة. حاول كتابة كلمات مفتاحية أخرى (مثل: أرملة، عجز، إصابة، مادة 102)."
    
    return "".join(results)

# واجهة المستخدم (الخانات المطلوبة)
st.markdown("### 🔍 اطرح تساؤلك القانوني:")
user_query = st.text_area("", placeholder="اكتب سؤالك هنا أو رقم المادة... مثال: ما هي شروط المعاش المبكر؟", height=150)

if st.button("عرض الإجابة القانونية ↩️"):
    if user_query:
        with st.spinner('جاري فحص مواد القانون واللائحة...'):
            answer = search_legal_db(user_query)
            st.markdown("### 📝 الإجابة:")
            st.markdown(f'<div class="answer-box">{answer}</div>', unsafe_allow_html=True)
    else:
        st.warning("من فضلك اكتب سؤالاً أولاً.")

# التوقيع
st.markdown(f"""
    <div class="signature">
        مع تحيات وليد حماد<br>
        الادارة العامة للشئون القانونية - ديوان عام منطقة البحيرة
    </div>
    """, unsafe_allow_html=True)

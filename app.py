import streamlit as st

# 1. إعدادات الصفحة والخطوط
st.set_page_config(page_title="المستشار القانوني الذكي - وليد حماد", layout="centered")

# 2. تنسيق الواجهة (CSS) لتصميم يليق بالإدارة القانونية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .stTextArea textarea { font-size: 1.3rem !important; text-align: right; border: 2px solid #1e3a8a !important; border-radius: 12px; background-color: #fcfcfc; }
    .stButton>button { width: 100%; background-color: #1e3a8a; color: white; height: 3.5rem; font-size: 1.3rem; font-weight: bold; border-radius: 12px; transition: 0.3s; }
    .stButton>button:hover { background-color: #2563eb; border: 1px solid #1e3a8a; }
    .answer-card { background-color: #ffffff; border: 1px solid #e2e8f0; padding: 25px; border-radius: 18px; margin-top: 20px; text-align: right; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }
    .article-tag { background-color: #facc15; color: #1e3a8a; padding: 5px 15px; border-radius: 20px; font-weight: bold; font-size: 0.9rem; }
    .doc-box { background-color: #f0fdf4; border-right: 5px solid #22c55e; padding: 15px; margin-top: 15px; border-radius: 8px; }
    .footer { text-align: center; color: #64748b; margin-top: 50px; font-size: 1rem; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

# 3. قاعدة البيانات الداخلية (مدمجة بالكامل لضمان الدقة والشمولية)
# أضفت لك هنا أهم مواد القانون واللائحة التي تغطي أغلب التساؤلات
LEGAL_DATA = [
    {
        "keywords": ["معاش مبكر", "المبكر", "استقالة", "خروج"],
        "article": "21",
        "question": "ما هي شروط استحقاق المعاش المبكر؟",
        "answer": "يشترط لاستحقاق المعاش المبكر: 1- توافر مدة اشتراك فعلية تعطي الحق في معاش لا يقل عن 50% من أجر التسوية الأخير. 2- ألا يقل المعاش عن 65% من الحد الأدنى لأجر الاشتراك في تاريخ الاستحقاق. 3- توفر مدة اشتراك فعلية لا تقل عن 240 شهراً (تصبح 300 شهر فعلية بدءاً من 1/1/2025).",
        "documents": "طلب صرف (نموذج 20)، بيان تدرج أجور معتمد، بيان مدد اشتراك.",
        "basis": "المادة (21) من قانون 148 لسنة 2019 والمادة (102) من اللائحة التنفيذية."
    },
    {
        "keywords": ["أرملة", "جمع", "زوج", "زوجة", "بين معاشين"],
        "article": "102",
        "question": "قواعد الجمع بين المعاشات للأرملة",
        "answer": "تجمع الأرملة بين معاشها عن زوجها وبين معاشها بصفتها مؤمناً عليها دون حدود، كما تجمع بين معاشها عن زوجها وبين دخلها من العمل أو المهنة دون حدود.",
        "documents": "صورة بطاقة الرقم القومي، بيان مفردات مرتب (إذا كانت تعمل)، بيان معاش.",
        "basis": "المادة (102) من قانون 148 لسنة 2019."
    },
    {
        "keywords": ["إصابة", "عمل", "طريق", "حادث", "عجز"],
        "article": "45",
        "question": "تعويض إصابة العمل وحادث الطريق",
        "answer": "تعتبر إصابة عمل كل حادث يقع للمؤمن عليه أثناء العمل أو بسببه، أو في طريقه الطبيعي للعمل. يستحق المصاب تعويض أجر يعادل 100% من أجره طوال فترة عجزه عن العمل.",
        "documents": "نموذج (51) إخطار إصابة، محضر شرطة معاينة الحادث (للطريق)، قرار التأمين الصحي.",
        "basis": "المواد (1، 45) من قانون 148 لسنة 2019."
    },
    {
        "keywords": ["زواج", "بنت", "ابنة", "أخت", "منحة"],
        "article": "105",
        "question": "شروط وقيمة منحة الزواج",
        "answer": "تستحق الابنة أو الأخت في حالة قطع المعاش للزواج منحة تساوي معاش سنة، بحد أدنى 500 جنيه. تصرف لمرة واحدة فقط وتسقط إذا لم تقدم خلال 5 سنوات.",
        "documents": "صورة عقد الزواج، بطاقة الرقم القومي سارية، نموذج (21) طلب صرف.",
        "basis": "المادة (105) من قانون 148 لسنة 2019 والمادة (268) من اللائحة."
    },
    {
        "keywords": ["تظلم", "فحص منازعات", "شكوى", "طعن"],
        "article": "148",
        "question": "إجراءات التظلم من قرارات الهيئة",
        "answer": "يجب على صاحب الشأن قبل اللجوء للقضاء تقديم طلب تظلم إلى لجان فحص المنازعات بالهيئة. وعلى اللجنة الفصل في التظلم خلال 60 يوماً من تاريخ تقديمه.",
        "documents": "طلب تظلم مسبب، صورة القرار المتظلم منه، توكيل إن وجد.",
        "basis": "المادة (148) من قانون 148 لسنة 2019."
    }
]

# 4. بناء واجهة المستخدم
st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>⚖️ المستشار القانوني المتخصص</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1rem;'>قانون التأمينات الاجتماعية والمعاشات رقم 148 لسنة 2019 ولائحته</p>", unsafe_allow_html=True)
st.divider()

# خانة السؤال الكبيرة
st.markdown("### 🔍 اطرح تساؤلك القانوني:")
user_query = st.text_area("", placeholder="مثلاً: ما هي شروط المعاش المبكر؟ أو ابحث برقم المادة...", height=150)

if st.button("عرض الإجابة القانونية ↩️"):
    if user_query:
        # منطق البحث الذكي بالكلمات المفتاحية
        found = False
        query_clean = user_query.lower()
        
        for item in LEGAL_DATA:
            # البحث في الكلمات المفتاحية أو رقم المادة أو السؤال
            if any(key in query_clean for key in item['keywords']) or item['article'] in query_clean:
                st.markdown(f"""
                <div class="answer-card">
                    <span class="article-tag">مادة {item['article']}</span>
                    <h3 style="color: #1e3a8a; margin-top: 15px;">{item['question']}</h3>
                    <p style="font-size: 1.15rem; color: #334155;"><b>✅ الإجابة القانونية:</b><br>{item['answer']}</p>
                    <div class="doc-box">
                        <b>📄 المستندات المطلوبة (حسب دليل الخدمات):</b><br>{item['documents']}
                    </div>
                    <p style="color: #991b1b; font-weight: bold; margin-top: 15px;">⚖️ السند: {item['basis']}</p>
                </div>
                """, unsafe_allow_html=True)
                found = True
        
        if not found:
            st.error("عذراً، لم أجد إجابة دقيقة لهذا السؤال حالياً. جرب البحث بكلمات أبسط مثل (معاش، إصابة، زواج، تظلم).")
    else:
        st.warning("يرجى كتابة السؤال أولاً في الخانة المخصصة.")

# 5. التوقيع النهائي
st.markdown(f"""
    <div class="footer">
        ---<br>
        مع تحيات وليد حماد<br>
        الادارة العامة للشئون القانونية - ديوان عام منطقة البحيرة
    </div>
    """, unsafe_allow_html=True)

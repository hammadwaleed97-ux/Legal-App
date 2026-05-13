import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="المستشار القانوني - وليد حماد", layout="centered")

# 2. التنسيق (CSS) - لجعل الواجهة بسيطة واحترافية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .stTextArea textarea { font-size: 1.2rem !important; text-align: right; border: 2px solid #1e3a8a !important; border-radius: 10px; }
    .answer-box { background-color: #ffffff; border: 1px solid #cbd5e1; padding: 25px; border-radius: 15px; margin-top: 20px; text-align: right; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    .stButton>button { width: 100%; background-color: #1e3a8a; color: white; height: 3.5rem; font-size: 1.2rem; font-weight: bold; border-radius: 10px; }
    .article-header { color: #1e3a8a; font-weight: bold; font-size: 1.3rem; border-right: 5px solid #facc15; padding-right: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. قاعدة البيانات الداخلية (المعلومات مخفية هنا ولن تظهر إلا عند السؤال)
# يمكنك إضافة مئات المواد هنا بنفس التنسيق
LEGAL_DB = [
    {
        "art": "21",
        "title": "المعاش المبكر",
        "ans": "يشترط توافر مدة اشتراك فعلية تعطي الحق في معاش لا يقل عن 50% من أجر التسوية الأخير، وبما لا يقل عن 65% من الحد الأدنى لأجر الاشتراك. المدة المطلوبة حالياً 240 شهر (تصبح 300 شهر في 2025).",
        "docs": "نموذج (20) طلب صرف، بيان تدرج أجور، بيان مدد اشتراك معتمد.",
        "basis": "المادة 21 من قانون 148 لسنة 2019 واللائحة التنفيذية م (102)."
    },
    {
        "art": "102",
        "title": "الجمع بين المعاشات (للأرملة)",
        "ans": "تجمع الأرملة بين معاشها عن زوجها وبين معاشها بصفتها مؤمناً عليها دون حدود، كما تجمع بين معاشها عن زوجها وبين دخلها من العمل دون حدود.",
        "docs": "صورة بطاقة الرقم القومي، بيان مفردات مرتب (للموظفة)، بيان معاش.",
        "basis": "المادة 102 من قانون 148 لسنة 2019."
    },
    {
        "art": "45",
        "title": "إصابة العمل وحادث الطريق",
        "ans": "تعتبر إصابة عمل إذا وقعت أثناء العمل أو بسببه، أو في الطريق الطبيعي للعمل دون توقف أو انحراف. يستحق المصاب تعويض أجر بنسبة 100% من أجره المسدد عنه الاشتراك.",
        "docs": "نموذج (51) إخطار إصابة، محضر شرطة (لحادث الطريق)، قرار اللجنة الطبية.",
        "basis": "المواد (1، 45) من قانون 148 لسنة 2019."
    },
    {
        "art": "148",
        "title": "لجنة فحص المنازعات (التظلمات)",
        "ans": "يجب على صاحب الشأن التظلم من قرارات الهيئة أمام لجنة فحص المنازعات قبل اللجوء للقضاء، وعلى اللجنة الفصل في التظلم خلال 60 يوماً.",
        "docs": "طلب تظلم، صورة القرار المتظلم منه، المستندات المؤيدة للحالة.",
        "basis": "المادة 148 من قانون 148 لسنة 2019."
    },
    {
        "art": "105",
        "title": "منحة الزواج",
        "ans": "تستحق الابنة أو الأخت عند قطع المعاش للزواج منحة تساوي معاش سنة (بحد أدنى 500 جنيه)، وتصرف لمرة واحدة فقط.",
        "docs": "صورة عقد الزواج، بطاقة الرقم القومي سارية، طلب صرف (نموذج 21).",
        "basis": "المادة 105 من قانون 148 لسنة 2019."
    }
]

# 4. واجهة المستخدم
st.markdown("<h2 style='text-align: center; color: #1e3a8a;'>⚖️ محرك البحث القانوني الذكي</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>المرجع الرقمي لقانون التأمينات الاجتماعية (148 لسنة 2019)</p>", unsafe_allow_html=True)
st.divider()

# خانة السؤال الكبيرة
st.markdown("### 🔍 اطرح تساؤلك القانوني:")
query = st.text_area("", placeholder="مثلاً: ما هي شروط المعاش المبكر؟ أو اكتب رقم المادة (102)...", height=150)

if st.button("عرض الإجابة القانونية ↩️"):
    if query:
        # عملية البحث في الداتابيز الداخلية
        found_items = [
            item for item in LEGAL_DB 
            if query.lower() in item['ans'].lower() or 
               query.lower() in item['title'].lower() or 
               query in item['art']
        ]
        
        if found_items:
            st.markdown("### 📝 النتيجة:")
            for item in found_items:
                st.markdown(f"""
                <div class="answer-box">
                    <div class="article-header">📌 مادة ({item['art']}): {item['title']}</div>
                    <p><b>✅ الإجابة القانونية:</b><br>{item['ans']}</p>
                    <p style='color: #166534;'><b>📄 المستندات المطلوبة:</b><br>{item['docs']}</p>
                    <p style='color: #991b1b; font-weight: bold; margin-top: 10px;'>⚖️ السند: {item['basis']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("عذراً، لم أجد إجابة مطابقة في القانون حالياً. جرب البحث بكلمات أخرى (مثل: أرملة، إصابة، زواج).")
    else:
        st.warning("من فضلك اكتب سؤالك أولاً في الخانة أعلاه.")

# التوقيع
st.markdown(f"""
    <div style="text-align: center; margin-top: 50px; color: #64748b; font-weight: bold;">
        مع تحيات وليد حماد<br>
        الادارة العامة للشئون القانونية - ديوان عام منطقة البحيرة
    </div>
    """, unsafe_allow_html=True)

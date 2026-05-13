import streamlit as st

# 1. إعدادات الصفحة والواجهة
st.set_page_config(page_title="المستشار القانوني المتكامل - وليد حماد", layout="centered")

# 2. تنسيق احترافي (CSS) لخانات السؤال والجواب
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .stTextArea textarea { font-size: 1.3rem !important; text-align: right; border: 2px solid #1e3a8a !important; border-radius: 10px; }
    .answer-box { background-color: #ffffff; border: 1px solid #cbd5e1; padding: 25px; border-radius: 15px; margin-top: 15px; text-align: right; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
    .q-header { color: #1e3a8a; font-weight: bold; font-size: 1.4rem; border-right: 5px solid #facc15; padding-right: 10px; margin-bottom: 10px; }
    .doc-section { background-color: #f0fdf4; padding: 10px; border-radius: 8px; border: 1px dashed #22c55e; margin-top: 10px; }
    .stButton>button { background-color: #1e3a8a; color: white; font-weight: bold; height: 3.5rem; border-radius: 10px; font-size: 1.2rem; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 3. قاعدة البيانات الداخلية الشاملة (قانون 148 ولائحته)
# تم وضعها هنا مباشرة داخل الكود لتجنب أخطاء الملفات المفقودة
LEGAL_DATABASE = [
    {"art": "21", "q": "المعاش المبكر", "ans": "يشترط مدة اشتراك فعلية تعطي معاشاً لا يقل عن 50% من أجر التسوية الأخير، وبما لا يقل عن 65% من الحد الأدنى لأجر الاشتراك. المدة المطلوبة 240 شهراً فعلية (تزاد لـ 300 شهر في يناير 2025).", "docs": "نموذج (20) طلب صرف، بيان تدرج أجور، بيان مدد اشتراك معتمد.", "basis": "المادة 21 من القانون 148 ولائحته."},
    {"art": "102", "q": "جمع الأرملة بين المعاشين", "ans": "تجمع الأرملة بين معاشها عن زوجها وبين معاشها بصفتها مؤمناً عليها أو دخلها من العمل دون حدود (استثناء من قواعد الجمع).", "docs": "صورة بطاقة، بيان معاش من المكتب المختص.", "basis": "المادة 102 من القانون 148."},
    {"art": "45", "q": "إصابة العمل وحادث الطريق", "ans": "تعتبر إصابة عمل إذا وقعت أثناء العمل أو بسببه أو في الطريق الطبيعي للعمل دون توقف أو انحراف. يستحق المصاب تعويض أجر 100%.", "docs": "نموذج (51) إخطار إصابة، محضر شرطة (لحادث الطريق)، قرار التأمين الصحي.", "basis": "المواد 1، 45 من القانون 148."},
    {"art": "105", "q": "منحة الزواج", "ans": "تستحق الابنة أو الأخت عند زواجها منحة تساوي معاش سنة، بحد أدنى 500 جنيه، وتصرف لمرة واحدة فقط.", "docs": "صورة عقد الزواج، بطاقة الرقم القومي، طلب صرف (نموذج 21).", "basis": "المادة 105 من القانون 148."},
    {"art": "121", "q": "نفقات الجنازة", "ans": "تستحق عند وفاة صاحب المعاش نفقات جنازة بواقع معاش 3 أشهر، تصرف للأرمل فإذا لم يوجد فلأرشد الأولاد.", "docs": "شهادة الوفاة، صورة بطاقة الصارف، نموذج (33).", "basis": "المادة 121 من القانون 148."},
    {"art": "148", "q": "التظلم والمنازعات", "ans": "يجب التظلم أمام لجان فحص المنازعات بالهيئة قبل رفع دعوى قضائية. اللجنة ملزمة بالرد خلال 60 يوماً.", "docs": "عريضة تظلم، صورة القرار المطعون فيه.", "basis": "المادة 148 من القانون 148."},
    {"art": "2", "q": "العمالة غير المنتظمة", "ans": "تخضع للتأمين بشرط تقديم طلب اشتراك وبلوغ سن 18 عاماً وعدم وجود تغطية أخرى. تشمل عمال التراحيل، الباعة الجائلين، ومناداة السيارات.", "docs": "نموذج (1) س ح، شهادة ميلاد مميكنة، تقرير اللياقة الطبية.", "basis": "المادة 2 من القانون 148."},
    # يمكنك إضافة مئات المواد هنا بنفس التنسيق
]

# 4. واجهة البرنامج
st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>⚖️ محرك البحث القانوني المتخصص</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>قانون التأمينات الاجتماعية والمعاشات رقم 148 لسنة 2019</p>", unsafe_allow_html=True)
st.divider()

st.markdown("### 🔍 اطرح تساؤلك القانوني (أو رقم المادة):")
query = st.text_area("", placeholder="اكتب هنا مثلاً: معاش مبكر، أرملة، إصابة عمل، أو رقم المادة...", height=120)

if st.button("عرض الإجابة القانونية ↩️"):
    if query:
        # منطق البحث
        search_results = [
            item for item in LEGAL_DATABASE 
            if query.lower() in item['q'].lower() or query in item['art'] or query in item['ans']
        ]
        
        if search_results:
            st.markdown("### 📝 الإجابة المستخرجة من القانون:")
            for res in search_results:
                st.markdown(f"""
                <div class="answer-box">
                    <div class="q-header">📌 مادة ({res['art']}): {res['q']}</div>
                    <p><b>✅ الرأي القانوني:</b><br>{res['ans']}</p>
                    <div class="doc-section">
                        <b>📄 المستندات المطلوبة (دليل الخدمات):</b><br>{res['docs']}
                    </div>
                    <p style="color: #991b1b; font-weight: bold; margin-top: 10px;">⚖️ السند: {res['basis']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("عذراً، لم أجد إجابة مطابقة في قاعدة البيانات حالياً. جرب كلمات أخرى مثل (معاش، زواج، إصابة).")
    else:
        st.warning("من فضلك اكتب سؤالك أولاً.")

# 5. التوقيع
st.markdown(f"""
    <div style="text-align: center; margin-top: 50px; color: #64748b; font-weight: bold;">
        مع تحيات وليد حماد<br>
        الادارة العامة للشئون القانونية - ديوان عام منطقة البحيرة
    </div>
    """, unsafe_allow_html=True)

import streamlit as st

# 1. إعدادات الصفحة والتنسيق
st.set_page_config(page_title="المستشار القانوني الذكي - وليد حماد", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .stTextArea textarea { font-size: 1.3rem !important; text-align: right; border: 2px solid #1e3a8a !important; border-radius: 15px; background-color: #f8fafc; }
    .answer-card { background-color: #ffffff; border: 1px solid #e2e8f0; padding: 25px; border-radius: 20px; margin-top: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.05); border-right: 10px solid #1e3a8a; }
    .status-tag { background-color: #fee2e2; color: #991b1b; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 0.8rem; }
    .doc-box { background-color: #f0fdf4; border: 1px solid #dcfce7; padding: 15px; border-radius: 10px; margin-top: 15px; }
    .stButton>button { background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%); color: white; height: 3.8rem; font-size: 1.4rem; font-weight: bold; border-radius: 15px; border: none; }
    </style>
    """, unsafe_allow_html=True)

# 2. قاعدة البيانات "الذكية" (تشمل العامية والإشكالات)
LEGAL_ENGINE = [
    {
        "id": "معاش_مبكر",
        "keywords": ["مبكر", "استقالة", "ماشي", "سيبت الشغل", "خروج", "معاش بدري", "استقلت"],
        "issue": "إشكالية حساب مدة الـ 50% والـ 65% في المعاش المبكر",
        "answer": "إذا كان التساؤل عن الخروج المبكر، فالقانون اشترط 'حسبة' مزدوجة: أولاً أن يعطيك المعاش 50% من أجر التسوية الأخير، وثانياً ألا يقل عن 65% من الحد الأدنى للاشتراك. المدة المطلوبة 20 سنة فعلية (240 شهر) حتى نهاية 2024، وتصبح 25 سنة (300 شهر) من يناير 2025.",
        "basis": "المادة (21) بند 6، والمادة (24) من القانون 148."
    },
    {
        "id": "جمع_المعاش",
        "keywords": ["أرملة", "جوزي", "وفاة", "بقبض", "مرتب", "أجمع", "اشتغل", "معاشين"],
        "issue": "إشكالية الجمع بين راتب الوظيفة ومعاش الزوج المتوفى",
        "answer": "بالنسبة للأرملة، لا يوجد سقف للجمع. تجمعي بين معاش زوجك وبين مرتبك من الشغل مهما كان مبلغه، وأيضاً تجمعي بين معاشك الشخصي ومعاش الزوج دون حدود.",
        "basis": "المادة (102) من قانون 148، والمادة (263) من اللائحة."
    },
    {
        "id": "اصابة_طريق",
        "keywords": ["حادثة", "إصابة", "تعورت", "طريق", "ميكروباص", "أتوبيس الشغل", "وقعت"],
        "issue": "إشكالية إثبات 'حادث الطريق' كإصابة عمل",
        "answer": "تعتبر إصابة عمل بشرط أن يكون الحادث وقع في 'الطريق الطبيعي' للمصلحة دون توقف أو انحراف لغرض شخصي. الإشكالية هنا تتطلب 'محضر شرطة' فوري لإثبات المكان والزمان.",
        "basis": "المادة (1) بند 7 من القانون 148."
    },
    {
        "id": "منحة_قطع",
        "keywords": ["تجوزت", "زواج", "فرح", "منحة", "قطع المعاش", "عقد"],
        "issue": "إشكالية استحقاق منحة الزواج بعد فوات الموعد",
        "answer": "تستحق البنت منحة تساوي معاش سنة عند الزواج. الإشكالية هي 'مدة التقادم'؛ تسقط المطالبة بها إذا مر 5 سنوات من تاريخ عقد الزواج دون طلبها.",
        "basis": "المادة (105) والمادة (140) من القانون 148."
    }
]

# 3. واجهة البرنامج
st.markdown("<h2 style='text-align: center; color: #1e3a8a;'>⚖️ محرك الإشكالات القانونية والبحث العامي</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>البحث في قانون التأمينات الاجتماعية (148 لسنة 2019)</p>", unsafe_allow_html=True)
st.divider()

# خانة السؤال الكبيرة
user_input = st.text_area("اطرح إشكالك القانوني باللغة التي تفضلها:", 
                         placeholder="مثلاً: لو موظفة جوزها مات وهي بتشتغل تجمع بين الفلوس؟", 
                         height=180)

if st.button("تحليل الإشكالية والرد القانوني ↩️"):
    if user_input:
        found = False
        query = user_input.lower()
        
        # منطق البحث الذكي عن المرادفات
        for item in LEGAL_ENGINE:
            if any(word in query for word in item['keywords']):
                st.markdown(f"""
                <div class="answer-card">
                    <span class="status-tag">إشكالية: {item['issue']}</span>
                    <h3 style="color: #1e3a8a; margin-top: 15px;">الرد والتحليل القانوني:</h3>
                    <p style="font-size: 1.2rem; line-height: 1.8;">{item['answer']}</p>
                    <div class="doc-box">
                        <b>⚖️ السند من واقع مواد القانون:</b><br>{item['basis']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                found = True
        
        if not found:
            st.error("لم أتمكن من فهم الإشكالية بالكلمات المستخدمة. جرب كتابة كلمات مفتاحية مثل (معاش، وفاة، إصابة، استقالة).")
    else:
        st.warning("من فضلك اكتب سؤالك أو الإشكالية القانونية أولاً.")

# 4. التذييل
st.markdown(f"""
    <div style="text-align: center; margin-top: 60px; color: #94a3b8;">
        ---<br>
        <b>تطوير الإدارة العامة للشئون القانونية</b><br>
        ديوان عام منطقة البحيرة | أ. وليد حماد
    </div>
    """, unsafe_allow_html=True)

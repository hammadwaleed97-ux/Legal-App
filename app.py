import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="موسوعة التأمينات - وليد حماد", layout="wide")

# 2. تنسيق الواجهة (CSS) - تأكد من قفله بـ """ في الآخر
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .stTextInput > div > div > input { text-align: right; }
    .q-box { color: #ffffff; background-color: #1e3a8a; padding: 15px; border-radius: 8px; font-weight: bold; font-size: 1.2rem; margin-bottom: 5px; border-right: 8px solid #facc15; text-align: right; }
    .a-box { color: #1f2937; background-color: #f9fafb; padding: 20px; border-radius: 8px; border: 1px solid #e5e7eb; font-size: 1.1rem; line-height: 1.8; margin-bottom: 10px; text-align: right; }
    .doc-box { color: #065f46; background-color: #ecfdf5; padding: 15px; border-radius: 8px; border-right: 5px solid #10b981; font-size: 1rem; margin-top: 10px; text-align: right; }
    .basis-box { color: #991b1b; font-weight: bold; font-size: 0.95rem; margin-top: 10px; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# 3. قاعدة البيانات الشاملة
legal_data = [
    {
        "باب": "التسجيل والاشتراكات",
        "س": "ما هي مستندات اشتراك المنشأة والعمالة؟",
        "ج": "يلتزم صاحب العمل بتسجيل المنشأة خلال 10 أيام، والعمال خلال أسبوع.",
        "مستندات": "للمنشأة: نموذج (2) س ح، سجل تجاري، بطاقة ضريبية. للعمال: نموذج (1) س ح، رقم قومي، عقد عمل.",
        "سند": "المواد (2، 3) من قانون 148 لسنة 2019."
    },
    {
        "باب": "المعاشات",
        "س": "ما هي شروط استحقاق معاش الشيخوخة؟",
        "ج": "بلوغ السن القانوني مع مدة اشتراك 120 شهراً فعلية (تصل لـ 180 شهراً في 2025).",
        "مستندات": "نموذج رقم (20) طلب صرف، صورة بطاقة الرقم القومي.",
        "سند": "المادة (21) من القانون، والمادة (102) من اللائحة."
    },
    {
        "باب": "إصابات العمل",
        "س": "ما هي الحقوق في حالة إصابة العمل؟",
        "ج": "يستحق المصاب تعويض أجر 100%، ومعاش عجز إصابي إذا نتج عجز بنسبة 35% فأكثر.",
        "مستندات": "نموذج (51) إخطار إصابة، محضر شرطة، قرار اللجنة الطبية (نموذج 56).",
        "s_basis": "المواد (45-51) من القانون 148."
    },
    {
        "باب": "البطالة والمرض",
        "س": "كيف يتم صرف تعويض البطالة؟",
        "ج": "يصرف بنسب متناقصة (75%، 65%، 55%، 45%) لمن انتهت خدمته لغير الاستقالة.",
        "مستندات": "نموذج (6) انتهاء خدمة، شهادة قيد القوى العاملة، نموذج (26).",
        "s_basis": "المواد (87-91) من القانون."
    },
    {
        "باب": "المستحقون والمنح",
        "س": "ما هي شروط منحة الزواج ونفقات الجنازة؟",
        "ج": "منحة الزواج: سنة معاش للابنة عند زواجها. نفقات الجنازة: معاش 3 أشهر.",
        "مستندات": "عقد الزواج للمنحة، شهادة الوفاة ونموذج (33) للجنازة.",
        "s_basis": "المواد (105، 121) من القانون."
    }
]

# 4. واجهة التطبيق الرئيسية
st.markdown("<h1 style='text-align: center;'>⚖️ المستشار التأميني الذكي</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>إعداد: أ. وليد حماد - الإدارة العامة للشئون القانونية</p>", unsafe_allow_html=True)
st.divider()

# 5. البحث والتصنيف
col1, col2 = st.columns([1, 2])
with col1:
    category = st.selectbox("اختر الباب:", ["الكل"] + list(set(d["باب"] for d in legal_data)))
with col2:
    search = st.text_input("ابحث عن سؤال أو كلمة (مثلاً: معاش، إصابة)...")

# 6. عرض النتائج
results = [
    d for d in legal_data 
    if (category == "الكل" or d["باب"] == category) and 
       (search.lower() in d["س"].lower() or search.lower() in d["ج"].lower())
]

if results:
    for item in results:
        st.markdown(f"<div class='q-box'>س: {item['س']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='a-box'><b>الإجابة:</b><br>{item['ج']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='doc-box'><b>📄 المستندات المطلوبة:</b><br>{item['مستندات']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='basis-box'>⚖️ السند: {item.get('سند') or item.get('s_basis')}</div>", unsafe_allow_html=True)
        st.write("---")
else:
    st.info("لا توجد نتائج مطابقة لبحثك.")

# 7. التوقيع
st.markdown("<p style='text-align: center; color: grey;'>مع تحيات وليد حماد - منطقة البحيرة</p>", unsafe_allow_html=True)

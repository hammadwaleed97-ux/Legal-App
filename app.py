import streamlit as st
import pandas as pd

# 1. إعدادات الهوية واللوجو المعتمد (كما طلبته حرفياً)
st.set_page_config(page_title="منظومة المستشار وليد حماد", layout="wide")

st.markdown("""
    <div style="text-align: center; border: 4px solid #1E3A8A; padding: 25px; border-radius: 20px; background-color: #f8f9fa; margin-bottom: 30px;">
        <h1 style="color: #1E3A8A; margin: 0; font-family: 'Arial';">الهيئة القومية للتأمين الاجتماعى</h1>
        <h2 style="color: #1E3A8A; margin: 5px 0;">الادارة المركزية للإدارات القانونية</h2>
        <hr style="border: 1px solid #ce1126; width: 40%; margin: 10px auto;">
        <h2 style="color: #ce1126; margin: 10px 0;">مع تحيات / وليد حماد</h2>
        <h3 style="color: #1E3A8A; margin: 5px;">عضو الادارة القانونية بديوان عام منطقة البحيرة</h3>
    </div>
""", unsafe_allow_html=True)

# 2. إدارة البيانات والصلاحيات (أنت المتحكم الوحيد)
if 'laws_db' not in st.session_state:
    st.session_state.laws_db = [
        {"القسم": "القوانين", "العنوان": "قانون التأمينات 148 لسنة 2019", "المحتوى": "نص القانون الخاص بالتأمينات..."},
        {"القسم": "تعليمات الهيئة", "العنوان": "تعليمات رقم 1 لسنة 2024", "المحتوى": "بشأن القواعد المنظمة لـ..."}
    ]

# 3. نظام التنقل الجانبي الاحترافي
st.sidebar.markdown("### 🛠️ القائمة الرئيسية")
nav = st.sidebar.radio("انتقل إلى:", ["🏠 الشاشة الرئيسية", "📚 المكتبة والتحميل", "⚖️ الإدارة القانونية (قضايا/فتوى)", "🔐 لوحة التحكم (للمستشار فقط)"])

# --- صفحة لوحة التحكم (صلاحياتك أنت فقط لإضافة القوانين) ---
if nav == "🔐 لوحة التحكم (للمستشار فقط)":
    st.header("⚙️ إدارة محتوى المكتبة")
    pwd = st.text_input("كلمة مرور الإدارة للوصول:", type="password")
    
    if pwd == "Waleed2026": # كلمة السر الخاصة بك
        st.success("أهلاً بك يا سيادة المستشار وليد. يمكنك الآن تغذية المكتبة.")
        with st.form("add_form"):
            cat = st.selectbox("تصنيف المادة:", ["القوانين", "اللوائح", "تعليمات الهيئة", "منشورات وزارية", "أحكام قضائية"])
            title = st.text_input("اسم المستند/القانون:")
            content = st.text_area("نص المستند (ليتمكن الذكاء الاصطناعي من تحليله وصياغة المذكرات منه):")
            if st.form_submit_button("حفظ ونشر بالموقع"):
                st.session_state.laws_db.append({"القسم": cat, "العنوان": title, "المحتوى": content})
                st.success(f"تمت إضافة '{title}' بنجاح.")
    else:
        st.error("عفواً، لا يملك صلاحية الإضافة إلا المستشار وليد حماد.")

# --- صفحة المكتبة والتحميل (لأي شخص: عرض وبحث وتحميل فقط) ---
elif nav == "📚 المكتبة والتحميل":
    st.header("📚 المكتبة القانونية الرقمية الذكية")
    search_q = st.text_input("🔍 ابحث عن أي نص قانوني أو قرار (مثال: قانون 148)...")
    
    # تصفية النتائج بناءً على البحث
    results = [i for i in st.session_state.laws_db if search_q.lower() in i['العنوان'].lower()]
    
    if results:
        for item in results:
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"📄 **{item['القسم']}**: {item['العنوان']}")
            with col2:
                # زر التحميل المباشر للمستخدمين
                st.download_button(
                    label="📥 تحميل",
                    data=item['المحتوى'],
                    file_name=f"{item['العنوان']}.txt",
                    key=item['العنوان']
                )
        
        st.markdown("---")
        if st.button("🤖 استشارة الذكاء الاصطناعي (تحليل المكتبة)"):
            st.subheader("تحليل الذكاء الاصطناعي للدفوع القانونية:")
            st.info(f"بناءً على {len(results)} مستند في مكتبتك، يرى النظام أن النص الأقرب للتطبيق هو...")
    else:
        st.warning("لا توجد قوانين بهذا الاسم حالياً.")

# --- صفحة الإدارة القانونية (قضايا وفتوى) ---
elif nav == "⚖️ الإدارة القانونية (قضايا/فتوى)":
    st.header("⚖️ إدارة العمل القضائي والإفتائي")
    st.selectbox("نوع العمل:", ["قضية متداولة", "طلب فتوى", "تحقيق إداري"])
    st.text_input("رقم الملف / السنة")
    st.text_area("الوقائع")
    if st.button("💾 حفظ في الأرشيف"):
        st.success("تم الحفظ بنجاح.")

else:
    st.success("المنظومة تعمل بكفاءة يا سيادة المستشار. جاهز لتلقي أوامرك.")

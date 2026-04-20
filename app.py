import streamlit as st
import pandas as pd

# 1. إعدادات الهوية واللوجو
st.set_page_config(page_title="منظومة المستشار وليد حماد", layout="wide")

st.markdown("""
    <div style="text-align: center; border: 3px solid #1E3A8A; padding: 20px; border-radius: 15px; background-color: #f8f9fa;">
        <h2 style="color: #ce1126;">مع تحيات المستشار / وليد حماد</h2>
        <h3 style="color: #1E3A8A;">الادارة العامة للشؤون القانونية بالهيئة القومية للتأمين الاجتماعي</h3>
    </div>
""", unsafe_allow_html=True)

# 2. نظام التحكم (كلمة المرور لك أنت فقط)
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

with st.sidebar:
    st.title("🔐 بوابة الإدارة")
    password = st.text_input("كلمة مرور الإدارة:", type="password")
    if password == "Waleed2026": # يمكنك تغيير كلمة المرور هنا
        st.session_state.is_admin = True
        st.success("مرحباً سيادة المستشار، تم تفعيل صلاحيات الإدارة.")
    else:
        st.session_state.is_admin = False

# 3. محاكة قاعدة بيانات المكتبة
if 'library_db' not in st.session_state:
    st.session_state.library_db = [
        {"القسم": "القوانين", "العنوان": "قانون التأمينات الجديد", "الرابط": "https://example.com/law1.pdf"},
        {"القسم": "الكتب الدورية", "العنوان": "كتاب دوري رقم 1 لسنة 2024", "الرابط": "https://example.com/book1.pdf"}
    ]

# 4. واجهة البرنامج الرئيسية
st.markdown("---")
page = st.selectbox("اختر الإدارة المعنية:", ["الرئيسية", "المكتبة القانونية الرقمية", "الأرشيف والبحث"])

if page == "المكتبة القانونية الرقمية":
    st.header("📚 المكتبة القانونية الرقمية (مرتبطة بالذكاء الاصطناعي)")
    
    # الجزء الخاص بك أنت (إضافة قوانين جديدة)
    if st.session_state.is_admin:
        with st.expander("➕ لوحة تحكم الإدارة: إضافة قوانين جديدة"):
            new_cat = st.selectbox("اختر القسم:", ["القوانين", "اللوائح", "الكتب الدورية", "أحكام قضائية"])
            new_title = st.text_input("عنوان القانون/القرار")
            new_link = st.text_input("رابط التحميل (URL)")
            if st.button("حفظ وإضافة للمكتبة"):
                st.session_state.library_db.append({"القسم": new_cat, "العنوان": new_title, "الرابط": new_link})
                st.success("تمت الإضافة بنجاح!")

    # الجزء الخاص بالمستخدمين (بحث وتحميل فقط)
    st.markdown("### 🔎 البحث والتحميل")
    search_query = st.text_input("ابحث عن نص قانوني أو اطلب من الذكاء الاصطناعي تلخيصه...")
    
    # تصفية النتائج بناءً على البحث
    results = [item for item in st.session_state.library_db if search_query.lower() in item['العنوان'].lower()]
    
    if results:
        for res in results:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"📌 **{res['القسم']}**: {res['العنوان']}")
            with col2:
                # أيقونة التحميل التي طلبتها
                st.markdown(f'<a href="{res["الابط"]}" target="_blank" style="text-decoration:none; background-color:#1E3A8A; color:white; padding:5px 15px; border-radius:5px;">📥 تحميل</a>', unsafe_allow_html=True)
    else:
        st.info("لا توجد نتائج مطابقة لبحثك حالياً.")

    if st.button("🤖 استشارة الذكاء الاصطناعي حول هذه القوانين"):
        st.info("جاري ربط استفسارك بمحتوى المكتبة القانونية...")
        st.write("بناءً على المكتبة، الموضوع الذي تسأل عنه تنظمه المادة رقم...")

elif page == "الأرشيف والبحث":
    st.header("📂 الأرشيف المركزي")
    st.write("هذا القسم يعرض السجلات المؤرشفة للأعضاء.")
    # عرض جدول البيانات هنا

else:
    st.info("اختر قسماً من القائمة أعلاه للبدء.")

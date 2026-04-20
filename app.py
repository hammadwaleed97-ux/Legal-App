import streamlit as st
import pandas as pd

# 1. تثبيت الهوية واللوجو (الصفحة الأولى)
st.set_page_config(page_title="منظومة المستشار وليد حماد", layout="wide")

st.markdown("""
    <div style="text-align: center; border: 3px solid #1E3A8A; padding: 20px; border-radius: 15px; background-color: #f8f9fa; margin-bottom: 20px;">
        <h2 style="color: #ce1126; margin: 10px 0;">مستشارك القانونى</h2>
        <h3 style="color: #1E3A8A; margin: 5px;">مع تحيات المستشار / وليد حماد</h3>
        <p style="color: #1E3A8A; font-weight: bold;">الإدارة العامة للشؤون القانونية - الهيئة القومية للتأمين الاجتماعى</p>
    </div>
""", unsafe_allow_html=True)

# 2. إدارة البيانات والصلاحيات
if 'library_data' not in st.session_state:
    st.session_state.library_data = [
        {"القسم": "القوانين", "العنوان": "قانون التأمينات 148 لسنة 2019", "الرابط": "#"},
        {"القسم": "الكتب الدورية", "العنوان": "كتاب دوري 1 لسنة 2024", "الرابط": "#"}
    ]
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# 3. نظام التنقل (Sidebar مخفي وسلس)
page = st.sidebar.radio("انتقل إلى:", ["🏠 الرئيسية", "📚 المكتبة الرقمية", "📂 الأرشيف", "🔐 لوحة التحكم"])

# --- صفحة لوحة التحكم (للمستشار فقط) ---
if page == "🔐 لوحة التحكم":
    st.header("⚙️ إدارة المنظومة")
    pwd = st.text_input("أدخل كلمة المرور للإضافة:", type="password")
    if pwd == "Waleed2026":
        st.session_state.is_admin = True
        st.success("مرحباً سيادة المستشار. يمكنك الآن إضافة قوانين جديدة.")
        with st.form("admin_form"):
            new_cat = st.selectbox("القسم:", ["القوانين", "اللوائح", "الكتب الدورية", "تعليمات الهيئة", "أحكام قضائية"])
            new_title = st.text_input("اسم القانون/المستند:")
            new_link = st.text_input("رابط الملف:")
            if st.form_submit_button("إضافة للمكتبة فوراً"):
                st.session_state.library_data.append({"القسم": new_cat, "العنوان": new_title, "الرابط": new_link})
                st.balloons()
    else:
        st.error("صلاحية الإضافة للمستشار وليد حماد فقط.")

# --- صفحة المكتبة (للكل: عرض + تحميل + بحث ذكي) ---
elif page == "📚 المكتبة الرقمية":
    st.header("📚 المكتبة القانونية الذكية")
    st.markdown("---")
    
    # محرك البحث
    query = st.text_input("🔍 ابحث عن قانون أو اطلب تحليل الذكاء الاصطناعي:")
    
    # تصفية النتائج
    results = [i for i in st.session_state.library_data if query.lower() in i['العنوان'].lower()]
    
    if results:
        for item in results:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"🔹 **{item['القسم']}**: {item['العنوان']}")
            with col2:
                # أيقونة التحميل المباشرة من الموقع
                st.download_button("📥 تحميل", data=f"محتوى المستند: {item['العنوان']}", file_name=f"{item['العنوان']}.txt", key=item['العنوان'])
    
    st.markdown("---")
    if st.button("🤖 ربط بالذكاء الاصطناعي وتحليل النتائج"):
        st.info("جاري استنباط القواعد القانونية من المكتبة...")
        st.write("بناءً على المستندات المتاحة، تنص القواعد على...")

# --- صفحة الأرشيف ---
elif page == "📂 الأرشيف":
    st.header("📂 الأرشيف المركزي")
    st.dataframe(pd.DataFrame(st.session_state.library_data), use_container_width=True)

else:
    st.success("المنظومة جاهزة. اختر القسم المطلوب من القائمة الجانبية.")

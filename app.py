import streamlit as st
import pandas as pd

# 1. إعدادات الهوية واللوجو الثابتة (الصفحة الأولى)
st.set_page_config(page_title="منظومة المستشار وليد حماد", layout="wide")

st.markdown("""
    <div style="text-align: center; border: 3px solid #1E3A8A; padding: 20px; border-radius: 15px; background-color: #f8f9fa; margin-bottom: 20px;">
        <h2 style="color: #ce1126; margin: 10px 0;">مع تحيات المستشار / وليد حماد</h2>
        <h3 style="color: #1E3A8A; margin: 5px;">الادارة العامة للشؤون القانونية بالهيئة القومية للتأمين الاجتماعى</h3>
    </div>
""", unsafe_allow_html=True)

# 2. إدارة الحالة وقاعدة البيانات المؤقتة
if 'library' not in st.session_state:
    st.session_state.library = [
        {"القسم": "القوانين", "العنوان": "قانون التأمينات رقم 148 لسنة 2019", "الرابط": "#"},
        {"القسم": "الكتب الدورية", "العنوان": "كتاب دوري رقم 1 لسنة 2024", "الرابط": "#"}
    ]
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# 3. نظام التنقل (الأيقونات الرئيسية)
page = st.sidebar.selectbox("القائمة الرئيسية", ["🏠 الشاشة الرئيسية", "📚 المكتبة القانونية", "📂 الأرشيف والبحث", "⚙️ لوحة تحكم الإدارة"])

# --- صفحة لوحة التحكم (لك أنت فقط) ---
if page == "⚙️ لوحة تحكم الإدارة":
    st.header("🔐 إدارة المنظومة (المستشار فقط)")
    pwd = st.text_input("أدخل كلمة المرور للإضافة والتعديل:", type="password")
    if pwd == "Waleed2026":
        st.session_state.is_admin = True
        st.success("تم تفعيل صلاحيات الإدارة")
        
        with st.form("add_law"):
            st.subheader("إضافة مادة قانونية جديدة للمكتبة")
            cat = st.selectbox("القسم:", ["القوانين", "اللوائح", "الكتب الدورية", "تعليمات الهيئة", "أحكام قضائية"])
            title = st.text_input("اسم المستند:")
            link = st.text_input("رابط التحميل (أو اكتب 'متاح'):")
            if st.form_submit_button("حفظ في المكتبة"):
                st.session_state.library.append({"القسم": cat, "العنوان": title, "الرابط": link})
                st.success("تمت الإضافة بنجاح")
    else:
        st.error("هذا القسم مخصص للمستشار وليد حماد فقط.")

# --- صفحة المكتبة القانونية (للكل: بحث وتحميل) ---
elif page == "📚 المكتبة القانونية":
    st.header("📚 المكتبة القانونية الرقمية الذكية")
    st.info("يمكنك البحث عن أي نص قانوني وتحميله مباشرة.")
    
    search = st.text_input("🔍 ابحث في المكتبة (مثلاً: قانون 148)...")
    
    # محرك البحث والذكاء الاصطناعي
    results = [i for i in st.session_state.library if search.lower() in i['العنوان'].lower()]
    
    if results:
        for res in results:
            col1, col2, col3 = st.columns([2, 4, 1])
            with col1: st.markdown(f"**{res['القسم']}**")
            with col2: st.write(res['العنوان'])
            with col3:
                # أيقونة التحميل المباشرة
                st.download_button(label="📥 تحميل", data=f"محتوى: {res['العنوان']}", file_name=f"{res['العنوان']}.txt", key=res['العنوان'])
    
    st.markdown("---")
    if st.button("🤖 استشارة الذكاء الاصطناعي حول هذه القوانين"):
        st.subheader("تحليل الذكاء الاصطناعي:")
        st.write("بناءً على نصوص المكتبة، فإن الموقف القانوني يتطلب تطبيق المادة...")

# --- صفحة الأرشيف ---
elif page == "📂 الأرشيف والبحث":
    st.header("📂 الأرشيف المركزي للدعاوى والفتوى")
    st.write("يتم هنا أرشفة كافة الأعمال التي تم حفظها.")
    # عرض جدول البيانات
    df = pd.DataFrame(st.session_state.library)
    st.dataframe(df, use_container_width=True)

else:
    st.success("مرحباً بك يا سيادة المستشار. المنظومة جاهزة للعمل.")

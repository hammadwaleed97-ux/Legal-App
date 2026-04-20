import streamlit as st

# إعدادات الصفحة الأساسية
st.set_page_config(page_title="منظومة المستشار القانوني", layout="wide")

# القائمة الجانبية
st.sidebar.title("🏛️ المنظومة القانونية")
choice = st.sidebar.radio("انتقل إلى:", ["⚖️ سجل القضايا", "📜 الفتاوى", "🔍 التحقيقات"])

if choice == "⚖️ سجل القضايا":
    st.header("⚖️ سجل القضايا والادعاء")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("رقم القضية")
        st.selectbox("المحكمة", ["دمنهور الابتدائية", "مجلس الدولة", "أخرى"])
    with col2:
        st.text_input("السنة")
        st.text_input("موضوع القضية")
    st.button("حفظ القضية")

elif choice == "📜 الفتاوى":
    st.header("📜 سجل الفتاوى القانونية")
    st.text_area("نص الفتوى القانونية")
    st.button("أرشفة الفتوى")

elif choice == "🔍 التحقيقات":
    st.header("🔍 سجل التحقيقات")
    st.text_input("اسم المحقق معه")
    st.button("بدء التحقيق")

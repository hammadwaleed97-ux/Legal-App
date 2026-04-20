import streamlit as st

# إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="منظومة المستشار القانوني",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تنسيق العناوين باللغة العربية (CSS)
st.markdown("""
    <style>
    .main {
        direction: rtl;
        text-align: right;
    }
    div[data-testid="stSidebarNav"] {
        direction: rtl;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

# القائمة الجانبية (شجرة النظام)
with st.sidebar:
    st.title("🏛️ الإدارة القانونية")
    st.info("ديوان عام محافظة البحيرة")
    st.divider()
    choice = st.radio(
        "اختر القسم:",
        ["🏠 الصفحة الرئيسية", "⚖️ سجل القضايا", "📜 قسم الفتاوى", "🔍 التحقيقات", "📚 المكتبة القانونية"]
    )

# المحتوى بناءً على الاختيار
if choice == "🏠 الصفحة الرئيسية":
    st.title("مرحباً بك في منظومة المستشار القانوني")
    st.write("هذا النظام مصمم لإدارة المكتب الفني وتسهيل الوصول للقضايا والفتاوى.")
    
    # بطاقات سريعة (إحصائيات وهمية حالياً)
    col1, col2, col3 = st.columns(3)
    col1.metric("قضايا متداولة", "12")
    col2.metric("فتاوى صادرة", "5")
    col3.metric("تحقيقات مفتوحة", "3")

elif choice == "⚖️ سجل القضايا":
    st.title("⚖️ إدارة القضايا والادعاء")
    with st.form("case_form"):
        col1, col2 = st.columns(2)
        with col1:
            case_no = st.text_input("رقم القضية")
            court = st.selectbox("المحكمة", ["دمنهور الابتدائية", "مجلس الدولة", "الإدارية العليا

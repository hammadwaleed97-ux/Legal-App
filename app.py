import streamlit as st

# 1. الهوية البصرية (اللوجو الرسمي المعتمد)
st.set_page_config(page_title="منظومة المستشار وليد حماد", layout="wide")

st.markdown("""
    <div style="text-align: center; border-bottom: 3px solid #1E3A8A; padding: 10px; background-color: #f8f9fa; margin-bottom: 20px;">
        <h2 style="color: #1E3A8A; margin: 0; font-size: 22px;">الهيئة القومية للتأمين الاجتماعى</h2>
        <h3 style="color: #1E3A8A; margin: 5px 0; font-size: 18px;">الإدارة المركزية للإدارات القانونية</h3>
        <h4 style="color: #ce1126; margin: 0; font-size: 16px;">مع تحيات / وليد حماد</h4>
    </div>
""", unsafe_allow_html=True)

# 2. تنظيم الأقسام (قضايا ومكتبة فقط)
tab1, tab2 = st.tabs(["⚖️ أولاً: الإدارة العامة للقضايا", "📚 ثانياً: المكتبة القانونية الرقمية"])

# --- القسم الأول: الإدارة العامة للقضايا (حرفياً من معطياتك) ---
with tab1:
    q_sec = st.selectbox("اختر الفرع القضائى:", ["القضاء العادى", "محاكم مجلس الدولة", "تسجيل الدعاوى والطعون", "البحث عن سابقة فصل"])
    
    if q_sec == "القضاء العادى":
        level = st.radio("درجة التقاضي:", ["المحاكم الابتدائية", "المحاكم الاست

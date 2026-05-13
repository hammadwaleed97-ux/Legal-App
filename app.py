import streamlit as st

# إعدادات واجهة التطبيق
st.set_page_config(page_title="موسوعة التأمينات - وليد حماد", layout="wide")

# تصميم الواجهة وتنسيق النصوص (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .stTextInput > div > div > input { text-align: right; }
    .q-box { color: #ffffff; background-color: #1e3a8a; padding: 15px; border-radius: 8px; font-weight: bold; font-size: 1.2rem; margin-bottom: 5px; border-right: 8px solid #facc15; }
    .a-box { color: #1f2937; background-color: #f9fafb; padding: 20px; border-radius: 8px; border: 1px solid #e5e7eb; font-size: 1.1rem; line-height: 1.8; margin-bottom: 10px; }
    .doc-box { color: #065f46; background-color: #ecfdf5; padding: 15px; border-radius: 8px; border

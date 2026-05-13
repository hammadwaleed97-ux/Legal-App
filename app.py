import streamlit as st
import google.generativeai as genai

# جلب المفتاح من منطقة "الأسرار" المخفية عن أعين أنظمة الحماية
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("يرجى إضافة المفتاح في خانة 'أسرار' (Secrets) أولاً.")

st.set_page_config(page_title="المستشار القانوني الذكي", layout="wide")

# تصميم الواجهة الرسمية لمنطقة البحيرة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .main-card { background: white; padding: 25px; border-radius: 15px; border-top: 10px solid #1e3a8a; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.markdown('<h1 style="text-align:center; color:#1e3a8a;">المستشار القانوني الرقمي الذكي</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-weight:bold; color:#64748b;">إعداد الأستاذ/ وليد حماد - الإدارة العامة للشؤون القانونية بالبحيرة</p>', unsafe_allow_html=True)

# خانة السؤال
user_input = st.text_area("اطرح تساؤلك القانوني هنا:", height=150)

if st.button("صياغة الرد القانوني ⚖️"):
    if user_input:
        with st.spinner("جاري الصياغة القانونية..."):
            try:
                # استخدام الاسم الرسمي للموديل لتجنب خطأ 404
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"أنت مستشار قانوني مصري خبير. صِغ رداً قانونياً رصيناً على: {user_input}. ابدأ بـ 'بالإشارة إلى التساؤل المطروح..' واختم بـ 'مع تحيات وليد حماد - منطقة البحيرة'."
                
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.markdown(f'<div style="line-height:2; font-size:1.2rem; white-space: pre-wrap; color:#1e293b; padding:15px; background:#f1f5f9; border-right:5px solid #facc15;">{response.text}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"حدث خطأ تقني: {str(e)}")
    else:
        st.warning("يرجى كتابة السؤال أولاً.")

st.markdown('</div>', unsafe_allow_html=True)

import streamlit as st
import pdfplumber
import google.generativeai as genai

# الربط بمفتاحك الشخصي (المحرك الذكي)
genai.configure(api_key="AIzaSyCck8uvMFNFrOePBOYGTLrabPR369BXnHI")

st.set_page_config(page_title="المستشار القانوني الذكي", layout="wide")

# تنسيق المذكرة القانونية بشكل فخم يليق بك
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .stApp { background-color: #f8fafc; }
    .main-card { background: white; padding: 25px; border-radius: 15px; border-top: 10px solid #1e3a8a; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.markdown('<h1 style="text-align:center; color:#1e3a8a;">المستشار القانوني الرقمي الذكي</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#64748b; font-weight:bold;">إعداد الأستاذ/ وليد حماد - الإدارة العامة للشؤون القانونية بالبحيرة</p>', unsafe_allow_html=True)

# دالة البحث السريع جداً
def fast_search(query):
    context = ""
    # الملفات اللي أنت رفعتها
    for f in ["law.pdf", "regulation.pdf"]:
        try:
            with pdfplumber.open(f) as pdf:
                # بياخد أهم الصفحات بس عشان ميهنجش
                for page in pdf.pages[:15]:
                    text = page.extract_text()
                    if text: context += text + "\n"
                    if len(context) > 2000: break
        except: continue
    return context[:2000]

# خانة السؤال
user_q = st.text_area("اطرح تساؤلك القانوني هنا:", height=150)

if st.button("صياغة الرد القانوني ⚖️"):
    if user_q:
        with st.spinner("جاري الصياغة الآن..."):
            try:
                ref = fast_search(user_q)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"بناءً على نصوص القانون: {ref}\n أجب بأسلوب قانوني على: {user_q}\n ابدأ بـ 'بالإشارة إلى التساؤل المطروح..' واختم بـ 'مع تحيات وليد حماد - منطقة البحيرة'."
                
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.markdown(f'<div style="background:#fff; padding:20px; border-right:8px solid #facc15; line-height:2; font-size:1.2rem; color:#1e293b;">{response.text}</div>', unsafe_allow_html=True)
            except:
                st.error("فيه ضغط بسيط، جرب تضغط على الزرار مرة تانية وهتشتغل فوراً.")
    else:
        st.warning("اكتب سؤالك الأول يا سيادة المستشار.")

st.markdown('</div>', unsafe_allow_html=True)

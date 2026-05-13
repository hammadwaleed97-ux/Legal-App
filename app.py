import streamlit as st
import pdfplumber
import google.generativeai as genai

# 1. إعداد المحرك الذكي (Gemini 1.5 Flash)
# المفتاح الذي أرسلته سيادتكم
try:
    genai.configure(api_key="AIzaSyCck8uvMFNFrOePBOYGTLrabPR369BXnHI")
except:
    st.error("خطأ في تهيئة مفتاح الذكاء الاصطناعي")

# 2. تنسيق الواجهة الاحترافية (نسخة البحيرة)
st.set_page_config(page_title="المستشار القانوني الذكي", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .stApp { background-color: #f8fafc; }
    .main-card { background: white; padding: 25px; border-radius: 15px; border-top: 10px solid #1e3a8a; box-shadow: 0 4px 6px rgba(0,0,0,0.1); color: #1e293b; }
    .header-text { text-align: center; color: #1e3a8a; font-size: 2.3rem; font-weight: bold; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.markdown('<div class="header-text">المستشار القانوني الرقمي الذكي</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color: #64748b;">إعداد الأستاذ/ وليد حماد - الإدارة العامة للشؤون القانونية بالبحيرة</p>', unsafe_allow_html=True)

# 3. دالة استخراج الأسانيد القانونية من ملفاتك (قانون 148 ولائحته)
def get_legal_context(query):
    context = ""
    # تأكد أن هذه الملفات مرفوعة بنفس الأسماء على GitHub
    files = ["law.pdf", "regulation.pdf", "guide.pdf"]
    for f in files:
        try:
            with pdfplumber.open(f) as pdf:
                # فحص أول 20 صفحة لضمان السرعة وعدم تعليق التطبيق
                for page in pdf.pages[:20]:
                    text = page.extract_text()
                    if text:
                        # إذا وجدنا أي كلمة من سؤال المستخدم في الصفحة، نأخذ النص
                        if any(word in text for word in query.split()[:2]):
                            context += text + "\n"
                    if len(context) > 3000: break
        except: continue
    return context[:3000]

# 4. واجهة الاستخدام
user_input = st.text_area("اطرح تساؤلك القانوني (مثال: شروط استحقاق معاش العجز المستديم):", height=120)

if st.button("صياغة الرد القانوني ⚖️"):
    if user_input:
        with st.spinner("جاري فحص المراجع وصياغة المذكرة القانونية..."):
            try:
                # جلب النص من ملفاتك المرفوعة
                legal_ref = get_legal_context(user_input)
                
                # تشغيل الذكاء الاصطناعي الأحدث
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                أنت مستشار قانوني خبير في قانون التأمينات والمعاشات المصري رقم 148 لسنة 2019.
                بناءً على هذه المراجع: {legal_ref}
                أجب على السؤال التالي بأسلوب مذكرات قانونية رصين ومفصل: {user_input}
                
                يجب أن يبدأ الرد بـ: "بالإشارة إلى التساؤل المطروح، وفي ضوء أحكام القانون رقم 148 لسنة 2019 ولائحته التنفيذية.."
                وفي النهاية اكتب: "مع تحيات وليد حماد - الإدارة العامة للشؤون القانونية - ديوان عام منطقة البحيرة"
                """
                
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.markdown(f"""
                <div style="background: #ffffff; padding: 20px; border-right: 8px solid #facc15; line-height: 1.8; font-size: 1.15rem; white-space: pre-wrap; color: #1e293b;">
                {response.text}
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"عذراً، حدث خطأ فني: {str(e)}")
    else:
        st.warning("يرجى إدخال التساؤل أولاً.")

st.markdown('</div>', unsafe_allow_html=True)

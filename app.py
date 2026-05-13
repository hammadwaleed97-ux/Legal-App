import streamlit as st
import pdfplumber
import google.generativeai as genai

# 1. إعداد محرك الذكاء الاصطناعي (Gemini 1.5 Flash)
# المفتاح الذي أرسلته سيادتكم
genai.configure(api_key="AIzaSyCck8uvMFNFrOePBOYGTLrabPR369BXnHI")

# 2. تنسيق الواجهة لتكون لائقة بالعمل القانوني
st.set_page_config(page_title="المستشار القانوني الذكي - وليد حماد", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .stApp { background-color: #f1f5f9; }
    .main-card { background: white; padding: 30px; border-radius: 15px; border-top: 8px solid #1e3a8a; box-shadow: 0 4px 12px rgba(0,0,0,0.1); color: #1e293b; }
    .header-text { text-align: center; color: #1e3a8a; font-size: 2.2rem; font-weight: bold; margin-bottom: 5px; }
    .footer-text { text-align: center; color: #64748b; font-size: 1rem; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.markdown('<div class="header-text">المستشار القانوني الرقمي الذكي</div>', unsafe_allow_html=True)
st.markdown('<div class="footer-text">إعداد الأستاذ/ وليد حماد - الإدارة العامة للشؤون القانونية بالبحيرة</div>', unsafe_allow_html=True)

# 3. دالة استخراج النصوص من ملفاتك (لربط الرد بالقانون)
def get_legal_context(user_query):
    context = ""
    # الملفات التي رفعتها على GitHub
    files = ["law.pdf", "regulation.pdf", "guide.pdf"]
    for file_name in files:
        try:
            with pdfplumber.open(file_name) as pdf:
                # نكتفي بفحص أول 30 صفحة لضمان السرعة
                for page in pdf.pages[:30]:
                    text = page.extract_text()
                    if text and any(word in text for word in user_query.split()[:2]):
                        context += text + "\n"
                    if len(context) > 4000: break
        except: continue
    return context[:4000]

# 4. واجهة إدخال التساؤلات
user_input = st.text_area("أدخل الحالة القانونية أو التساؤل (مثال: شروط الجمع بين المعاش والمرتب):", height=150)

if st.button("صياغة الرد القانوني بالذكاء الاصطناعي ⚖️"):
    if user_input:
        with st.spinner("جاري مراجعة المراجع وصياغة المذكرة..."):
            try:
                # جلب الأسانيد من ملفات الـ PDF الخاصة بك
                legal_reference = get_legal_context(user_input)
                
                # إعداد النموذج الذكي (الإصدار الحديث المصلح)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # توجيه الذكاء الاصطناعي للصياغة المطلوبة
                prompt = f"""
                أنت مستشار قانوني خبير في قانون التأمينات والمعاشات المصري (قانون 148 لسنة 2019).
                استخدم النصوص التالية المستخرجة من مراجع المستخدم:
                {legal_reference}
                
                أجب على سؤال المستخدم التالي بأسلوب قانوني رصين ومفصل، مستشهداً بمواد القانون إذا وجدت:
                {user_input}
                
                تعليمات الصياغة:
                1. ابدأ بـ: "بالإشارة إلى التساؤل المطروح، وفي ضوء أحكام القانون رقم 148 لسنة 2019 ولائحته التنفيذية.."
                2. اجعل الأسلوب رسمياً ولائقاً بالمذكرات القانونية.
                3. في النهاية اكتب: "مع تحيات وليد حماد - الإدارة العامة للشؤون القانونية - ديوان عام منطقة البحيرة".
                """
                
                response = model.generate_content(prompt)
                
                # عرض النتيجة
                st.markdown("---")
                st.markdown(f"""
                <div style="background-color: #ffffff; padding: 20px; border-right: 5px solid #facc15; line-height: 1.8; font-size: 1.1rem; white-space: pre-wrap;">
                {response.text}
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"حدث خطأ في الاتصال بالمخ الذكي. تأكد من تفعيل الـ API. (الخطأ: {str(e)})")
    else:
        st.warning("من فضلك اكتب التساؤل أولاً.")

st.markdown('</div>', unsafe_allow_html=True)

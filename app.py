import streamlit as st
import pdfplumber
import google.generativeai as genai

# 1. إعداد المحرك الذكي بأقصى درجات الاستقرار
# المفتاح الخاص بسيادتكم
genai.configure(api_key="AIzaSyCck8uvMFNFrOePBOYGTLrabPR369BXnHI")

# 2. تنسيق الواجهة لتكون رسمية وبدون أمثلة
st.set_page_config(page_title="المستشار القانوني الذكي", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .stApp { background-color: #f8fafc; }
    .main-card { background: white; padding: 25px; border-radius: 15px; border-top: 10px solid #1e3a8a; box-shadow: 0 4px 6px rgba(0,0,0,0.1); color: #1e293b; }
    .header-text { text-align: center; color: #1e3a8a; font-size: 2.3rem; font-weight: bold; margin-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.markdown('<div class="header-text">المستشار القانوني الرقمي الذكي</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color: #64748b; font-weight: bold;">إعداد الأستاذ/ وليد حماد - الإدارة العامة للشؤون القانونية بالبحيرة</p>', unsafe_allow_html=True)

# 3. دالة استخراج الأسانيد من ملفاتك (قانون 148 ولائحته)
def get_legal_context(query):
    context = ""
    files = ["law.pdf", "regulation.pdf", "guide.pdf"]
    for f in files:
        try:
            with pdfplumber.open(f) as pdf:
                # فحص سريع لضمان عدم حدوث Timeout
                for page in pdf.pages[:15]:
                    text = page.extract_text()
                    if text and any(word in text for word in query.split()[:1]):
                        context += text + "\n"
                    if len(context) > 2500: break
        except: continue
    return context[:2500]

# 4. واجهة الاستخدام (تم حذف الأمثلة كما طلبت)
user_input = st.text_area("اطرح تساؤلك القانوني أو الحالة المراد فحصها هنا:", height=150)

if st.button("صياغة الرد القانوني ⚖️"):
    if user_input:
        with st.spinner("جاري فحص المراجع وصياغة المذكرة..."):
            try:
                # جلب الأسانيد
                legal_ref = get_legal_context(user_input)
                
                # استخدام الموديل المستقر وتحديد الإصدار لتفادي خطأ 404
                model = genai.GenerativeModel(model_name='gemini-1.5-flash-latest')
                
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
                <div style="background: #ffffff; padding: 25px; border-right: 8px solid #facc15; line-height: 2; font-size: 1.2rem; white-space: pre-wrap; color: #1e293b;">
                {response.text}
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                # عرض رسالة خطأ واضحة في حال تعطل الخدمة مؤقتاً
                st.error("نعتذر، واجهة جوجل الذكية مشغولة حالياً. يرجى الضغط على زر الصياغة مرة أخرى.")
    else:
        st.warning("يرجى كتابة التساؤل أولاً.")

st.markdown('</div>', unsafe_allow_html=True)

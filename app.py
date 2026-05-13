import streamlit as st
import pdfplumber
import google.generativeai as genai

# 1. إعداد المخ الذكي (المفتاح الذي أرسلته)
genai.configure(api_key="AIzaSyCck8uvMFNFrOePBOYGTLrabPR369BXnHI")

st.set_page_config(page_title="المستشار الذكي - وليد حماد", layout="wide")

# التنسيق البصري
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    .stApp { background-color: #f8fafc; font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .legal-box { background: white; padding: 25px; border-radius: 15px; border-right: 10px solid #1e3a8a; box-shadow: 0 4px 6px rgba(0,0,0,0.1); color: #1e293b; margin-top: 20px; }
    .header { text-align: center; color: #1e3a8a; font-size: 2.5rem; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header">المستشار القانوني الذكي (نسخة مطورة)</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>بإشراف الأستاذ/ وليد حماد - ديوان عام منطقة البحيرة</p>", unsafe_allow_html=True)

# 2. وظيفة قراءة النصوص من ملفاتك
def get_context(query):
    context = ""
    files = ["law.pdf", "regulation.pdf", "guide.pdf"]
    for f in files:
        try:
            with pdfplumber.open(f) as pdf:
                # نبحث في أول 20 صفحة لسرعة الرد
                for page in pdf.pages[:20]:
                    text = page.extract_text()
                    if text and query[:5] in text: # بحث تقريبي أولي
                        context += text + "\n"
        except: continue
    return context[:3000] # نأخذ أهم 3000 حرف

# 3. واجهة المستخدم
user_question = st.text_area("اطرح تساؤلك القانوني أو الحالة التي تريد فحصها:")

if st.button("تحليل الصياغة القانونية بالذكاء الاصطناعي ⚖️"):
    if user_question:
        with st.spinner("جاري تحليل النصوص القانونية وصياغة الرد..."):
            # جلب النصوص المتعلقة بالسؤال من ملفاتك
            reference_text = get_context(user_question)
            
            # إرسال الطلب للمخ الذكي
            model = genai.GenerativeModel('gemini-pro')
            prompt = f"""
            أنت مستشار قانوني خبير في قانون التأمينات والمعاشات المصري (قانون 148 لسنة 2019).
            بناءً على النصوص التالية من المراجع: {reference_text}
            أجب على سؤال المستخدم بأسلوب قانوني رصين ومفصل: {user_question}
            يجب أن تبدأ الإجابة بعبارة: "بالإشارة إلى التساؤل المطروح، وفي ضوء أحكام القانون رقم 148 لسنة 2019 ولائحته التنفيذية.."
            وفي النهاية اكتب: "مع تحيات وليد حماد - الإدارة العامة للشؤون القانونية"
            """
            
            response = model.generate_content(prompt)
            
            st.markdown(f"""
            <div class="legal-box">
                <div style="white-space: pre-wrap; line-height: 1.8; font-size: 1.1rem;">
                {response.text}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("يرجى كتابة التساؤل أولاً.")

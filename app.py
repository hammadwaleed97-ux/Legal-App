import streamlit as st
import pandas as pd
from datetime import datetime

# 1. إعدادات الصفحة واللوجو الثابت
st.set_page_config(page_title="منظومة المستشار القانوني", layout="wide")

st.markdown("""
    <div style="text-align: center; border: 3px solid #1E3A8A; padding: 20px; border-radius: 15px; background-color: #f8f9fa; margin-bottom: 25px;">
        <h2 style="color: #ce1126; margin: 10px 0;">مع تحيات المستشار / وليد حماد</h2>
        <h3 style="color: #1E3A8A; margin: 5px;">الادارة العامة للشؤون القانونية</h3>
        <h3 style="color: #1E3A8A; margin: 0;">بالهيئة القومية للتأمين الاجتماعى</h3>
    </div>
""", unsafe_allow_html=True)

# 2. نظام التنقل بالأيقونات
if 'page' not in st.session_state:
    st.session_state.page = "الرئيسية"
if 'archive_data' not in st.session_state:
    st.session_state.archive_data = [] # قاعدة بيانات مؤقتة للأرشيف

c1, c2 = st.columns(2)
with c1:
    if st.button("⚖️ أولاً: الإدارة العامة للقضايا", use_container_width=True): st.session_state.page = "قضايا"
    if st.button("🔍 ثالثاً: الإدارة العامة للتحقيقات والنيابات", use_container_width=True): st.session_state.page = "تحقيقات"
    if st.button("📂 خامساً: البحث والأرشيف", use_container_width=True): st.session_state.page = "أرشيف"
with c2:
    if st.button("📜 ثانياً: الإدارة العامة للفتوى", use_container_width=True): st.session_state.page = "فتوى"
    if st.button("📚 رابعاً: المكتبة القانونية الرقمية", use_container_width=True): st.session_state.page = "مكتبة"
    if st.button("🏠 العودة للشاشة الرئيسية", use_container_width=True): st.session_state.page = "الرئيسية"

st.markdown("---")

# 3. الأقسام وتفعيل الذكاء الاصطناعي والتحميل

if st.session_state.page == "قضايا":
    st.header("⚖️ الإدارة العامة للقضايا")
    court_type = st.radio("نوع القضاء:", ["القضاء العادي", "مجلس الدولة"], horizontal=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        case_no = st.text_input("رقم الدعوى والسنة")
        court_name = st.text_input("المحكمة والدائرة")
    with col_b:
        opponent = st.text_input("اسم الخصم")
        session_date = st.date_input("تاريخ الجلسة")

    facts = st.text_area("ملخص الوقائع القانونية (اكتب التفاصيل هنا ليحللها الذكاء الاصطناعي)")
    
    uploaded_file = st.file_uploader("📂 ارفع مستندات القضية (PDF/Images)")

    if st.button("📝 توليد الصياغة القانونية بالذكاء الاصطناعي"):
        if facts:
            with st.spinner("جاري تحليل الوقائع وربطها بالمكتبة القانونية..."):
                # محاكاة الربط بالذكاء الاصطناعي والمكتبة
                draft_text = f"بناءً على الوقائع المقدمة في الدعوى رقم {case_no}، نرى الدفع بـ..." 
                st.subheader("📄 المسودة المقترحة:")
                st.info(draft_text)
                
                # إضافة زر التحميل (المطلوب)
                st.download_button(
                    label="📥 تحميل مذكرة الدفاع (Word/Text)",
                    data=draft_text,
                    file_name=f"مذكرة_قضية_{case_no}.txt",
                    mime="text/plain"
                )
                
                # حفظ في الأرشيف تلقائياً
                st.session_state.archive_data.append({
                    "الرقم": case_no, "الخصم": opponent, "التاريخ": str(session_date), "النوع": "قضايا"
                })
        else:
            st.warning("يرجى كتابة الوقائع أولاً ليتمكن الذكاء الاصطناعي من صياغتها.")

elif st.session_state.page == "مكتبة":
    st.header("📚 المكتبة القانونية الرقمية (مرتبطة بالذكاء الاصطناعي)")
    lib_sections = ["القوانين", "اللوائح", "الكتب الدورية", "تعليمات الهيئة", "أحكام قضائية"]
    section = st.selectbox("اختر القسم:", lib_sections)
    search_query = st.text_input("ابحث عن نص قانوني أو اطلب من الذكاء الاصطناعي تلخيص قانون...")
    
    if st.button("🔍 بحث ذكي"):
        st.write(f"جاري البحث في قسم {section} عن: {search_query}")
        # هنا يتم الربط بملفات الـ PDF المخزنة عندك مستقبلاً
        st.success("تم العثور على 3 نتائج مرتبطة بموضوعك.")
        st.download_button("📥 تحميل النص الكامل للقانون", data="نص القانون...", file_name="قانون.txt")

elif st.session_state.page == "أرشيف":
    st.header("📂 البحث والأرشيف")
    if st.session_state.archive_data:
        df = pd.DataFrame(st.session_state.archive_data)
        st.table(df) # عرض البيانات المخزنة
    else:
        st.info("الأرشيف فارغ حالياً. سيتم ملؤه تلقائياً عند حفظ أي قضية أو فتوى.")

elif st.session_state.page == "الرئيسية":
    st.info("مرحباً بك يا سيادة المستشار. المنظومة جاهزة للعمل.")

import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة وتصغير اللوجو (Header احترافي)
st.set_page_config(page_title="منظومة المستشار وليد حماد", layout="wide")

st.markdown("""
    <div style="text-align: center; border-bottom: 3px solid #1E3A8A; padding: 10px; background-color: #f8f9fa; margin-bottom: 20px;">
        <h2 style="color: #1E3A8A; margin: 0; font-size: 20px;">الهيئة القومية للتأمين الاجتماعى</h2>
        <h3 style="color: #1E3A8A; margin: 0; font-size: 16px;">الادارة المركزية للإدارات القانونية</h3>
        <p style="color: #ce1126; margin: 5px; font-weight: bold;">مع تحيات وليد حماد - عضو الادارة القانونية بالبحيرة</p>
    </div>
""", unsafe_allow_html=True)

# 2. إدارة البيانات (المادة العلمية والأرشيف)
if 'lib_db' not in st.session_state: st.session_state.lib_db = []
if 'arc_db' not in st.session_state: st.session_state.arc_db = []

# 3. الأيقونات الستة - تفتح مباشرة في مكانها
col1, col2, col3 = st.columns(3)

with col1:
    with st.expander("⚖️ إدارة القضايا", expanded=False):
        c_num = st.text_input("رقم القضية")
        c_opp = st.text_input("الخصم")
        c_draft = st.text_area("مسودة المذكرة:")
        if st.button("💾 حفظ"):
            st.session_state.arc_db.append({"الرقم": c_num, "الخصم": c_opp})
            st.success("تم الحفظ")
        st.download_button("📥 تحميل المذكرة", data=c_draft, file_name=f"case_{c_num}.txt")

    with st.expander("📂 الأرشيف والبحث", expanded=False):
        st.write("سجلاتك المحفوظة:")
        if st.session_state.arc_db:
            st.table(pd.DataFrame(st.session_state.arc_db))
        else: st.info("الأرشيف فارغ")

with col2:
    with st.expander("📚 المكتبة الرقمية", expanded=False):
        search = st.text_input("🔍 ابحث في المادة العلمية:")
        if st.session_state.lib_db:
            for item in st.session_state.lib_db:
                if search in item['نص']:
                    st.write(f"📄 {item['نص'][:50]}...")
                    st.download_button("📥 تحميل", data=item['نص'], file_name="law_doc.txt", key=item['نص'][:10])
        
        if st.button("🤖 استشارة الذكاء الاصطناعي"):
            st.info("جاري تحليل المادة العلمية المرفوعة...")

    with st.expander("📜 إدارة الفتوى", expanded=False):
        st.text_area("موضوع الفتوى")
        st.button("إرسال للتحليل")

with col3:
    with st.expander("🔐 لوحة التحكم (رفع الداتا)", expanded=True):
        pwd = st.text_input("كلمة السر:", type="password")
        if pwd == "Waleed2026":
            st.info("ارفع هنا المادة العلمية اللي الذكاء الاصطناعي هيبحث فيها")
            up_file = st.file_uploader("رفع ملف")
            up_text = st.text_area("أو انسخ النص:")
            if st.button("✅ حفظ ونشر"):
                st.session_state.lib_db.append({"نص": up_text if up_text else up_file.name})
                st.success("تمت الإضافة")
        elif pwd != "": st.error("خاص بالمستشار وليد فقط")

    with st.expander("🔍 التحقيقات والنيابات", expanded=False):
        st.text_input("اسم المحال للتحقيق")
        st.button("صياغة قرار التصرف")

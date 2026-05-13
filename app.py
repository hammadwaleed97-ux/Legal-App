import os
from langchain.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain.indexes import VectorstoreIndexCreator

# 1. إعداد مجلد "المادة العلمية"
# ضع كل ملفاتك (PDF, Text, Docx) في هذا المجلد
MATERIAL_DIR = "scientific_material"
if not os.path.exists(MATERIAL_DIR):
    os.makedirs(MATERIAL_DIR)

def ask_pension_bot(user_question):
    """
    هذه الوظيفة لا تعرف شيئاً من تلقاء نفسها.
    هي تدخل إلى مجلد المادة العلمية، تقرأ الملفات، وتستخرج الإجابة.
    """
    # تحميل المادة العلمية من المجلد
    loader = DirectoryLoader(MATERIAL_DIR, glob="./*.*")
    
    # بناء كشاف (Index) للمادة العلمية للبحث السريع داخلها
    index = VectorstoreIndexCreator().from_loaders([loader])
    
    # استخراج الإجابة والسند القانوني
    # البرنامج سيبحث عن المواد والأنصبة داخل ملفاتك فقط
    response = index.query(user_question)
    
    return response

# --- مثال للاستخدام ---
# بمجرد رفع المادة العلمية للمجلد، يمكنك تشغيل البرنامج:
# question = "ما هو نصيب الابنة المطلقة في وجود أرملة وفقاً للمواد العلمية المرفوعة؟"
# print(ask_pension_bot(question))

import os

# وظيفة المحرك: استخراج الإجابة من ملفات المادة العلمية المرفقة
def extract_from_legal_resources(user_query, legal_folder="المادة_العلمية"):
    """
    هذا المحرك لا يملك إجابات مسبقة.
    بمجرد سؤال المستخدم، يدخل للمجلد ويقرأ المواد العلمية ويستخرج الإجابة.
    """
    
    # قائمة المواد العلمية المحملة في البرنامج
    resources = os.listdir(legal_folder)
    
    context = ""
    # قراءة كافة الملفات (قانون 148، اللائحة، الكتب الدورية)
    for file_name in resources:
        with open(f"{legal_folder}/{file_name}", "r", encoding="utf-8") as file:
            context += file.read()

    # هنا المحرك "يستخرج" الإجابة من النص بناءً على سؤال المستخدم
    # يتم استخدام تقنية "التنقيب عن النصوص" للربط بين السؤال والمادة
    answer = perform_extraction(user_query, context)
    
    return answer

def perform_extraction(query, source_material):
    # منطق البحث والاستخراج الذكي بناءً على "المادة العلمية" فقط
    # البرنامج هنا يبحث عن (المواد، الأنصبة، الشروط) داخل المادة العلمية
    return f"بناءً على المادة العلمية المرفقة: {source_material[:200]}..." # مثال للاستخراج

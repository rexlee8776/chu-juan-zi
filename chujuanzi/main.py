from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import json

# 加载题库 JSON 文件
file_path_with_types = "./tiku.json"
with open(file_path_with_types, "r", encoding="utf-8") as file:
    questions = json.load(file)

# PDF 文件路径
output_pdf = "printable_exam.pdf"

# 样式
styles = getSampleStyleSheet()

# 创建 PDF
doc = SimpleDocTemplate(output_pdf, pagesize=A4)
elements = []

# 添加标题
title = Paragraph("自动生成的试卷", styles['Title'])
elements.append(title)
elements.append(Spacer(1, 20))

# 遍历题目并生成内容
for question in questions:
    if question["type"] == "选择题":
        # 添加选择题
        q_text = f"{question['id']}. {question['question']}"
        elements.append(Paragraph(q_text, styles['Normal']))
        options = question.get("options", [])
        for opt in options:
            elements.append(Paragraph(opt, styles['Normal']))
        elements.append(Spacer(1, 15))
    elif question["type"] == "填空题":
        # 添加填空题
        q_text = f"{question['id']}. {question['question']}"
        elements.append(Paragraph(q_text, styles['Normal']))
        elements.append(Spacer(1, 15))

# 添加页脚或其他内容
elements.append(Spacer(1, 50))
footer = Paragraph("请认真答题，祝考试顺利！", styles['Italic'])
elements.append(footer)

# 生成 PDF
doc.build(elements)

print(f"试卷生成完成：{output_pdf}")
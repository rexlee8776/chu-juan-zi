from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors

import json

JZ_TITLE = "天数智芯2025届应届生招聘笔试"

# 注册中文字体
pdfmetrics.registerFont(TTFont('SimSun', 'c:/windows/fonts/SimSun.ttc'))  # SimSun.ttc 是宋体字体文件，请确保路径正确
# pdfmetrics.registerFont(TTFont('SimSunBold', 'c:/windows/fonts/simsunb.ttf'))


# 自定义样式（中文支持）
# 对齐说明：["left", "center", "centre", "right", "justify"]
styles = {
    'title': ParagraphStyle(
        'title',
        fontName='SimSun',
        fontSize=16,
        leading=22,
        alignment=1,  # 居中
        spaceAfter=20,
    ),
    'normal': ParagraphStyle(
        'normal',
        fontName='SimSun',
        fontSize=10.5,
        leading=18,
        alignment=0,
    ),
    'code': ParagraphStyle(
        'code',
        fontName='Courier',
        fontSize=10.5,
        leading=10,
        alignment=0,
    ),
    'normal_indent': ParagraphStyle(
        'normal_indent',
        fontName='SimSun',
        fontSize=10.5,
        leading=18,
        alignment=0,
        leftIndent=17.0,
    ),
    'title_2': ParagraphStyle(
        'title_2',
        fontName='SimSun',
        fontSize=12,
        leading=18,
        alignment=0,
    ),
}

# 加载题库 JSON 文件
file_path_with_types = "./tiku.json"
with open(file_path_with_types, "r", encoding="utf-8") as file:
    questions = json.load(file)

# PDF 文件路径
output_pdf = "juanzi.pdf"

# 创建 PDF
doc = SimpleDocTemplate(output_pdf, pagesize=A4)
elements = []

# 添加标题
title = Paragraph(JZ_TITLE, styles['title'])
elements.append(title)

elements.append(Paragraph("一、 选择题（每题 2 分，共 40 分）", styles['title_2']))
for question in [q for q in questions if q["type"] == "选择题"]:
    # 添加选择题
    q_text = f"{question['id']}. {question['question']}"
    elements.append(Paragraph(q_text, styles['normal']))
    options = question.get("options", [])
    for opt in options:
        elements.append(Paragraph(opt, styles['normal_indent']))
    elements.append(Spacer(1, 15))

elements.append(Paragraph("二、 填空题（每题 4 分，共 20 分）", styles['title_2']))
for question in [q for q in questions if q["type"] == "填空题"]:
    # 添加填空题
    q_text = f"{question['id']}. {question['question']}"
    elements.append(Paragraph(q_text, styles['normal']))
    elements.append(Spacer(1, 15))

# # 遍历题目并生成内容
# for question in questions:
#     if question["type"] == "选择题":
#         # 添加选择题
#         q_text = f"{question['id']}. {question['question']}"
#         elements.append(Paragraph(q_text, styles['normal']))
#         options = question.get("options", [])
#         for opt in options:
#             elements.append(Paragraph(opt, styles['normal']))
#         elements.append(Spacer(1, 15))
#     elif question["type"] == "填空题":
#         # 添加填空题
#         q_text = f"{question['id']}. {question['question']}"
#         elements.append(Paragraph(q_text, styles['normal']))
#         elements.append(Spacer(1, 15))

# 试着加代码
code = """
#include <stdio.h>
#include <stdlib.h>

int main() {
    int *p = (int *)malloc(4 * sizeof(int));
    if (!p) {
        printf("Memory allocation failed\n");
        return 1;
    }
    for (int i = 0; i < 4; i++) {
        *(p + i) = i * 10;
    }
    int *q = realloc(p, 2 * sizeof(int));
    if (!q) {
        printf("Reallocation failed\n");
        free(p);
        return 1;
    }
    free(q);
    return 0;
}
"""

formatted_code = code.replace(" ", "&nbsp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>")
elements.append(Paragraph(f"<pre>{formatted_code}</pre>", styles['code']))

# 添加页脚或其他内容
elements.append(Spacer(1, 50))
footer = Paragraph("请认真答题，祝考试顺利！", styles['normal'])
elements.append(footer)

# 生成 PDF
doc.build(elements)

print(f"试卷生成完成：{output_pdf}")

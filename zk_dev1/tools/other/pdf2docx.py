# 方法1
from pdf2docx import parse


pdf_file = r'D:\MyInfo_file\全栈自动化测试课程.pdf'
docx_file = r'D:\MyInfo_file\全栈自动化测试课程11..docx'

# convert pdf to docx
parse(pdf_file, docx_file)

# --------------------------------------------- 方法2

# import pdfplumber
# from docx import Document
#
# # 打开pdf文件
# with pdfplumber.open(r'D:\MyInfo_file\全栈自动化测试课程.pdf') as pdf:
#     # 创建一个空的word文档
#     doc = Document()
#     # 遍历pdf中的每一页
#     for page in pdf.pages:
#         # 获取当前页的文本内容
#         text = page.extract_text()
#         # 将文本内容添加到word文档中
#         doc.add_paragraph(text)
#     # 保存word文档
#     doc.save(r'D:\MyInfo_file\全栈自动化测试课程22..docx')






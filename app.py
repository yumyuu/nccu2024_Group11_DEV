# import streamlit as st
# import os
# import tempfile
# from pptx import Presentation
# from pptx.util import Inches, Pt
# from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
# from PyPDF2 import PdfReader
# import google.generativeai as genai

# # 配置 Google Gemini API
# genai.configure(api_key='AIzaSyADv9y5ye8btqr12Wlwo7FD-pPJBUMMc_A')
# # 到 https://ai.google.dev/gemini-api/docs/api-key 申請 API Key
# model = genai.GenerativeModel(model_name='gemini-1.5-flash') # 選擇模型

# # ======== 功能函數 ========

# def read_pdf(pdf_path):
#     """讀取 PDF 並合併所有頁面的文字內容"""
#     reader = PdfReader(pdf_path)
#     text = ""
#     for page in reader.pages:
#         text += page.extract_text()
#     return text

# def get_title(text, top_text=500):
#     """使用 Google Gemini API 生成標題"""
#     prompt = f"只給我這篇論文的標題：\n\n{text[:top_text]}"
#     try:
#         response = model.generate_content(prompt)
#         return response.text.strip()
#     except Exception as e:
#         st.error(f"生成標題時出错：{e}")
#         return "未能生成"

# def generate_pdf_summary_and_details(pdf_text):
#     """使用 Google Gemini API 生成 PDF 條列摘要與詳細重點整理"""
#     summary_prompt = f"summary_prompt = 請為以下論文文本生成條列式摘要，每點以「-」開頭。請確保每個要點清晰、具體並且包含文檔中的關鍵信息，要求每項要點必須要30 字以上。\n{pdf_text[:2500]}"
#     details_prompt = f"請為以下論文文本生成更詳細的英文重點整理，
#     ，每個部分的重點整理應該包括以下內容:
#     1. **背景**：簡要介紹文檔的背景，解釋問題的起源和研究的目的。
#     2. **方法**：詳細描述文檔中使用的研究方法或分析技巧。
#     3. **結果**：呈現研究的主要結果，並詳細描述每個發現的具體細節。
#     4. **結論與討論**：分析結果的意涵，並討論研究的貢獻、局限性，以及未來研究的方向。
#     每個部分的描述應該詳盡且具體，避免簡單概括，要求更多的上下文和分析，幫助讀者深入理解文檔的精髓。：\n\n{pdf_text[:2000]}"
#     try:
#         summary_response = model.generate_content(summary_prompt)
#         summary = summary_response.text.strip() if summary_response else "未能生成摘要。"

#         details_response = model.generate_content(details_prompt)
#         details = details_response.text.strip() if details_response else "未能生成重點整理。"

#         return summary, details
#     except Exception as e:
#         st.error(f"生成摘要與詳細時發生錯誤：{e}")
#         return "未能生成摘要。", "未能生成詳細重點整理。"

# def generate_image_description(image_path):
#     """使用 Google Gemini API 上傳圖片並生成描述"""

#     myfile = genai.upload_file(image_path)
#     prompt = "請為下圖片生成總共40英文字以內簡短且完整的描述。圖片可能包含各種類型（如圖表、流程圖、模型架構或數據表格）："
#     result = model.generate_content([myfile, "\n\n", prompt])
#     return result.text.strip() if result else f"未能生成圖片描述：{image_path}"


# # def add_image_and_description_to_slide(prs, image_path, description, max_chars_per_slide=400):
# #     """為每張圖片添加解說內容到單獨的幻燈片"""
# #     description_pages = [description[i:i + max_chars_per_slide] for i in range(0, len(description), max_chars_per_slide)]

# #     for page_num, page_content in enumerate(description_pages):
# #         slide_layout = prs.slide_layouts[5]
# #         slide = prs.slides.add_slide(slide_layout)

# #         # 添加圖片
# #         if image_path and os.path.exists(image_path):
# #             slide.shapes.add_picture(image_path, Inches(0.5), Inches(0.5), Inches(8), Inches(4.5))

# #         # 添加文字框
# #         text_box = slide.shapes.add_textbox(Inches(0.5), Inches(5.2), Inches(8), Inches(2))
# #         text_frame = text_box.text_frame
# #         text_frame.clear()
# #         text_frame.word_wrap = True
# #         text_frame.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT
# #         p = text_frame.add_paragraph()
# #         p.text = page_content.strip()
# #         p.font.size = Pt(16)
# #         p.line_spacing = Pt(20)
# #         text_frame.vertical_anchor = MSO_ANCHOR.TOP

# def add_image_and_description_to_slide(prs, image_path, description):
#     """為每張圖片添加解釋內容到單獨的幻燈片"""
#     slide_layout = prs.slide_layouts[5]
#     slide = prs.slides.add_slide(slide_layout)

#     if image_path and os.path.exists(image_path): # 這裡是圖片位置
#         left = Inches(0.9)
#         top = Inches(0.2)
#         width = Inches(8)
#         height = Inches(4.0)
#         slide.shapes.add_picture(image_path, left, top, width=width, height=height)
  
#     #description = truncate_description(description, max_chars_per_line, max_lines)
#     text_box = slide.shapes.add_textbox(Inches(0.4), Inches(4.5), Inches(8), Inches(1.0))# 添加解釋文字
#     text_frame = text_box.text_frame
#     text_frame.word_wrap = True
#     text_frame.text = description

#     for paragraph in text_frame.paragraphs:# 設置文字格式
#         paragraph.font.size = Pt(14)
#         paragraph.alignment = PP_ALIGN.LEFT

# # def add_text_slide(prs, title, content, bullet=False, font_size=20, max_chars_per_slide=800):
# #     """添加純文字幻燈片，支持分頁"""
# #     content_pages = [content[i:i + max_chars_per_slide] for i in range(0, len(content), max_chars_per_slide)]

# #     for page_num, page_content in enumerate(content_pages):
# #         slide_layout = prs.slide_layouts[1]
# #         slide = prs.slides.add_slide(slide_layout)
# #         slide.shapes.title.text = f"{title}（第 {page_num + 1} 部分）"
# #         text_box = slide.placeholders[1]
# #         text_frame = text_box.text_frame
# #         text_frame.clear()

# #         if bullet:
# #             for line in page_content.split("\n"):
# #                 p = text_frame.add_paragraph()
# #                 p.text = line.strip()
# #                 p.font.size = Pt(font_size)
# #         else:
# #             text_frame.text = page_content
# #             for paragraph in text_frame.paragraphs:
# #                 paragraph.font.size = Pt(font_size)
# #                 paragraph.alignment = PP_ALIGN.LEFT
# def add_text_slide(prs, title, content, bullet=False, font_size=20):
#     """新增一個純文字投影片"""
#     # 使用空白的投影片佈局（無預設標題框和內容框）
#     slide_layout = prs.slide_layouts[5]
#     slide = prs.slides.add_slide(slide_layout)

#     # 添加標題框，並設定位置與大小
#     title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(8), Inches(1))  # 標題位置
#     title_frame = title_box.text_frame
#     title_frame.text = title  # 設定標題文字
#     for paragraph in title_frame.paragraphs:
#         paragraph.font.size = Pt(font_size + 4)  # 標題字體大小（比內容稍大）
#         paragraph.alignment = PP_ALIGN.LEFT  # 左對齊

#     # 如果內容為空，新增一個標示頁面為空白的文字框
#     if not content.strip():
#         text_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(8), Inches(5))  # 文字框位置
#         text_frame = text_box.text_frame
#         text_frame.text = "(此頁為空白)"  # 顯示空白頁的提示文字
#         for paragraph in text_frame.paragraphs:
#             paragraph.font.size = Pt(font_size)  # 設定字體大小
#             paragraph.alignment = PP_ALIGN.CENTER  # 置中對齊
#         return

#     # 添加內容文字框，設定位置與大小
#     text_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(8), Inches(5))  # 調整內容框位置與大小
#     text_frame = text_box.text_frame
#     text_frame.word_wrap = True  # 啟用自動換行
#     text_frame.clear()  # 清空框內的預設內容

#     if bullet:
#         # 條列式內容處理
#         for line in content.split("\n"):  # 逐行處理文字內容
#             if line.strip():  # 確保行不為空
#                 p = text_frame.add_paragraph()  # 新增段落
#                 p.text = f"{line.strip()}。"  # 加入條列項目，並自動添加句號
#                 p.font.size = Pt(font_size)  # 設定字體大小
#                 text_frame.add_paragraph()  # 添加段行（換行）
#     else:
#         # 普通段落處理
#         formatted_content = content.replace("\n", "。\n\n\n")  # 將換行視為段落，並加入句號與段行
#         p = text_frame.add_paragraph()
#         p.text = formatted_content  # 設定段落文字內容
#         p.font.size = Pt(font_size)  # 設定字體大小

#     # 調整內容的文字對齊方式
#     for paragraph in text_frame.paragraphs:
#         paragraph.alignment = PP_ALIGN.LEFT  # 左對齊

# def create_presentation(pdf_path, image_folder):
#     """
#     根據 PDF 和圖片生成 PPT，包含摘要、詳細整理與圖片解釋。返回生成的 PPT 文件名。
#     """
#     prs = Presentation()

#     pdf_text = read_pdf(pdf_path)
#     title = get_title(pdf_text)
#     # 添加標題頁
#     slide_layout = prs.slide_layouts[0]
#     slide = prs.slides.add_slide(slide_layout)
#     adjust_title_font(slide, title if title else "未能提取標題")

#     summary, details = generate_pdf_summary_and_details(pdf_text)

#     # 動態分頁處理摘要
#     summary_chunks = split_text_by_points(summary, points_per_slide=3)
#     for i, chunk in enumerate(summary_chunks):
#         # 合併 chunk 為字串
#         chunk_text = "\n".join(chunk)
#         add_text_slide(prs, f"PDF 條列摘要（第 {i+1} 部分）", chunk_text, bullet=True, font_size=24)

#     # 詳細整理部分按照條列數分頁顯示
#     details_points = split_text_by_points(details, points_per_slide=2)
#     for i, points in enumerate(details_points):
#         page_content = "\n".join(points)
#         add_text_slide(prs, f"PDF 詳細整理（第 {i+1} 部分）", page_content, bullet=False, font_size=18)

#     flattened_summary = [item for chunk in summary_chunks for item in chunk]
#     #save_summary_as_markdown(flattened_summary)

#     # 處理圖片生成描述
#     images = [
#         os.path.join(image_folder, img)
#         for img in os.listdir(image_folder)
#         if img.endswith(('.png', '.jpg', '.jpeg'))
#     ]
#     images.sort()

#     for i, image_path in enumerate(images):
#         description = generate_image_description(image_path)
#         add_image_and_description_to_slide(prs, image_path, description)

#     output_path = 'pdf_and_images_analysis.pptx'
#     prs.save(output_path)
#     return output_path

# def split_text_by_points(text, points_per_slide=2):
#     """根據條列數分割文本"""
#     # 如果 text 是列表，將其轉換為字串
#     if isinstance(text, list):
#         text = "\n".join(text)
        
#     points = [line.strip() for line in text.split("\n") if line.strip()]
#     return [points[i:i + points_per_slide] for i in range(0, len(points), points_per_slide)]
# # def create_presentation(pdf_path, image_paths):
# #     """根據 PDF 和圖片生成 PPT，返回 PPT 檔案的路徑"""
# #     pdf_text = read_pdf(pdf_path)
# #     title = get_title(pdf_text)
# #     summary, details = generate_pdf_summary_and_details(pdf_text)

# #     prs = Presentation()
# #     slide_layout = prs.slide_layouts[0]
# #     slide = prs.slides.add_slide(slide_layout)
# #     slide.shapes.title.text = title
# #     slide.placeholders[1].text = "由 Paper Helper 生成的內容"

# #     add_text_slide(prs, "PDF 條列摘要", summary, bullet=True, font_size=20)
# #     add_text_slide(prs, "PDF 詳細整理", details, bullet=False, font_size=18)

# #     for image_path in image_paths:
# #         description = generate_image_description(image_path)
# #         add_image_and_description_to_slide(prs, image_path, description)

# #     output_path = os.path.join(tempfile.gettempdir(), f"{title}_presentation.pptx")
# #     prs.save(output_path)
# #     return output_path

# def adjust_title_font(slide, title):
#     """根據標題長度自動調整字體大小"""
#     max_length = 50  # 假設超過 50 個字符需要調整字體
#     font_size = Pt(42) if len(title) <= max_length else Pt(36)  # 根據長度調整
#     title_shape = slide.shapes.title
#     title_shape.text = title
#     for paragraph in title_shape.text_frame.paragraphs:
#         paragraph.font.size = font_size
# # ======== Streamlit Web App ========

# st.markdown(
#     """
#     <style>
#     .main-title {
#         text-align: center;
#         font-size: 36px;
#         color: #4CAF50;
#     }
#     .sub-title {
#         text-align: center;
#         font-size: 18px;
#         color: #555;
#     }
#     .upload-section {
#         padding: 20px;
#         background: #f9f9f9;
#         border-radius: 10px;
#         margin-bottom: 20px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# st.markdown('<h1 class="main-title">Paper Helper: Your Presentation Partner</h1>', unsafe_allow_html=True)
# st.markdown('<p class="sub-title">Upload your PDF and images to generate a stunning slides!</p>', unsafe_allow_html=True)

# # 上傳區域
# st.markdown('<div class="upload-section">', unsafe_allow_html=True)
# uploaded_pdf = st.file_uploader("選擇 PDF 文件", type=["pdf"])
# uploaded_images = st.file_uploader("選擇圖片（可多選）", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
# st.markdown('</div>', unsafe_allow_html=True)

# if uploaded_pdf and uploaded_images and st.button("生成 PPT"):
#     with st.spinner("正在生成簡報，請稍候..."):
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
#             temp_pdf.write(uploaded_pdf.read())
#             temp_pdf_path = temp_pdf.name

#         image_paths = []
#         for uploaded_image in uploaded_images:
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_image:
#                 temp_image.write(uploaded_image.read())
#                 image_paths.append(temp_image.name)

#         ppt_path = create_presentation(temp_pdf_path, image_paths)
#         st.success("簡報已生成 🎉")

#         with open(ppt_path, "rb") as ppt_file:
#             st.download_button(
#                 label="下載簡報",
#                 data=ppt_file,
#                 file_name=os.path.basename(ppt_path),
#                 mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
#             )
from flask import Flask, request, jsonify, send_file, render_template
import os
import tempfile
from ppt_generator import create_presentation

app = Flask(__name__)

# 創建臨時存儲文件的資料夾
UPLOAD_FOLDER = tempfile.mkdtemp()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    """
    主頁提供文件上傳的界面
    """
    return render_template('index.html')

@app.route('/generate_ppt', methods=['POST'])
def generate_ppt():
    """
    接收 PDF 和圖片，生成 PPT 並提供下載
    """
    # 確保文件已上傳
    if 'pdf' not in request.files:
        return jsonify({"error": "請上傳 PDF 文件"}), 400

    pdf_file = request.files['pdf']
    if not pdf_file.filename.endswith('.pdf'):
        return jsonify({"error": "無效的 PDF 文件"}), 400

    # 保存 PDF 文件
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
    pdf_file.save(pdf_path)

    # 保存圖片文件
    image_folder = os.path.join(app.config['UPLOAD_FOLDER'], "images")
    os.makedirs(image_folder, exist_ok=True)

    if 'images' in request.files:
        images = request.files.getlist('images')
        for image in images:
            if image.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(image_folder, image.filename)
                image.save(image_path)

    # 調用 PPT 生成邏輯
    try:
        ppt_file_path = create_presentation(pdf_path, image_folder)
        return send_file(ppt_file_path, as_attachment=True, download_name="presentation.pptx")
    except Exception as e:
        return jsonify({"error": f"生成 PPT 時出錯：{str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
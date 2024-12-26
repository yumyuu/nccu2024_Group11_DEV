from flask import Flask, request, jsonify, render_template, send_from_directory
import os
# from testpptx import create_presentation 
import ppt_generator as g
import utils as u

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'  # 上傳的檔案儲存目錄
OUTPUT_FOLDER = 'outputs'  # 生成的檔案儲存目錄
STATIC_FOLDER = 'static'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER

# 主頁面
@app.route('/')
def index():
    return render_template('index.html')  # 前端頁面

# 處理 PDF 檔案上傳
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf_file' not in request.files:
        return jsonify({'error': '未提供檔案'}), 400
    
    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return jsonify({'error': '未選擇檔案'}), 400
    
    # 儲存上傳的檔案
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
    pdf_file.save(pdf_path)
    
    try:
        # 讀取 PDF 內容並提取標題
        pdf_text = u.read_pdf(pdf_path)
        title = u.get_title(pdf_text)

        # 指定圖片目錄（這裡使用預設目錄）
        image_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'images')  
        os.makedirs(image_folder, exist_ok=True)

        # 呼叫 PPT 生成程式
        ppt_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{os.path.splitext(pdf_file.filename)[0]}.pptx")
        g.create_presentation(pdf_path, image_folder)

        # 生成 Markdown 檔案
        md_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{os.path.splitext(pdf_file.filename)[0]}.md")
        summary = "這是摘要範例。"  # 假設已有摘要，後續可替換為實際邏輯
        with open(md_path, "w", encoding="utf-8") as md_file:
            md_file.write(summary)
        
        # 回傳結果
        return jsonify({
            'message': '檔案處理成功',
            'title': title,
            'ppt_url': f'/download/{os.path.basename(ppt_path)}',
            'md_url': f'/download/{os.path.basename(md_path)}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 提供生成檔案的下載功能
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

@app.route('/generate_ppt', methods=['POST'])
@app.route('/generate_ppt', methods=['POST'])
def generate_ppt():
    """接收 PDF 和可選圖片，生成 PPT 並返回下載 URL 和教授問答"""
    if 'pdf' not in request.files:
        return jsonify({"error": "請上傳 PDF 文件"}), 400

    pdf_file = request.files['pdf']
    if not pdf_file.filename.endswith('.pdf'):
        return jsonify({"error": "無效的 PDF 文件"}), 400

    # 保存 PDF 文件到 UPLOAD_FOLDER
    upload_folder = app.config['UPLOAD_FOLDER']
    pdf_path = os.path.join(upload_folder, pdf_file.filename)
    pdf_file.save(pdf_path)

    # 處理可選的圖片
    image_folder = os.path.join(upload_folder, "images")
    os.makedirs(image_folder, exist_ok=True)

    if 'images' in request.files:
        images = request.files.getlist('images')
        for image in images:
            if image.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(image_folder, image.filename)
                image.save(image_path)
            else:
                print(f"跳過不支持的圖片類型: {image.filename}")

    try:
        # 生成 PPT 文件
        ppt_file_path = g.create_presentation(pdf_path, image_folder)
        
        # 保存到 OUTPUT_FOLDER
        output_folder = app.config['OUTPUT_FOLDER']
        unique_name = u.get_unique_filename(os.path.basename(ppt_file_path))
        ppt_output_path = os.path.join(output_folder, unique_name)
        os.rename(ppt_file_path, ppt_output_path)

        # 複製到 STATIC_FOLDER 供前端使用
        static_folder = app.config['STATIC_FOLDER']
        ppt_static_path = os.path.join(static_folder, unique_name)
        os.rename(ppt_output_path, ppt_static_path)

        ppt_file_url = f"/static/{unique_name}"

        # 生成教授問答
        pdf_text = u.read_pdf(pdf_path)
        questions = u.generate_professor_questions(pdf_text)
        print("PPT URL:", ppt_file_url)
        print("Questions:", questions)
        return jsonify({
            "ppt_url": ppt_file_url,
            "questions": questions[:3] if isinstance(questions, list) else []
        })
    except Exception as e:
        print(f"生成 PPT 或問答時發生錯誤：{e}")
        return jsonify({"error": f"生成 PPT 或問答時出錯：{str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)

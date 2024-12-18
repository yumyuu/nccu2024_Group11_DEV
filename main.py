import ppt_generator as p

def main(pdf_path, image_folder):
    try:
        ppt_file = p.create_presentation(pdf_path, image_folder)
        return f"PPT 已生成: {ppt_file}"
    except Exception as e:
        return f"生成 PPT 時發生錯誤: {e}"

if __name__ == "__main__":
    pdf_path = r"D:\Paper\Bird-eye-views.pdf" # pdf 路徑
    image_folder = r"D:\llama3\code\images" # img 路徑
    result = main(pdf_path, image_folder)
    print(result)
    print('end')
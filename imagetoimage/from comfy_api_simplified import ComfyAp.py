from comfy_api_simplified import ComfyApiWrapper, ComfyWorkflowWrapper

# 创建API包装器，使用你的ComfyUI URL（如果需要，添加用户名和密码参数）
api = ComfyApiWrapper("http://127.0.0.1:8188/")

# 创建工作流包装器，使用你下载的API格式工作流
wf = ComfyWorkflowWrapper("workflow_api.json")

# 用户输入的风格编号
print("Please select a style that you like: 1. Wassily Kandinsky, 2. Pablo Picasso, 3. Keith Haring")
style_choice = input("input the number（1/2/3）：")

# 根据风格编号设置不同的文本提示
style_prompts = {
    '1': "Abstract | Futuristic | Experimental | Contemporary art | Jazz album | Kandinsky | Mysterious",
    '2': "Abstract | Futuristic | Experimental | Contemporary art | Jazz album | Pablo Picasso | Mysterious",
    '3': "Abstract | Futuristic | Experimental | Contemporary art | Jazz album | Keith Haring | Mysterious"
}

prompt_text = style_prompts.get(style_choice)
if not prompt_text:
    print("Invalid style input number")
    exit()

# 修改工作流中的文本提示节点
wf.set_node_param("Positive", "text", prompt_text)

# 将本地图像文件上传到ComfyUI
image_path = "image_2.png"  # 确保这个路径是正确的，并且文件存在于这个路径
try:
    with open(image_path, 'rb') as image_file:
        api.upload_image(image_path, image_file)  # 传递文件名和文件对象
except Exception as e:
    print(f"An error occurred while uploading the image: {e}")

# 队列工作流以完成
try:
    results = api.queue_and_wait_images(wf, "Save Image")
    for filename, image_data in results.items():
        with open(f"{filename}", "wb+") as f:
            f.write(image_data)
            
except Exception as e:
    print(f"An error occurred while processing the workflow: {e}")
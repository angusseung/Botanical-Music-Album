from comfy_api_simplified import ComfyApiWrapper, ComfyWorkflowWrapper
import streamlit as st


def generate(ref_image, caption):
    # 创建API包装器，使用你的ComfyUI URL（如果需要，添加用户名和密码参数）
    api = ComfyApiWrapper("http://127.0.0.1:8188/")

    # 创建工作流包装器，使用你下载的API格式工作流
    wf = ComfyWorkflowWrapper("workflow_api.json")

    # 用户输入的风格编号
    

    # 根据风格编号设置不同的文本提示
    style_prompts = [
        "Abstract | Futuristic | Experimental | Contemporary art | Jazz album | Pablo Picasso | Mysterious",
        "Abstract | Futuristic | Experimental | Contemporary art | Jazz album | Keith Haring | Mysterious",
        "Abstract | Futuristic | Experimental | Contemporary art | Jazz album | Wassily Kandinsky | Mysterious"
    ]

    ref_image_path = ""

    prompt_text = style_prompts[st.session_state['selected_caption_index']]
    if not prompt_text:
        print("Invalid style input number")
        exit()

    # 修改工作流中的文本提示节点
    wf.set_node_param("Positive", "text", prompt_text)


    image_metadata = api.upload_image(ref_image)  # 传递文件名和文件对象
    print(image_metadata)
    wf.set_node_param("Load Image", "image", f"{image_metadata['subfolder']}/{image_metadata['name']}")



    # 队列工作流以完成
    try:
        results = api.queue_and_wait_images(wf, "Save Image")
        for filename, image_data in results.items():
            #st.image(image_data, caption=caption)
            with open(f"output/{filename}", "wb+") as f:
                f.write(image_data)
                st.session_state.generated_image_path = f"output/{filename}"
            with open(f"output/{filename}.txt", "w") as f:
                f.write(caption)
            
                
    except Exception as e:
        print(f"An error occurred while processing the workflow: {e}")
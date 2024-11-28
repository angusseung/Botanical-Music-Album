from comfy_api_simplified import ComfyApiWrapper, ComfyWorkflowWrapper
import streamlit as st
import random  # For generating random seeds


def generate(ref_image, generate_caption, caption, progress=None):
    # 创建API包装器，使用你的ComfyUI URL（如果需要，添加用户名和密码参数）
    api = ComfyApiWrapper("http://127.0.0.1:8188/")

    # 创建工作流包装器，使用你下载的API格式工作流
    wf = ComfyWorkflowWrapper("workflow_api.json")

    # Generate a random seed
    random_seed = random.randint(1, 2**48 - 1)  # Random seed within a large range
    wf.set_node_param("KSampler", "seed", random_seed)  # Update the seed in the workflow
    print(f"Random seed set: {random_seed}")

    # 根据风格编号设置不同的文本提示
    style_prompts = [
        "Abstract | Futuristic | Experimental | Contemporary art | Jazz album | Pablo Picasso | Mysterious |" + generate_caption,
        "John Singer Sargent style | Impressionist watercolors | loose brushwork | fluid color transitions | natural light and shadow play | portraiture | elegant and realistic" + generate_caption,
        "Abstract | Futuristic | Experimental | Contemporary art | Jazz album | Wassily Kandinsky | Mysterious| " + generate_caption,
        "A minimalist abstract composition in the style of Kazimir Malevich | featuring geometric shapes like squares and circles | Strong contrasts between black and white | with a focus on pure abstraction | No emotional expression | just rational forms | Inspired by the Suprematist movement | with a monochromatic palette and simple | rigid lines." + generate_caption,
        "Abstract | Contemporary | Inspired by Zao Wou-Ki | Fluid brushstrokes | Fusion of Eastern and Western art | Free-flowing brushwork | Colorful and emotional abstraction | Bold strokes and texture | Large-scale compositions | Harmonious balance between light and dark | Expressive and spontaneous" + generate_caption,
        "Hiroshi Yoshida | Japanese woodblock print artist | Landscape and nature scenes | Rich color palette| Detailed yet harmonious composition" + generate_caption
    ]

    ref_image_path = ""

    # Validate the selected_caption_index before using it
    selected_index = st.session_state.get('selected_caption_index', -1)  # Default to -1 if not found
    if selected_index < 0 or selected_index >= len(style_prompts):
        print("Invalid style input number, using default style.")
        selected_index = 0  # Default to the first style prompt

    prompt_text = style_prompts[selected_index]

    # 修改工作流中的文本提示节点
    wf.set_node_param("Positive", "text", prompt_text)

    image_metadata = api.upload_image(ref_image)  # 传递文件名和文件对象
    print(image_metadata)
    wf.set_node_param("Load Image", "image", f"{image_metadata['subfolder']}/{image_metadata['name']}")

    # 队列工作流以完成
    try:
        if progress:
            progress.progress(0)
        results = api.queue_and_wait_images(wf, "Save Image")
        total_steps = len(results)
        for step, (filename, image_data) in enumerate(results.items()):
            if progress:
                progress.progress(int((step + 1) / total_steps * 100))
            with open(f"output/{filename}", "wb+") as f:
                f.write(image_data)
                st.session_state.generated_image_path = f"output/{filename}"
            with open(f"output/{filename}.txt", "w") as f:
                f.write(caption)
            if progress:
                progress.progress(100)

    except Exception as e:
        print(f"An error occurred while processing the workflow: {e}")

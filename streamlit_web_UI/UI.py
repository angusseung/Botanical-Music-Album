import streamlit as st
from streamlit_image_select import image_select
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
import base64
from datetime import datetime
import asyncio

from pathlib import Path
from comfy_api import generate
from music_generator import generate_music
import time

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)



image_path = './img/plant1.jpg'
output_dir = './audio'

# UI configurations
st.set_page_config(page_title="Music Album Generator", page_icon=":minidisc:", layout="wide")




# Function to display the first page
def display_page1():
    cover_content = """
    <div style="width: 100%; ">
    <img src="https://images.unsplash.com/photo-1727905845455-41f099fbeeff?q=80&w=2274&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" alt="Cover Image" style="width: 100%; height: 300px; object-fit: cover;">
    </div>
    """
    # Render the cover page content
    st.markdown(cover_content, unsafe_allow_html=True)
    st.markdown("# Music Album Generator")
    #st.markdown("Let's find out some art things in nature!")

    st.write("\n\n")
    st.subheader("Step 1 - Choose an Art Style")
    image_paths = [
        "pic/Pablo Picasso.jpg",
        "pic/John Singer Sargent.jpg",
        "pic/Wassily Kandinsky.jpg",
        "pic/Kazimir Malevich.png",
        "pic/Zao Wou-Ki.png",
        "pic/Hiroshi Yoshida.png"
    ]
    captions = [
        "Pablo Picasso",
        "John Singer Sargent",
        "Wassily Kandinsky",
        "Kazimir Malevich",
        "Zao Wou-Ki",
        "Hiroshi Yoshida"


    ]
    selected_path = image_select(
        label="Select an art style:",
        images=image_paths,
        captions=captions,
        use_container_width=True
    )

    # Check if an image is selected and update session state
    if selected_path:
        selected_index = image_paths.index(selected_path)
        st.session_state['selected_caption_index'] = selected_index
        st.session_state['selected_caption'] = captions[selected_index]
        image_path = selected_path
    else:
        st.write("No image selected.")

    st.write("\n\n")
    st.subheader("Step 2 - Import a Picture")
    tempfile = "tempimage.jpg"
    if uploaded_file := st.file_uploader("Choose a picture you took in real life...", type=['jpg', 'jpeg', 'png']):
        with open(tempfile, "wb") as temp_file:
            temp_file.write(uploaded_file.getvalue())
    
        st.write("\n\n")
        st.subheader("Step 3 - Leave Your Unique Imprint")
        user_mark_input = st.text_input("Input your participants in the album production...", " ")
        st.session_state.user_mark_input = user_mark_input  # Storing user input in session_state


        st.write("\n\n")
        st.write("\n\n")
        if st.button("Submit", type="primary", key="submit_button_page1"):
            if not user_mark_input.strip():
                st.warning("Please enter your participants in the album production. This field cannot be empty.")
            elif st.session_state.get('selected_caption') and uploaded_file:
                st.success("Submission successful! You selected: " + st.session_state['selected_caption'] + ".")
                st.session_state.user_mark_input = user_mark_input  # Store user input in session_state after validation
                caption = st.session_state.user_mark_input
                generate_caption = generate_music(image_path, output_dir)
                generate(tempfile, generate_caption,caption)

                progress_bar = st.progress(0)
                for i in range(1,101):
                    progress_bar.progress(i)
                    time.sleep(0.05)
                
                st.switch_page(page2)

            else:
                st.warning("Please select an art style and upload an image to proceed.")
    





# Function to display the second page
def display_page2():
    
    # Load the original image using OpenCV
    generated_image_path = st.session_state.get('generated_image_path', '')
    if generated_image_path and Path(generated_image_path).exists():
        original_image = cv2.imread(generated_image_path)

    
        # Apply Gaussian blur to the image
        blurred_image = cv2.GaussianBlur(original_image, (71, 71), 0)
    
        # Adjust the brightness of the blurred image (make it darker)
        darkness_factor = 30  # The higher the value, the darker the image
        adjusted_blurred_image = cv2.addWeighted(blurred_image, 1, np.zeros(blurred_image.shape, blurred_image.dtype), 0, -darkness_factor)
    
        # Convert the blurred image to LAB color space
        lab_image = cv2.cvtColor(adjusted_blurred_image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab_image)
    
        # Adjust the contrast of the L channel (reduce contrast)
        contrast_factor = 0.6  # Reduce contrast by 40%
        l_adjusted = cv2.convertScaleAbs(l, alpha=contrast_factor, beta=0)
    
        # Adjust the saturation of the A and B channels (reduce saturation)
        saturation_factor = 0.8  # Reduce saturation by 20%
        a_adjusted = cv2.convertScaleAbs(a, alpha=saturation_factor, beta=0)
        b_adjusted = cv2.convertScaleAbs(b, alpha=saturation_factor, beta=0)
        
        # Merge the adjusted L, A, and B channels back together
        lab_adjusted = cv2.merge((l_adjusted, a_adjusted, b_adjusted))
        
        # Convert back to BGR color space
        final_image = cv2.cvtColor(lab_adjusted, cv2.COLOR_LAB2BGR)
        
        # Resize the original image to a specific size (e.g., 200x200) with high-quality interpolation
        desired_width = 200
        desired_height = 200
        resized_original_image = cv2.resize(original_image, (desired_width, desired_height), interpolation=cv2.INTER_CUBIC)
        
        # Resize the final image to a specific size (e.g., 650x250)
        resized_final_image = cv2.resize(final_image, (650, 250), interpolation=cv2.INTER_AREA)
        
        # Define the position of the resized original image (e.g., 150, 100)
        x = (650 - desired_width) // 2
        y = (250 - desired_height) // 2
        
        # Ensure the resized original image does not go out of the bounds of the final image
        end_x = min(x + desired_width, 650)
        end_y = min(y + desired_height, 250)
        
        # Overlay the resized original image onto the final image
        resized_final_image[y:end_y, x:end_x] = resized_original_image[0:end_y-y, 0:end_x-x]
        
        # Get the current date
        current_date = datetime.now().strftime("%d.%m          .%Y")
        if "user_mark_input" not in st.session_state:
            st.session_state.user_mark_input = ""

        user_mark_input = st.session_state.user_mark_input #get the user_mark_input info in page1
        
        # Add the date to the album cover
        font = cv2.FONT_HERSHEY_TRIPLEX
        font_scale = 1
        font_color = (255, 255, 255)  # White color
        line_type = 1
        text_position = (150, 143)  # Position where the text will be placed
        cv2.putText(resized_final_image, current_date, text_position, font, font_scale, font_color, line_type)

        #Add the user_mark_input to the album cover
        text_size = cv2.getTextSize(user_mark_input, font, font_scale, line_type)[0]
        text_width = text_size[0]
        text_position_2_x = (resized_final_image.shape[1] - text_width) // 2 + 40
        text_position_2 = (text_position_2_x, 240)
        font_scale_2 = 0.8
        line_type_2 = 1
        font_2 = cv2.FONT_HERSHEY_PLAIN
        cv2.putText(resized_final_image, user_mark_input, text_position_2, font_2, font_scale_2, font_color, line_type_2)
        
        # Convert the final image back to RGB for Streamlit
        final_image_rgb = cv2.cvtColor(resized_final_image, cv2.COLOR_BGR2RGB)
        
        # Convert the final image to a format that can be displayed by Streamlit
        final_image_pil = Image.fromarray(final_image_rgb)
        final_image_bytes = BytesIO()
        final_image_pil.save(final_image_bytes, format='PNG')
        final_image_base64 = base64.b64encode(final_image_bytes.getvalue()).decode()
        
        st.markdown(
        f'<img src="data:image/png;base64,{final_image_base64}" style="display: block; margin-left: auto; margin-right: auto; width: 100%;">',
        unsafe_allow_html=True
        )

    else:
        print()
    

    st.write("\n\n")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("# Music Player")
        st.subheader("Now Playing")

    with col2:
        audio_file = "audio/music.wav"
        st.write("\n\n")
        st.write("\n\n")
        st.write("\n\n")
        st.write("\n\n")
        st.write("\n\n")
        st.write("\n\n")
        st.write("\n\n")
        st.write("\n\n") 
        st.write("\n\n")

        st.audio(audio_file, "Listen to the music")

    st.write("\n\n")
    st.write("\n\n")
    st.write("\n\n")
    st.write("\n\n")
    st.write("\n\n")
    st.write("\n\n")
    st.write("\n\n")

    st.markdown("# Album Gallery")
    st.subheader("See the visual and musical artworks that others have created with different artists.")

    all_files = list(Path('output').iterdir())
    images = [image for image in all_files if not image.name.endswith("txt")]
    captions = [open(f'output/{image.name}.txt').read() for image in images]

    if images:
        history_songs = image_select(
            label=" ",
            images=images,
            captions=captions
        )


    st.write("\n\n")
    if st.button("Play Again!", type="primary", key="play_again_button"):
        st.switch_page(page1)

    


def main():
    # Create a sidebar
    global page1, page2
    page1 = st.Page(display_page1, title="Plant Import")
    page2 = st.Page(display_page2, title="Music Player")
    pg = st.navigation([page1, page2])
    pg.run()

    # with st.sidebar:
    #    st.header("🌲 Navigation")
    #    page = st.radio(" ", ["Plant Importer", "Music Player"])

    # # Display the selected page
    # if page == "Plant Importer":
    #    display_page1()
    # elif page == "Music Player":
    #    display_page2()

if __name__ == "__main__":
    main()
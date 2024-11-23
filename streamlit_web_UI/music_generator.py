import torch
import numpy as np
from diffusers import AudioLDM2Pipeline, DPMSolverMultistepScheduler
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from scipy.io.wavfile import write

def generate_music(image_path, output_dir, num_inference_steps=200, audio_length_in_s=10):
    """
    Generate music based on an image and save it as WAV files.

    Parameters:
        image_path (str): The path to the input image.
        output_dir (str): The directory where the output WAV files will be saved.
        num_inference_steps (int): Number of inference steps for audio generation.
        audio_length_in_s (int): Length of the generated audio in seconds.
    """
    
    # Load the image captioning model
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    # Load and process the image
    image = Image.open(image_path)
    inputs = processor(images=image, return_tensors="pt")
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)

    print("Generated Caption:", caption)

    # Load the audio generation model
    pipeline = AudioLDM2Pipeline.from_pretrained(
        "cvssp/audioldm2-music", torch_dtype=torch.float16
    )
    pipeline.to("cuda")
    pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
        pipeline.scheduler.config
    )
    pipeline.enable_model_cpu_offload()

    # Generate audio based on the caption
    audios = pipeline(caption, 
                      num_inference_steps=num_inference_steps,
                      audio_length_in_s=audio_length_in_s).audios

    # Save the generated audio to WAV files
    for i, audio in enumerate(audios):
        wav_file_path = f"{output_dir}/music.wav"
        write(wav_file_path, 16000, audio.astype(np.float32))  # Assuming a sample rate of 16000 Hz

    print(f"Audio files saved successfully in {output_dir}.")

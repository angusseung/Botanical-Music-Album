import torch
import numpy as np
from diffusers import AudioLDM2Pipeline, DPMSolverMultistepScheduler
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from scipy.io.wavfile import write  # Importing the write function

# Load the image captioning model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Load and process the image
image = Image.open('./img/plant4.jpg')
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
                  num_inference_steps=200,
                  audio_length_in_s=15).audios

# Save the generated audio to a WAV file
for i, audio in enumerate(audios):
    # Convert audio to float32 and save as WAV file
    write(f'./music/output_audio_{i}.wav', 16000, audio.astype(np.float32))  # Assuming a sample rate of 16000 Hz

print("Audio files saved successfully.")
from diffusers import StableDiffusionPipeline
import torch
import os

# ✅ Load model using CPU and float32 (no safetensors)
pipe = StableDiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",
    use_safetensors=False,
    torch_dtype=torch.float32
).to("cpu")

# ✅ Disable safety checker to avoid censorship errors
class DummySafetyChecker:
    def __call__(self, images, **kwargs):
        return images, [False] * len(images)

pipe.safety_checker = DummySafetyChecker()

def generate_emoji(prompt: str, output_path: str):
    try:
        # ✅ Build rich emoji prompt
        optimized_prompt = (
            f"cute {prompt} emoji, anime style, 3D look, clean lines, vibrant colors, soft lighting"
        )

        # ✅ Generate image
        image = pipe(
            prompt=optimized_prompt,
            width=512,
            height=512,
            num_inference_steps=40,
            guidance_scale=7.5
        ).images[0]

        # ✅ Save the result
        image.save(output_path)
        return output_path

    except Exception as e:
        print(f"❌ Error generating emoji: {str(e)}")
        raise

# ✅ Test the module directly
if __name__ == "__main__":
    output_file = "cat_boy_emoji.png"
    generate_emoji("cat boy", output_file)
    print(f"✅ Emoji saved to: {output_file}")

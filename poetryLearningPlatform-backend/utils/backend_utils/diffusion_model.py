from diffusers import DiffusionPipeline
import torch


# 文生图模型
class Diffusion_model:
    def __init__(self) -> None:
        self.model = DiffusionPipeline.from_pretrained(
            # "/home/sjc/Program/playground-v2-512px-base",
            "/work/gaohan/pythonProjects/PoetryLearningPlatform/poetryLearningPlatform-backend/models/playground-v2-512px-base",
            torch_dtype=torch.float16,
            use_safetensors=True,
            add_watermarker=False,
            variant="fp16",
        ).to("cuda")


pipe = Diffusion_model()

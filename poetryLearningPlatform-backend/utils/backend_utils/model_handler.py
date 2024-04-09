import torch
from diffusers import DiffusionPipeline
from models.moellava.mm_utils import get_model_name_from_path
from models.moellava.model.builder import load_pretrained_model


def initialize_models():
    # 初始化文生图模型
    diffusion_model = DiffusionPipeline.from_pretrained(
        # "/home/sjc/Program/playground-v2-512px-base",
        "/work/gaohan/pythonProjects/PoetryLearningPlatform/poetryLearningPlatform-backend/models/playground-v2-512px-base",
        torch_dtype=torch.float16,
        use_safetensors=True,
        add_watermarker=False,
        variant="fp16",
    ).to("cuda")

    # 初始化图文回答模型
    moellava_model_path = '/work/gaohan/pythonProjects/PoetryLearningPlatform/poetryLearningPlatform-backend/models/moellava/MoE-LLaVA-StableLM-1.6B-4e'
    moellava_device = 'cuda'
    moellava_load_4bit, moellava_load_8bit = False, False  # FIXME: Deepspeed support 4bit or 8bit?
    moellava_model_name = get_model_name_from_path(moellava_model_path)
    moellava_tokenizer, moellava_model, moellava_processor, moellava_context_len = load_pretrained_model(
        moellava_model_path, None, moellava_model_name, moellava_load_8bit, moellava_load_4bit,
        device=moellava_device)

    return diffusion_model, (moellava_tokenizer, moellava_model, moellava_processor, moellava_context_len)


# diffusion_model, moellava_model = initialize_models()

from diffusers import DiffusionPipeline
import torch
import requests
import json
from utils.youdao_api.AuthV3Util import addAuthParams
from utils.gpt.prompt_utils import *
from models.moellava.mm_utils import get_model_name_from_path
from models.moellava.model.builder import load_pretrained_model
#文生图模型
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
#图文回答模型
class MOELLAVA_LOAD:
    def __init__(self) -> None:
        self.model_path = '/work/gaohan/pythonProjects/PoetryLearningPlatform/poetryLearningPlatform-backend/models/moellava/MoE-LLaVA-StableLM-1.6B-4e'  # LanguageBind/MoE-LLaVA-Qwen-1.8B-4e or LanguageBind/MoE-LLaVA-StableLM-1.6B-4e
        self.device = 'cuda'
        self.load_4bit, self.load_8bit = False, False  # FIXME: Deepspeed support 4bit or 8bit?
        self.model_name = get_model_name_from_path(self.model_path)
        self.tokenizer, self.model, self.processor, self.context_len = load_pretrained_model(self.model_path, None, self.model_name, self.load_8bit, self.load_4bit,
                                                                     device=self.device)

pipe = Diffusion_model()
MOELLAVA_MODEL = MOELLAVA_LOAD()
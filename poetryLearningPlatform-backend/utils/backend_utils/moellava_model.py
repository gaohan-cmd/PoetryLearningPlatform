from models.moellava.mm_utils import get_model_name_from_path
from models.moellava.model.builder import load_pretrained_model


# 图文回答模型
class moellava_model:
    def __init__(self) -> None:
        self.model_path = '/work/gaohan/pythonProjects/PoetryLearningPlatform/poetryLearningPlatform-backend/models/moellava/MoE-LLaVA-StableLM-1.6B-4e'  # LanguageBind/MoE-LLaVA-Qwen-1.8B-4e or LanguageBind/MoE-LLaVA-StableLM-1.6B-4e
        self.device = 'cuda'
        self.load_4bit, self.load_8bit = False, False  # FIXME: Deepspeed support 4bit or 8bit?
        self.model_name = get_model_name_from_path(self.model_path)
        self.tokenizer, self.model, self.processor, self.context_len = load_pretrained_model(self.model_path, None,
                                                                                             self.model_name,
                                                                                             self.load_8bit,
                                                                                             self.load_4bit,
                                                                                             device=self.device)


MOELLAVA_MODEL = moellava_model()

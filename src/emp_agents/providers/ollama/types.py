from enum import StrEnum


class OllamaModelType(StrEnum):
    gemma3_27b = "gemma3:27b-it-q4_K_M"
    gemma3_27b_qat = "gemma3:27b-it-qat"
    openthinker_32b = "openthinker:32b"
    deepseek_r1_32b = "deepseek-r1:32b"
    mistral_latest = "mistral:latest"
    qwen2_5_coder_14b = "qwen2.5-coder:14b"
    llama3_2 = "llama3.2"
    mistral_small_3_1 = "mistral-small3.1:latest"
    qwq_32b = "qwq:latest"
    granite_3 = "granite3.3:latest"
 
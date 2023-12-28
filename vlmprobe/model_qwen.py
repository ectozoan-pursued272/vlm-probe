"""Qwen-VL-Chat loader. Trust-remote-code is required."""
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def load(name="Qwen/Qwen-VL-Chat", device="cuda"):
    tok = AutoTokenizer.from_pretrained(name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        name, trust_remote_code=True, torch_dtype=torch.float16,
    ).to(device).eval()
    return tok, model

"""Model loaders. Right now just LLaVA, more coming."""
import torch
from transformers import AutoProcessor, LlavaForConditionalGeneration


def load_llava(name="llava-hf/llava-1.5-7b-hf", device="cuda", dtype="float16"):
    proc  = AutoProcessor.from_pretrained(name)
    model = LlavaForConditionalGeneration.from_pretrained(
        name, torch_dtype=getattr(torch, dtype)
    ).to(device).eval()
    return proc, model


def generate(proc, model, image, prompt, max_new_tokens=16):
    inputs = proc(images=image, text=prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        out = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
    return proc.batch_decode(out, skip_special_tokens=True)[0]

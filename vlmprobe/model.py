"""Model loaders for the VLMs in the writeup."""
import torch
from PIL import Image

# import lazily so we don't drag transformers in for every CLI call
def _hf():
    import transformers
    return transformers


def load(name, device="cuda", dtype="float16"):
    """Return (processor, model). Dispatches by name prefix."""
    hf = _hf()
    torch_dtype = getattr(torch, dtype)
    if "llava-" in name.lower() or "llava_" in name.lower():
        proc  = hf.AutoProcessor.from_pretrained(name)
        model = hf.LlavaForConditionalGeneration.from_pretrained(name, torch_dtype=torch_dtype)
    elif "Qwen-VL" in name or "qwen-vl" in name.lower():
        proc  = hf.AutoProcessor.from_pretrained(name, trust_remote_code=True)
        model = hf.AutoModelForCausalLM.from_pretrained(name, torch_dtype=torch_dtype,
                                                        trust_remote_code=True)
    elif "InternVL" in name or "internvl" in name.lower():
        proc  = hf.AutoTokenizer.from_pretrained(name, trust_remote_code=True)
        model = hf.AutoModel.from_pretrained(name, torch_dtype=torch_dtype,
                                             trust_remote_code=True)
    else:
        # generic fallback — works for blip2 / instructblip family
        proc  = hf.AutoProcessor.from_pretrained(name)
        model = hf.AutoModelForVision2Seq.from_pretrained(name, torch_dtype=torch_dtype)
    return proc, model.to(device).eval()


def generate(proc, model, image, prompt, max_new_tokens=16):
    """Vanilla deterministic decoding. We override per-model if needed."""
    if isinstance(image, str):
        image = Image.open(image).convert("RGB")
    # Most processors accept (image, text); a few use chat templates.
    try:
        inputs = proc(images=image, text=prompt, return_tensors="pt")
    except TypeError:
        # InternVL-style tokenizer-only path; the model handles the image internally
        inputs = proc(prompt, return_tensors="pt")
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    with torch.no_grad():
        out = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
    text = proc.batch_decode(out, skip_special_tokens=True)[0]
    # strip the echoed prompt if present
    if text.startswith(prompt):
        text = text[len(prompt):]
    return text.strip()

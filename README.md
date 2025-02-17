# VLM-Probe: When Do VLMs Actually Look?

> Companion code for our (in-progress) report on what fine-grained perceptual tasks
> open-source vision-language models fail on, and whether the failure is in the
> visual encoder or the language head.

This repo contains the evaluation harness, probe templates, and per-task scoring
scripts used in the writeup. Models are loaded through `transformers`; tasks are
specified as YAML.

## Citation

If you find any of the scripts here useful, please cite the report (preprint pending):

```bibtex
@misc{xu2026vlmprobe,
  title  = {When Do VLMs Actually Look? Probing fine-grained perception in
            open-source vision-language models},
  author = {Xu, Mingrui},
  year   = {2026},
  note   = {Technical report, Beihang University},
}
```

## Reproducing the numbers

```bash
git clone https://github.com/marived/vlm-probe.git
cd vlm-probe
pip install -e .

# Download the small image set (~500 MB)
python -m vlmprobe.data.fetch --out data/images/

# Evaluate a model on all tasks
python -m vlmprobe.run \
    --model llava-hf/llava-1.5-7b-hf \
    --tasks tasks/*.yaml \
    --out   results/llava15.json
```

Reported numbers in the writeup were produced on 2 x A100 40 GB and pinned versions in
`requirements.lock`. Stochastic decoding is off by default (`temperature=0`); per-task
seeds live in the task YAMLs.

## Tasks

| Task             | Items | What it asks                                    |
| ---------------- | ----- | ----------------------------------------------- |
| `count_objects`  |   ~50 | how many X are there? (1..8)                    |
| `spatial_rel`    |   ~30 | is X to the left of Y? above? in front of?      |
| `colour_attr`    |   ~30 | what colour is the X?                           |
| `text_in_image`  |   ~20 | what does the sign say? (small text, OCR-ish)   |
| `partial_occl`   |   ~25 | is X fully visible? partially occluded? hidden? |

All five are multiple-choice. Scoring is exact-match on the parsed answer.

## Layout

```
vlm-probe/
├── vlmprobe/
│   ├── run.py            # main eval driver
│   ├── model.py          # model loaders (LLaVA, Qwen-VL, InternVL, ...)
│   ├── tasks.py          # task loader / scorer
│   └── data/
├── tasks/                # one YAML per task
├── results/              # JSON outputs go here
└── scripts/              # ad-hoc post-processing
```

## License

MIT, see [LICENSE](LICENSE).

<!-- writeup draft (internal): https://drive.example/d/draft -->

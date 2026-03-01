# notes

things that surprised me while building this:

- counting is genuinely hard for all the open VLMs I tried. >5 objects basically falls
  apart. LLaVA-1.5 was at 0.31 on `count_objects`, Qwen-VL-Chat at 0.40, InternVL-1.5 at
  0.49. The pattern is the same: 1-3 mostly right, 4+ random.
- partial occlusion is the easiest task, weirdly. I'd expected the opposite.
- prompt phrasing matters by ~3 points absolute. "Answer with a single number" beats
  "How many?" alone by a lot.
- one of the LLaVA evals was wrong for two months because the answer-parser stripped a
  leading "the" so "the cat" matched both "cat" and "the dog". Lesson: write the scorer
  tests first.

todo:
- bigger occlusion set
- add a "no, it's not there" distractor for the spatial task
- maybe a referring-expression set

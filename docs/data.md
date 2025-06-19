# data

Images come from three sources:

1. Photos I took on campus (counting, occlusion sets, signage).
2. A subset of COCO 2017 val, hand-picked for unambiguous answers.
3. A small batch of synthetic compositions made in Blender (mostly the spatial set,
   where you need ground-truth 3D positions).

Annotations are mine. The synthetic compositions are released under CC0; everything
else has source attribution in `data/sources.tsv`.

## sizes (as of v0.4)

| task            |  items |
| --------------- | ------ |
| count_objects   |   400  |
| spatial_rel     |   300  |
| colour_attr     |   300  |
| text_in_image   |   200  |
| partial_occl    |   250  |

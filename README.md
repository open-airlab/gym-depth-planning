# gym-depth-planning

Paper: [link](https://www.mdpi.com/2218-6581/11/5/109)

[![Watch the video](https://img.youtube.com/vi/HPXXc_R3re8/default.jpg)](https://youtu.be/HPXXc_R3re8)

To cite this paper:

```
  @Article{robotics11050109,
  AUTHOR = {Ugurlu, Halil Ibrahim and Pham, Xuan Huy and Kayacan, Erdal},
  TITLE = {Sim-to-Real Deep Reinforcement Learning for Safe End-to-End Planning of Aerial Robots},
  JOURNAL = {Robotics},
  VOLUME = {11},
  YEAR = {2022},
  NUMBER = {5},
  ARTICLE-NUMBER = {109},
  URL = {https://www.mdpi.com/2218-6581/11/5/109},
  ISSN = {2218-6581},
  DOI = {10.3390/robotics11050109}
  }
```

### Prerequisites 
- Create conda environment using `conda_env.yml`
- `pip install -e .`

### Examples
- Run roscore
- Open `webots/worlds/train-no-dynamic-random-obstacles.wbt` with Webots 2021a
- Training: run train/train.py
- Evaluation examples of pretrained models under eval folder

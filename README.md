App that posts television series rewatch threads in online message boards on a recurring interval.

# getting-started

1) Create a virtual environment and install dependencies:
```bash
python -m venv avenv
source avenv/bin/activate
pip install -r requirements/requirements-dev.txt
```

[Refer to cloudformation template](templates/rewatch_aws.yml#32) for safe source of python runtime

2) run unittests and make sure they pass

```bash
python -m unittest
```

# application-link
[Example message board post](https://www.reddit.com/r/Toonami/comments/1ao9p0t/cyborg_009_episode_1_and_episode_2_rewatch/) created by the application

Since the human condition is such that we always prefer to watch the same tv series over again since it is good and familiar as opposed to trying something new we might not like, this application is desperately needed.

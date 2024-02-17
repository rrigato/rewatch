App that posts television series rewatch threads in online message boards on a recurring interval.

# getting-started

1) Create a virtual environment and install dependencies:
```bash
python -m venv avenv
source avenv/bin/activate
pip install -r requirements/requirements-dev.txt
```

[Refer to cloudformation template](templates/rewatch_aws.yml#32) for safe source of python runtime

1) run unittests and make sure they pass

```bash
python -m unittest
```

3) install [aws cli v2](https://aws.amazon.com/cli/) for working with aws resources locally 


Since the human condition is such that we always prefer to watch the same tv series over again since it is good and familiar as opposed to trying something new we might not like, this application is desperately needed.
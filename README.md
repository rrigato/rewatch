App that posts television series rewatch threads in online message boards on a recurring interval.

# getting-started

1) Create a virtual environment and install dependencies:
```bash
python3.11 -m venv avenv
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


# Deployment

Pushes to `master` deploy the application using Python 3.11. Pull requests run
unit tests, dependency validation, CloudFormation linting, and ZIP packaging
without AWS credentials or invoking the function.

The deployment ZIP includes the pinned production dependencies. Deployment waits
for the code update to finish before invoking the handler. The GitHub Actions
role needs `lambda:GetFunctionConfiguration` for this wait in addition to its
existing deployment permissions. The final invocation can publish a Reddit post
scheduled for the current date. The Lambda runtime remains Python 3.11.

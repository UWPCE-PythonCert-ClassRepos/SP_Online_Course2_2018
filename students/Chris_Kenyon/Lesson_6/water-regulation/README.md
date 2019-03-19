# Water Regulation

## Instructions

Your assignment is to complete, test, and lint this project. Begin by forking a copy of this project to yourself, and then cloning down to your computer.

## Your Goals

Note that all of the command examples below should be run from the project root which contains the directories waterregulation, sensor, and pump.

1. Complete the TODOs in *waterregulation/controller.py* and *waterregulation/decider.py*.
2. Complete the TODOs in *waterregulation/test.py* and *waterregulation/integrationtest.py*. A single integration test may be sufficient. However, your unit tests in *test.py* should include at least one test for each specified behavior.
3. `python -m unittest waterregulation/test.py` and `python -m unittest waterregulation/integrationtest.py` should have no failures.
4. Running `coverage run --source=waterregulation/controller.py,waterregulation/decider.py -m unittest waterregulation/test.py; coverage report` shows 90%+ coverage..
5. Satisfy the linter such that `pylint waterregulation` gives no errors and and `flake8 waterregulation` gives no errors. You may have to add docstrings to your test files.


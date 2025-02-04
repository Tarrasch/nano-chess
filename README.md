# Mini chess engine

Good commands to know:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt

pytest
pytest tests/test_checkmates.py

optional:
echo 'echo ENTERED; source .venv/bin/activate' > .autoenv.zsh

submissions:

mkdir -p out/models/
pyminify src/main.py --output out/main.py
pyminify src/neural_network_eval.py --output out/neural_network_eval.py
pyminify src/position.py --output out/position.py
pyminify src/search.py --output out/search.py
cp models/first_attempt.pickle out/models/first_attempt.pickle

tar -czf submission.tar.gz -C out .
```

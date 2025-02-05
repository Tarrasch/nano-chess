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

mkdir -p kaggle_submissions/
pyminify src/main.py --output kaggle_submissions/main.py
pyminify src/neural_network_eval.py --output kaggle_submissions/neural_network_eval.py
pyminify src/position.py --output kaggle_submissions/position.py
pyminify src/search.py --output kaggle_submissions/search.py

cp models/first_attempt.pickle kaggle_submissions/model.pickle
sed --in-place 's%models/first_attempt.pickle%/kaggle_simulations/agent/model.pickle%'  kaggle_submissions/neural_network_eval.py

tar -czf submission.tar.gz -C kaggle_submissions .
```

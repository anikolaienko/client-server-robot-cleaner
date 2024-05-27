export PYTHONPATH=$PYTHONPATH:$(pwd)/src

./.venv/bin/python src/server/main.py -p 8081

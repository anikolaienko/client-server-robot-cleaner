export PYTHONPATH=$PYTHONPATH:$(pwd)/src

./.venv/bin/python src/robot/main.py -n Rusty $@

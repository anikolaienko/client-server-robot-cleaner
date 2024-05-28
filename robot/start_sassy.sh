export PYTHONPATH=$PYTHONPATH:$(pwd)/src

./.venv/bin/python src/robot/main.py -n Sassy -p 8080

export PYTHONPATH=$PYTHONPATH:$(pwd)/src

./.venv/bin/python src/robot/main.py -n Gizmo -p 8081

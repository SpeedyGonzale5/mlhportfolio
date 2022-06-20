#!/bin/bash

tmux kill-server && cd mlhportfolio && git fetch && git reset origin/main –hard 01~ && source python3-virtualenv/bin/activate && pip3 install -r requirements.txt && tmux && flask run –host=0.0.0.0
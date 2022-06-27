#!/bin/bash

cd mlhportfolio && git fetch && git reset origin/main -hard  && source python3-virtualenv/bin/activate && pip3 install -r && requirements.txt && systemctl restart mlhportfolio && flask run --host=0.0.0.0
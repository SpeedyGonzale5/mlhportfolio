#!/bin/bash

curl -request POST http://104.248.14.212:5000/api/timeline_post -d 'name=Weib&email=wei.he@mlh.io&content=Just Added Database to my portfolio site!' && curl --request GET http://104.248.14.212:5000/api/timeline_post | jq '.'
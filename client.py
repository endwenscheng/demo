# -*- coding=utf-8 -*-

import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")
socket.setsockopt_string(zmq.SUBSCRIBE, '')  # 消息过滤
while True:
    response = socket.recv_string()
    response = json.loads(response)
    if isinstance(response, list):
        for r in response:
            print(r)
    else:
        print(response)

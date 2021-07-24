import asyncio
import json
import datetime
from pybit import WebSocket
import zmq

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")


def get_timestamp():
    now = datetime.datetime.now()
    t = now.isoformat("T", "milliseconds")
    return t + "Z"


async def get_ws(url, channels):
    return WebSocket(url, subscriptions=channels)


async def fetch(ws, channel):
    return ws.fetch(channel)


async def ping(ws):
    return ws.ping()


async def subscribe_without_login(url: str, channels):
    while True:
        try:
            ws = await asyncio.wait_for(get_ws(url, channels), timeout=25)
            print('Start')

            while True:
                try:
                    for channel in channels:
                        res = await fetch(ws, channel)
                        socket.send_string(json.dumps(res))
                        print('{} Send {} to mq'.format(get_timestamp(), channel))
                        # print(res)
                except (asyncio.TimeoutError,) as e:
                    try:
                        res = await ping(ws)
                        print(res)
                        continue
                    except Exception as e:
                        print("连接关闭，正在重连……")
                        break
                await asyncio.sleep(3)

        except Exception as e:
            print("{}.连接断开，正在重连……".format(e.__str__()))
            continue


if __name__ == '__main__':
    channels = [
        'orderBookL2_25.BTCUSD',
        'trade.BTCUSD'
    ]
    # endpoint_public = 'wss://stream-testnet.bybit.com/realtime'
    endpoint_public = 'wss://stream.bytick.com/realtime'
    # endpoint_public = 'wss://stream.bybit.com/realtime_public'
    loop = asyncio.get_event_loop()

    loop.run_until_complete(
        subscribe_without_login(endpoint_public, channels),
    )
    loop.close()

import websockets
import asyncio
from threading import Thread, Lock
import logging
from raspberry_pi_controller.constants import NUM_PIXELS

uri = "ws://10.41.222.122/strip_data"

class WebsocketTransmitter:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.message = None
        thread = Thread(target=self.websocket_thread)
        self.message_lock = Lock()
        thread.start()
    
    def send(self, message):
        with self.message_lock:
            self.message = message

    def websocket_thread(self):
        asyncio.run(self._websocket_thread())
        self.logger.debug(f"End of websocket thread")

    async def _websocket_thread(self):
        async with websockets.connect(uri=uri) as websocket:
            logging.getLogger(self.__class__.__name__).info(f"Started new websocket")
            while True:
                try:
                    if self.message:
                        # logging.getLogger(self.__class__.__name__).info(f"sending a message")
                        # with self.message_lock:
                        await websocket.send(self.message)
                        self.message = None
                    else:
                        # self.logger.info("no message to send")
                        pass
                    await asyncio.sleep(1/40)
                except Exception as e:
                    logging.getLogger(self.__class__.__name__).error(e)
                    await asyncio.sleep(2)
                    break

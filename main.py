import asyncio
from frameutils import Bluetooth

import io

#bluetooth is so sick wow


async def main():
    b = Bluetooth()
    await b.connect()

    print(await b.send_lua("print('hello world')", await_print=True))
    print(await b.send_lua("print(1 + 2)", await_print=True))
    # print(f"Frame battery: {await b.get_battery_level()}")
    #await b.send_lua("bmp_data = frame.file.open('EXOTYPE FINAL Richa.bmp', 'read')")
    #await b.send_lua("frame.display.bitmap(100, 50, 32, 2, 3, bmp_data)")
    
    ### CLEAR POINT
    # await b.send_lua("frame.display.text('HI RICHAS', 1, 1)")
    # await b.send_lua("frame.display.text('AIRPODS CONNECTED', 530, 1)")
    # await b.send_lua("frame.display.text('TEST', 1, 320)")
    # await b.send_lua('''frame.display.bitmap(100, 50, 32, 2, 3, string.rep("\xFF", 32 / 8 * 16))''')
    # await b.send_lua("frame.display.show()")

    # await b.send_lua("frame.display.text('TEST', 1, 1)")
    # await asyncio.sleep(5.00)
    await b.disconnect()

asyncio.run(main())

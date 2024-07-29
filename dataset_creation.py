import asyncio

from datetime import datetime

from viam.robot.client import RobotClient
from viam.components.camera import Camera 

async def connect():
    opts = RobotClient.Options.with_api_key( 
        api_key='ig8r23hpv7527lsyxn28u51be0fvfjzb',
        api_key_id='23b76826-ba96-4a3d-aaeb-b59ddaa1f3ac'
    )
    return await RobotClient.at_address('rover-0-main.b2fkxt2kv3.viam.cloud', opts)


async def main():
    robot = await connect()

    # Get webcam (camera component)
    webcam = Camera.from_robot(robot, "webcam")

    # throw out a few initial images
    for _ in range(0,3):
        await webcam.get_image()

    while True:
        cmd = input("Press Enter to take a picture, Q to quit: ")
        if cmd == "Q" or cmd == "q":
            break
        try:
            image = await webcam.get_image()
            time = datetime.now()
            timestamp = time.isoformat('T')
            timestamp_filename = timestamp.replace(":","_") + ".png"

            # Save image with timestamp
            image.save("/root/.viam/capture/cd/webcam/" + timestamp_filename)
                
        except:
            continue

    # Don't forget to close the machine when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
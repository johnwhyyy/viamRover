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


    
    # Don't forget to close the machine when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
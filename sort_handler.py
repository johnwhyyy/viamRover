import asyncio
import time

from viam.robot.client import RobotClient
from viam.components.camera import Camera
from viam.components.servo import Servo
from viam.services.vision import VisionClient

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

    # Get clssifier (vision service)
    recycle_classifier = VisionClient.from_robot(robot, "mi_recycle_classifier_vision")

    # Get sort servo (servocomponent)
    sorter = Servo.from_robot(robot, "sorter")

    # Get dump servo (servo component)
    left_dump = Servo.from_robot(robot, "left_dump")
    right_dump = Servo.from_robot(robot, "right_dump")

    # Start loop
    while True:
        cmd = input("Press <Enter> to start, L to dump left, R to dump right, Q to quit: ")
        # Exit loop
        if cmd == "Q" or cmd == "q":
            break
        # Dump left
        elif cmd == "L" or cmd == "l":
            await left_dump.move(45)
            time.sleep(1)
            await left_dump.move(0)
        # Dump right
        elif cmd == "R" or cmd == "r":
            await right_dump.move(45)
            time.sleep(1)
            await right_dump.move(0)
        
        # Start sorting
        try:
            for _ in range(0,3):
                await webcam.get_image()

            image = await webcam.get_image()
            recycle_labels = await recycle_classifier.get_detections(image)
        
            # Iterate through detections to determine to tilt right or left
            dominant_label = ""
            dominant_label_confidence = 0.0
            for detection in recycle_labels:
                if detection.confidence > dominant_label_confidence:
                    dominant_label = detection.class_name
                    dominant_label_confidence = detection.confidence
            
            print("Label: ")
            print("- {}".format(dominant_label.class_name))

            # Handle detections of 'Recyclable'
            if dominant_label.class_name == "Recyclable":
                await sorter.move(45)

            # Handle detections of 'Not-Recyclable'
            elif dominant_label.class_name == "Not_Recyclable":
                await sorter.move(-45)
            
            time.sleep(1)
            
            # Reset sorter
            sorter.move(0)
        except:
            continue

    # Don't forget to close the machine when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
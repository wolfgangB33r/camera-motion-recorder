# Camera motion recorder

A Docker container that records motion still images of configured images sources (cameras)

## Environment variables and defaults

Use the parameters below as Docker environment variables in order to control the motion detection behaviour.

Configure a threshold that defines how much change a single pixel must show to count as changed. \
PIXEL_CHANGE_THRESHOLD = 30

Configures the delay between the images are fetched.\
FREQUENCY = 5

Configures the size of individual objects that need to be detected to count as motion.\
MOTION_PIXEL_THRESHOLD = 5000

Configures the mapped folder where we store the motion recordings.\
FOLDER = "./motion/"

Configures the URL where the container fetches the images.\
URL = ""

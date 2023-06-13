import common
import math #note, for this lab only, your are allowed to import math

def detect_slope_intercept(image):
    line = common.Line()
    line.m = 0
    line.b = 0

    space = common.init_space(2000, 2000)

    for y in range(common.constants.HEIGHT):
        for x in range(common.constants.WIDTH):
            if image[y][x] == 0:  # black lines (0) on a white background (255)
                for theta in range(181):  # theta from 0 to 180 degrees
                    w = x * math.cos(math.radians(theta)) + y * math.sin(math.radians(theta))
                    space[int(w)][theta] += 1

    max_votes = 0
    max_w = 0
    max_theta = 0

    for w in range(2000):
        for theta in range(181):
            if space[w][theta] > max_votes:
                max_votes = space[w][theta]
                max_w = w
                max_theta = theta

    max_theta_radians = math.radians(max_theta)
    line.m = -round(math.cos(max_theta_radians) / math.sin(max_theta_radians), 1)
    line.b = round(max_w / math.sin(max_theta_radians))

    return line


def detect_circles(image):
    # Initialize the voting space
    space = common.init_space(common.constants.HEIGHT, common.constants.WIDTH)

    # Edge Image
    edge_image = common.init_space(common.constants.HEIGHT, common.constants.WIDTH)

    for y in range(common.constants.HEIGHT):
        for x in range(common.constants.WIDTH):
            # black circles (0) on a white background (255)
            if image[y][x] == 0:
                edge_image[y][x] = 255

    # Define the radius of circle
    radius = 30

    # Iterate over the edge pixels and accumulate votes in the voting space
    for y in range(common.constants.HEIGHT):
        for x in range(common.constants.WIDTH):
            if edge_image[y][x] == 255:
                for theta in range(360):
                    a = x - int(radius * math.cos(math.radians(theta)))
                    b = y - int(radius * math.sin(math.radians(theta)))
                    if 0 <= a < common.constants.WIDTH and 0 <= b < common.constants.HEIGHT:
                        space[a][b] += 1

    # Count the number of circles by finding the centers with votes above a threshold
    threshold = 150  # threshold

    num_circles = 0
    for y in range(common.constants.HEIGHT):
        for x in range(common.constants.WIDTH):
            if space[x][y] > threshold:
                num_circles += 1

    return num_circles

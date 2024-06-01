<!-- omit in toc -->
# client-server-robot-cleaner
Exercise: Build client/server app using Socket.IO and Kafka. Solve Robot Cleaner algo.

<!-- omit in toc -->
# Table of Contents:
- [Screenshots](#screenshots)
  - [Run 1](#run-1)
  - [Run 2](#run-2)
- [Robot Cleaner algorithm](#robot-cleaner-algorithm)
- [System design](#system-design)
- [Architecture diagram](#architecture-diagram)
- [Requirements](#requirements)
- [Setup](#setup)
- [Play time](#play-time)

# Screenshots
Should be the last section but everyone likes visuals 😏
## Run 1
Server: 1. Robots: Rusty floor 1
![failed to load screenshot](/docs/screenshot_rusty_level_1.png)

## Run 2
Servers: 1 and 2. Robots: Rusty level 0, Sassy level 1, Gizmo level 2
![failed to load screenshot](/docs/screenshot_all_robots.png)


# Robot Cleaner algorithm
Imagine you have a building with multiple floors (levels).
|         |
| ------- |
\| [level 3](/server/src/data/levels/3.txt) \|
\| [level 2](/server/src/data/levels/2.txt) \|
\| [level 1](/server/src/data/levels/1.txt) \|
\| [level 0](/server/src/data/levels/0.txt) \|

Each level has a different floor layout (click on the level links above). Layout symbols meaning:
* "-" empty space where Robot can move.
* "x" obstacle, Robot need to go around it.
* "R" initial Robot position.

So the algorithmic task is to move Robot around the level and visit every empty space avoiding obstacles. Here is a link to [Robot Cleaner task on leetcode.ca](https://leetcode.ca/all/489.html).

# System design
We have 3 robots available:
* [Rusty](/robot/start_rusty.sh)
* [Sassy](/robot/start_sassy.sh)
* [Gizmo](/robot/start_gizmo.sh)

There are couple of differences between the robots:
* **Rusty** and **Sassy** prefer to connect to [server_1](/server/start_server_1.sh) on post 8080 when **Gizmo** prefers [server_2](/server/start_server_2.sh) on port 8081.
* Each robot has a preference when doing a cleaning. E.g. **Rusty** likes going NORTH first, when **Sassy** choses to go WEST. Configs are described in [robot_configs/data](/robot/src/robot/robot_configs/data/) files.

Two servers **server_1** and **server_2** are connected to Docker hosted Kafka service. This is where **server_1** and **server_2** get commands to send to robots.

To post commands to Kafka topic you need to have a client. For this exercise we just use `kafka-console-producer.sh` available in Kafka Docker image.

# Architecture diagram
![failed to load diagram](/docs/server-client-robot-cleaner.drawio.png)

# Requirements
* Python 3.11 (at least this one was used)
* Docker

# Setup
* Robot
  * In terminal, navigate to [robot](/robot/) folder.
  * Create virtualenv: `virtualenv -p python3.11 .venv`
  * Install dependencies: `.venv/bin/pip install -r requirements.txt`
* Server
  * In terminal, navigate to [server](/server/) folder.
  * Create virtualenv: `virtualenv -p python3.11 .venv`
  * Install dependencies: `.venv/bin/pip install -r requirements.txt`

# Play time
To launch the whole system we need several terminal windows, at least 3: robot, server, kafka client.

Launch system:
* Launch kafka broker:
  * In terminal, navigate to [kafka_queue](/kafka_queue/) folder.
  * Run: `docker compose up -d`
* Launch kafka client:
  * In same terminal, you can run client:
    ```bash 
    docker run -it --rm \
      --network kafka_queue_app-tier \
      bitnami/kafka:3.7.0 /bin/bash
    ```
* Launch server:
  * In new terminal window, navigate to [server](/server/) folder.
  * Run: `. start_server_1.sh`
* Run robot:
  * In new terminal window, navigate to [robot](/robot/) folder.
  * Run: `. start_rusty.sh`

Now in kafka client we need to create topics:
```bash
kafka-topics.sh --create --topic commands --bootstrap-server kafka-server:9092
```

Finally, we can publish commands. In kafka client launch producer:
```bash
kafka-console-producer.sh --topic commands --bootstrap-server kafka-server:9092
```

After you launched Kafka producer you can type messages and send them pressing Enter. If you with to finish session, press Cmd+C.

Valid producer commands:
```bash
# get and display robot firmware version in server 
version

# run cleaning for robot ? on level ?
clean robot Rusty level 0

# pause robot
pause robot Rusty

# resume robot
resume robot Rusty

# reset robot, stop cleaning task completely
reset robot Rusty

# speed, int values 1 to 5, 5 is the fastest
speed value 3 robot Rusty

# speed also can be specified in clean command
clean robot Rusty level 1 speed 5
```

In commands, character case (lower/upper) matters. Command format is required but key value pairs order doesn't matter:
```bash
[command] [key] [value] ...
# e.g.
clean robot Rusty level 0
# same as
clean level 0 robot Rusty
```

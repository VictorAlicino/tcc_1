# University Final Paper

This is a system that can make a bridge between cheap IoT devices and multiple users in a same building.
Making possible that a lot of authorized people control the same light, HVAC and etc

* Opus (Local Server): Create the bridge between IoT devices and any other device necessary to control a building.

* Maestro (Public Server): Authenticate the users, keeps a relation of all Local Servers and it's the "outside of network" bridge
for controlling Local Server

* Conductor (WebApp): WebApp for an Admin control the Local Server

* Conductor Mobile (MobileApp): Any user app, basically the front-end
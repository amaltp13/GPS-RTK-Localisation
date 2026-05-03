# GPS-RTK-Localisation
This repository describes how to use the Waveshare LC29H GNSS module for GPS-based localization. 
This project uses tools from the Waveshare LC29H series, primarily the LC29H DA and LC29H BS modules. However, this repository focuses exclusively on the LC29H DA module used together with an RTK correction subscription.
If you are not familiar with GPS RTK (Real-Time Kinematic) positioning, you can refer to the following link for background information:
https://en.wikipedia.org/wiki/Real-time_kinematic_positioning
RTK GNSS systems are typically very expensive, but the Waveshare LC29H series offers a cost effective and easy to use alternative. Despite this, there is a lack of complete, ready to use documentation available online. This repository aims to bridge that gap.
Using this module, I was able to achieve an RTK fix and successfully use it for autonomous vehicle navigation with 2cm accuracy. I was able to run my robot vehicle over a 100 meter area without completely rely on the vehicle odometry.
The modules are relatively affordable (approximately ₹6000 per unit) and support both L1 and L5 frequency bands.
Waveshare provides two main variants:
•	LC29H BS – a base station module used to generate RTK correction data (not focused in this repo)
•	LC29H DA – a rover module that receives RTK corrections
Detailed discussion of the base station (LC29H BS) will be covered separately. This repository focuses on the LC29H DA, which I used along with an external RTK correction service.
I obtained the RTK correction subscription from https://www.rtkdata.com. They offer a one month free trial, after which subscriptions are available at a very low cost (approximately ₹5000 per month).
Just connect the LC29H -DA module with your PC/Raspi with micro-USB cable. Connect the antenna and you may just use the code.
There is mainly 3 codes in the repo 
1.
2.
3.

All code in this repository is developed for the ROS 2 Humble framework. You are welcome to review the code and modify it as needed to suit your project requirements.

---
layout: post
title:  "Self Driving RC Car"
date:   2022-07-16 12:11:00 +0530
categories: robot
---

<script type="text/x-mathjax-config">
	MathJax.Hub.Config({
		tex2jax: {
			inlineMath: [['$', '$']]
		}
	});
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>

<p align="center">
  <img src="/assets/car.jpeg" alt="drawing" width="400"/>
<p/>

<h1>Motivation</h1>

<p> 
I saw a talk where the speaker spoke about how modern computer vision systems should take more inspiration from biology. He described the mantis shrimp, a sea animal with two eyes that move independently of each other, and wondered whether its eyes enable better representations of the visual world. He was asking why evolution chose this design for the shrimp? And how did the design help?
</p>

<p> 
Transforming these questions into scientific inquiry would be challenging to say the least. Nevertheless, they inspired me to try to build a small-scale autonomous vehicle with mantis shrimp like eyes. I'm not there yet: my RC Car has only one eye i.e. one camera. But it can drive itself, albeit only on a particular track. I'll use this post to describe my car. Before I begin, I would like to give huge credit to the <a href="https://github.com/autorope/donkeycar">Donkeycar</a> project. I was able to build my car only due to them.
</p>

<h1>Design</h1>

<p>
I haven't found discussions on motor selection, battery selection, power consumption and weight of RC cars on the Internet. My struggles in understanding these culminated in a lot of bad designs. I think it'll be useful to describe and justify my design here. 
</p>

<p align="center">
  <img src="/assets/schematic.png" alt="drawing" width="400"/>
<p/>

<p>
The schematic (<a href="https://www.electronicshub.org/raspberry-pi-l298n-interface-tutorial-control-dc-motor-l298n-raspberry-pi/">original source</a>) shows how to control a DC motor using a Raspberry Pi. A lithium-polymer battery powers both the Raspberry Pi (4B) and the L298N motor controller. The Raspberry Pi requires an operating voltage of 5V at 2A current, which it gets from the XY-3606 DC-to-DC converter (the blue board in the schematic). It is important to connect the XY-3606 to the Pi using a USB cable. I tried to connect the two, directly using jumper wires. It didn't work: the Pi failed to boot. 
</p>

<p>
The Pi controls motor speed and direction by sending 3 signals to the L298N motor controller. Two of them (orange and green wires in the schematic) control start, break and the direction (forward or reverse). The third (yellow wire) is a PWM signal which controls the voltage supplied to the motor, and hence the car's speed. A single L298N motor controller controls 2 motors. My car has 4 motors and thus requires 2 such motor controllers. These are stitched on the underside of my car in order to save space.
</p> 

<p align="center">
  <img src="/assets/carbackside.jpeg" alt="drawing" width="400"/>
<p/>

<p> 
The total cost of all the components on the car is around 11,000 rupees. It is quite a lot but note that the Raspberry Pi, its camera module and the Lithium-Polymer batter account for nearly 75% of the total cost. These can be used for a lot of other things as well. 
</p> 

<p> 
Now that I have described my design, I'll try to justify it. My justifications are based on extremely crude models that don't represent the actual physics of the system. Still, they are useful in illustrating which variables are important and which are not.
</p> 

<h4>Battery</h4> 

<p>
Selecting the battery is obviously crucial. They are quite expensive. Before purchasing them, you have to be sure that they will be able to power the components in your circuit and will be able to run them for sufficient amount of time. 
</p> 

<p>
I collected the power requirements of components in my car. Some I obtained from their respective datasheets. Others I estimated from their operating currents and voltages. I don't have the sources for these anymore. Treat them as ball-park estimates.
</p> 

<table>
  <tr>
    <th>Component</th>
    <th>Power Consumption (W)</th>
  </tr>
  <tr>
    <td>Raspberry Pi 4B</td>
    <td>10</td>
  </tr>
  <tr>
    <td>2 L298N motor controllers</td>
    <td>50</td>
  </tr>
  <tr>
    <td>4 BO motors</td>
    <td>10</td>
  </tr>
  <tr>
    <td>XY-3606</td>
    <td>5</td>
  </tr> 
  <tr>
    <td><b>Total</b></td>
    <td><b>75</b></td>
  </tr> 
</table> 

<p>
My <a href="https://robu.in/product/orange-1000mah-3s-30c60c-lithium-polymer-battery-pack-lipo/">Lithium-Polymer</a> battery supplies a voltage of 11.1V. Since $\text{Power} = \text{Voltage} \times \text{Current}$, the discharge rate is $\frac{\text{Power}}{\text{Voltage}} = \frac{70}{11.1} \approx 6.3A$. This is well within the rated discharge rate for my battery. 
</p>

<p>
I can also estimate the battery life by reading the battery capacity. The battery contains $1000mAh$ of charge. In SI units, this is $1000 \times 10^{-3} \times 3600 = 3600C$. Now assuming that I can discharge the battery completely, I get $\frac{3600}{6.3} \approx 10 \text{ minutes}$ of battery life. 
</p>

<p>
This analysis should raise a lot of eyebrows. For one, Lithium-Polymer batteries should never be discharged completely. Doing so would render them unsafe for future use. Moreover, batteries don't supply constant power as they discharge. Power supply diminishes through battery operation. This means that my calculation of the discharge rate and battery life is not really accurate. Nevertheless, these back-of-the-envelope calculations helped me be sure that my car could run and would do so, at least for a few minutes. 
</p> 

<h4>Force</h4> 

<p> 
In order for the car to move, it has to overcome friction. Frictional force is often modelled as $F_{\text{friction}} = \mu \times M \times g$. The mass of my car $M$ is around 0.5Kg, the coefficient of friction $\mu$ is usually less than 1 and $g$ is acceleration due to gravity, $10 m/s^2$. If the motors can provide a force greater than $1 \times 0.5 \times 10 = 5N$, the car should move.
</p> 

<p> 
Motors convert electrical power to mechanical power. The cheap DC motors that I use, do so with around 50% efficiency. This means that we get $0.5 \times 10W = 5W$ of mechanical power to work with. 
<p> 

<p> 
Mechanical power is $F_{\text{motors}} \times v_{\text{car}}$. Since the motor turns at 150 rpm or about 15 rad/s, the velocity of the car is $v_{\text{car}} = \text{wheel radius} \times \omega = 2 cm \times 15 rad/s = 0.3 m/s$. Hence $F_{\text{motor}} = \frac{5W}{0.3m/s} \approx 17N$. This is more than $F_{\text{friction}}$ with some margin. The car should move. In practice, it does!
</p>

<p> 
Even with these crude arguments, few things become apparent. For example, your car shouldn't be too heavy. Perhaps this was already obvious. But some other things were not, at least to me. For example, wheel radius is an important variable. It trades of the car's velocity for motor's force. If your car doesn't move, try reducing the wheel radius. I learnt this the hard way when I bought monster wheels only to later have to bin them when the car didn't move. 
</p>

<h1>Software</h1> 

<p>
I installed the Donkeycar github repository. It has a lot of useful features that make experiments easier. You can launch a web server on the Pi and control your car through a web browser. There is a convenient way to define parts in your car and interface between them. They even save data for you as you drive. You can use this later as training data for your neural networks.
</p>

<p>
Donkeycar also advices you to install Tensorflow or Pytorch on your Pi. It wasn't easy to install these. The pre-built python wheels didn't work for me. In the end, I abandoned them, instead installing the lightweight ONNX runtime for neural network inference. 
</p>

<p> 
Donkeycar has also provides predefined templates for 2 wheel differential drive using the L298N motor controllers. These specify which pins on the Pi control what. Differential dirve lets you can steer the car by controlling the speeds of 2 motors. For example, to turn left, you would turn the left side wheel slowler than the right wheel. Since my car has 4 wheels, I had to define my own template. You can find it in this <a href="https://github.com/autorope/donkeycar/pull/1019">pull request</a> for your reference. 
</p>

<h1>Driving it around</h1> 

<p>
I enjoy driving the car around. Part of my motivation in building it was to show it off to other people. Such projects were quite common in my college, but they are rarer back at home. I kind of miss that environment now that I have graduated. It would be nice to have a community such as Donkeycar's where people got together to learn about this kind of stuff. People, regardless of age, will always find something like this very interesting. It can be an easy gateway to learning deeply about today's technological buzzwords such as IoT and Machine Learning. 
</p> 

<p> 
Sometimes when I'm driving the car around, people ask me how I built it? how much did it cost? how does it work? how does it move on its own? To the last question, initially, I gave some vague reply, "Oh, it'll be tough to explain". That person pushed me, "You think I won't understand?". So I explained that I had recorded myself driving and he immediately got it, "Oh so it is copying your behaviour". This is quite accurate. Maybe I can explain it to people at different levels of detail. It is not always necessary to describe what neural networks are and what backpropagation is.
</p> 

<p> 
I get fascinated by how children interact with the car. They'll run in front of it or chase it. One toddler even tried to poke it, as if it were a dog. Sometimes, I let them drive it. It is a good way to stress-test the car. Since it is hard for them to control the car, they'll often drive it off the track or into a wall or turn it upside-down. It makes them laugh and so far my car is intact. 
</p>

<p align="center"> 
 <video width="400" height="400" controls>
   <source src="/assets/movie.mp4" type="video/mp4">
 </figure>
</p>

<h1>Training Self-Driving Module</h1>

<p>
I collected training data using Donkeycar's web app by driving around a small track near my house. I visualized histograms of throttles and steering angles and found that I drove at a constant throttle. Hence I chose to only predict the steering angles through a neural network. 
</p>

<p>
The inputs to my neural network were the camera image and 5 previous steering commands. From this, the network predicted the next steering command. I augmented the training images by color jittering, adjusting sharpness and inverting them at random. 
</p>

<p>
I used the ImageNet-pretrained MobileNet-V2 network available in TorchVision as the convolutional branch in the network. I found that this model is at least twice as fast as ResNet-18 on the Pi. Finally, I held out a portion of the training data for validation and plotted network predictions along with ground truth steering commands. This is my <a href="https://colab.research.google.com/drive/1v24nXC2KOibLp5mg60A8y0_wthuUE04o?usp=sharing">Colab notebook</a> where I pondered over neural architectures and such.
</p> 

<p align="center">
  <img src="/assets/val.png" alt="val" width="400"/>
<p/>

<h1>Driving on its own</h1> 

<p> 
The trained neural network predicted steering controls almost perfectly on the validation set. But when I deployed it to my car, things didn't go so well. The car kept going off track. Even the camera stick broke, ending experiments for the day. 
</p>

<p>
I think the main problem was the difference in the training and deployment environments. I collected training data by driving the car at full throttle with Donkeycar backing up snapshots of $(\text{image}_t, \text{throttle}_t, \text{angle}_t)$ 20 times per second. On the other hand, the neural network could make steering predictions only 10 times per second. 
<p> 

<p> 
This was important because the network relied on previous predictions in order to make the next. In the training data, the car had moved by distance $d$ between subsequent frames, but when the model was deployed, the car moved by distance $2 \times d$ between subsequent neural network evaluations. By then, it would already be off track. 
</p>

<p>
I had two options to fix this. The first was to speed up inference, possibly by quantizing the model. This wasn't straightforward because there is limited operator support for quantized models on ONNX. I could try <a href="https://pytorch.org/tutorials/intermediate/realtime_rpi.html">torch.jit</a> but it requires a 64 bit OS. My Raspberry Pi runs on the 32 bit OS since the PiCam library, which Donkeycar uses to interface with the camera, is deprecated in the 64 bit OS.
</p>

<p>
The second option was to simply run the car at half the speed. The deployed network would observe new images after the car had covered the same distance as it had in the training data. This idea was not only easier to implement but more importantly, successful. Below you can see the car moving on its own. It still crashes every now and but its much better than what it was like before. 
</p>

<p align="center"> 
 <video width="400" height="400" controls>
   <source src="/assets/drive.mp4" type="video/mp4">
 </figure>
</p>

<h1>Next Steps</h1>

<p>
There is a lot that excites me about this car. I want to explore its potential as a medium for education. It would be great if I can get even one other person in my area excited about this project and have them build there own car. 
</p>

<p> 
Right now, the car doesn't know anything about it's own position and velocity. I would like to integrate sensors for odometry. With this, I could learn more about path planing and algorithms such as SLAM. I saw a <a href="https://www.youtube.com/watch?v=o9jEQZn6I6E">talk</a> by Joydeep Biswas and it would be fun to implement one of his papers on my car. In his talk, he envisions a fleet of autonomous vehicles. We could call such a fleet a Redundant Array of Inexpensive Cars. 
</p> 

<p> 
I can also try to improve inference on the Pi. The main bottleneck right now seems to be the dependency on the 32 bit OS. I should try to build a clone of PiCam compatible with the 64 bit OS. In this way I would also be giving something back to the Donkeycar project. 
</p>

<h1>Credits</h1> 

I depended on a lot of resources on the Internet at various moments. The biggest of them all is Donkeycar which I have already mentioned. Apart from them, I used <a href="https://www.tomshardware.com/reviews/raspberry-pi-headless-setup-how-to,6028.html">Tom's Hardware</a> to figure out how to setup the Pi via SSH. I found out how to connect the Pi to mobile hotspot from this <a href="https://medium.com/geekculture/how-to-connect-to-the-raspberry-pi-using-mobile-hotspot-2362a6b02efc">Medium Article</a>. I was able to build the circuit with help from a <a href="https://www.youtube.com/watch?v=lPyDtuzYE5s&t=959s">YouTube Video</a> and this <a href="https://www.electronicshub.org/raspberry-pi-l298n-interface-tutorial-control-dc-motor-l298n-raspberry-pi/">Article</a>.

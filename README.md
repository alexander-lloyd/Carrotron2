# Carrotron2 

**Carrotron2** is a robot that can use infrared to create a radar of its
      surroundings. *With working motors, we would also have liked to have
      added pathfinding and GPS support :)*

### The robot

  The robot is controlled via Raspberry Pi and Arduino units. We have a servo
  attached to the front, onto which the infrared sensor is mounted, enabling
  a 180 degree vision for the radar.

### Mapping

  Using an infrared sensor attached to the front of the robot, we are able
  to obtain estimations of distances to the nearest solid object. By
  rotating these sensors constantly, we can obtain a live 'radar' of the
  surroundings.

  The infrared sensor is connected to an analogue pin on the **Arduino**, which
  can be read via the **Raspberry Pi**. This gives us a logarithmic value for
  distance, which we pass to the **Flask** server and convert to millimeters.
  Using **Socket.IO** we can transmit this value via a socket to the **React** web
  app, which then finally converts this distance into a pixel representation
  and draws it on the canvas.
 
### *Extensions: Pathfinding*

  Unfortunately our motors for the wheels do not quite work correctly, so we
  have been unable to implement any kind of movement on the robot. Once basic
  movements have been added, it would then be possible to add GPS support using
  the GPS module for the Arduino.


  Basic pathfinding is possible using the **[bug algorithm](https://www.cs.cmu.edu/~./motionplanning/lecture/Chap2-Bug-Alg_howie.pdf)**

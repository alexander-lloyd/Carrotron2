import React from 'react';
import { Card, CardTitle } from 'react-materialize';

const About = () => (
  <div>
    <div className="App">
    <div className="About">
    <h1>About the project</h1>
    <p className="App-intro justify">
      <b>Carrotron2</b> is a robot that can use infrared to create a radar of its
      surroundings. <i>With working motors, we would also have liked to have
      added pathfinding and GPS support :)</i>
    </p>
    <h3>The robot</h3>
    <p className="App-intro justify">
      The robot is controlled via Raspberry Pi and Arduino units. We have a servo
      attached to the front, onto which the infrared sensor is mounted, enabling
      a 180 degree vision for the radar.
    </p>
    <h3>Mapping</h3>
    <p className="App-intro justify">
      Using an infrared sensor attached to the front of the robot, we are able
      to obtain estimations of distances to the nearest solid object. By
      rotating these sensors constantly, we can obtain a live 'radar' of the
      surroundings.
    </p>
    <p className="App-intro justify">
      The infrared sensor is connected to an analogue pin on the <b>Arduino</b>, which
      can be read via the <b>Raspberry Pi</b>. This gives us a logarithmic value for
      distance, which we pass to the <b>Flask</b> server and convert to millimeters.
      Using <b>Socket.IO</b> we can transmit this value via a socket to the <b>React</b> web
      app, which then finally converts this distance into a pixel representation
      and draws it on the canvas.
    </p>
    <h3><i>Extensions: Pathfinding</i></h3>
    <p className="App-intro justify">
      Unfortunately our motors for the wheels do not quite work correctly, so we
      have been unable to implement any kind of movement on the robot. Once basic
      movements have been added, it would then be possible to add GPS support using
      the GPS module for the Arduino.
    </p>
    <p className="App-intro justify">
      Basic pathfinding is possible using the <b><a href="https://www.cs.cmu.edu/~./motionplanning/lecture/Chap2-Bug-Alg_howie.pdf">bug algorithm</a></b>.
    </p>
    </div>

    <h1>Who are we?</h1>
    </div>
    <div className="cards">
        <Card className='small'
    	     header={<CardTitle image='img/harry.jpg'>Harry Brown</CardTitle>}
    	     actions={[<a href='https://harryrbrown.github.io'>My website</a>]}>
           Second-year Computing student at Imperial College London.
        </Card>
        <Card className='small'
           header={<CardTitle image='img/alexl.jpg'><div style={{color: '#000'}}>Alex Lloyd</div></CardTitle>}
           actions={[<a href='https://github.com/alexander-lloyd'>Github</a>]}>
           Second-year Computer Science student at the University of Birmingham.
        </Card>
        <Card className='small'
           header={<CardTitle image='img/chrisl.jpg'>Chris Lloyd</CardTitle>}
           actions={[<a href='https://github.com/terimater2'>Github</a>]}>
           First-year Visual Effects student at Birmingham City University.
        </Card>
    </div>
  </div>
);

export default About;

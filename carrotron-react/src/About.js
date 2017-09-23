import React from 'react';
import { Card, CardTitle } from 'react-materialize';

const About = () => (
  <div>
    <div className="App">
    <div className="About">
    <h1>About the project</h1>
    <p className="App-intro">
      <b>Carrotron2</b> is a robot that can be driven, instructed to navigate to
      GPS coordinates, and map its surroundings using ultrasound and infrared
      scanners.
    </p>
    <h3>The robot</h3>
    <p className="App-intro">
      The robot is controlled via Raspberry Pi and Arduino units.
    </p>
    <h3>Pathfinding</h3>
    <p className="App-intro">
      The robot implements the
    </p>
    <h3>Mapping</h3>
    <p className="App-intro">
      Using an ultrasound and an infrared sensor attached to the front of the
      robot, we are able to obtain estimations of distances to the nearest solid
      object. By rotating these sensors constantly, we can obtain a live 'radar'
      of the surroundings.
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

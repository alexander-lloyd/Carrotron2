import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import './App.css';
import { subscribeToInfrared } from './api';

class Home extends Component {
  constructor() {
    super();
    this.drawRobot = this.drawRobot.bind(this);
    this.drawBoundary = this.drawBoundary.bind(this);
    this.drawDir = this.drawDir.bind(this);
    this.drawObject = this.drawObject.bind(this);
    this.sensorPoint = this.sensorPoint.bind(this);

    subscribeToInfrared((err, dict) => this.drawPoints(dict));
  }

  componentDidMount() {
    let canvas = ReactDOM.findDOMNode(this.refs.myCanvas);
    this.ctx = canvas.getContext('2d');
    this.drawBoundary();
    this.drawRobot();
    // var bg = this.ctx.getImageData(0, 0, 800, 800);
    //
    // this.drawObject(90, 20);
  }

  drawDir(theta) {
    var r = 800;
    this.ctx.beginPath();
    this.ctx.setLineDash([4, 8]);
    this.ctx.moveTo(400, 610);
    this.ctx.lineTo(400 - r * Math.cos(theta * Math.PI / 180.0), 610 - r * Math.sin(theta * Math.PI / 180.0));
    this.ctx.stroke();
  }

  drawObject(theta, distance) {
    // scale distance into pixels
    var dist = distance;
    // set size of dot
    var pixelSize = 8;

    this.ctx.fillStyle = 'rgb(30, 30, 30)';
    this.ctx.fillRect(400 - dist * Math.cos(theta * Math.PI / 180.0), 610 - dist * Math.sin(theta * Math.PI / 180.0), pixelSize, pixelSize);
  }

  drawPoints(dict) {
    this.ctx.clearRect(0, 0, 800, 800);
    this.componentDidMount();
    console.log(dict);
    Object.entries(dict).map(([degrees, distance]) => {
      this.drawObject(degrees, distance / 2.0);
    })
  }

  drawRobot() {
    this.ctx.fillStyle = 'rgb(0, 0, 0)';
    this.ctx.fillRect(375, 600, 50, 60);
  }

  drawBoundary() {
    this.ctx.fillStyle = 'rgb(200,200,200)';
    this.ctx.fillRect(0, 620, 800, 180);
    this.ctx.fillStyle = 'rgb(55,55,55)';
    this.ctx.fillRect(10, 640, 50, 5);
    this.ctx.font = "20px Arial";
    this.ctx.fillText("10cm", 10, 670);
  }

  sensorPoint(theta) {
    this.drawDir(theta);
  }

  render() {
    return (
      <div className="App">
        <h1>Home</h1>
        <p className="App-intro">
          Live radar map of the Carrotron
        </p>
        <canvas ref="myCanvas" width="800" height="700" style={{border: 1 + 'px solid'}} />
      </div>
    );
  }
}

export default Home

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
  }

  componentDidMount() {
    let canvas = ReactDOM.findDOMNode(this.refs.myCanvas);
    this.ctx = canvas.getContext('2d');
    this.drawBoundary();
    this.drawRobot();
    var bg = this.ctx.getImageData(0, 0, 800, 800);
    this.drawObject(90, 2.314);
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
    var dist = distance * 210;

    // set size of dot
    var pixelSize = 5;

    this.ctx.fillStyle = 'rgb(30, 30, 30)';
    this.ctx.fillRect(400 - dist * Math.cos(theta * Math.PI / 180.0), 610 - dist * Math.sin(theta * Math.PI / 180.0), pixelSize, pixelSize);
  }

  drawRobot() {
    this.ctx.fillStyle = 'rgb(0, 0, 0)';
    this.ctx.fillRect(375, 600, 50, 60);
  }

  drawBoundary() {
    this.ctx.fillStyle = 'rgb(200,200,200)';
    this.ctx.fillRect(0, 620, 800, 180);
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

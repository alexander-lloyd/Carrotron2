import openSocket from 'socket.io-client';
const socket = openSocket('http://localhost:3001');

function subscribeToInfrared(cb) {
  socket.on('subscribeToData', timestamp => cb(null, timestamp));
  socket.emit('subscribeToInfrared', 1000);
}

export { subscribeToInfrared };

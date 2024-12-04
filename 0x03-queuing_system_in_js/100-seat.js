import redis from 'redis';
import { promisify } from 'util';
import { createQueue } from 'kue';
import express from 'express';

const client = redis.createClient();
const queue = createQueue();
const app = express();
const port = '1245';

let reservationEnabled = true;

function reserveSeat(number) {
  client.set('available_seats', number);
}

async function getCurrentAvailableSeats() {
  const getAsync = promisify(client.get).bind(client);
  const availableSeats = await getAsync('available_seats');

  return Number(availableSeats);
}

app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  res.send({'numberOfAvailableSeats': availableSeats});
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    res.send({ "status": "Reservation are blocked" });
    return;
  }
  res.send();
  const reserveSeatJob = queue.create('reserve_seat').save((err) => {
    if (!err) {
      res.send({ "status": "Reservation failed" });
    }
    res.send({ "status": "Reservation in process" }); 
  });

  reserveSeatJob.on('complete', () => {
    console.log('Seat reservation job JOB_ID completed');
  })

  reserveSeatJob.on('failed' (err) => {
    console.log(`Seat reservation job JOB_ID failed: ${err}`);
  });
  
});

app.get('/process', (req, res) => {
  queue.process('reserve_seat', async (job, done) => {
    let availableSeats = await getCurrentAvailableSeats();

    availableSeats -= 1;
    reserveSeat(availableSeats);

    if (availableSeats === 0) {
      reservationEnabled = false;
    }
    if (!availableSeats || availableSeats < 0) {
      done(new Error('Not enough seats available'));
    }
    res.send({ "status": "Queue processing" });
  });
});

import kue from 'kue';

const queue = kue.createQueue();

const jobs = {
  phoneNumber: '+201552077841',
  message: 'Hello, it\'s Ahmed'
}

const job = queue.create('push_notification_code', jobs).save((err) => {
  if (!err){
    console.log(`Notification job created: ${job.id}`);
  }
});

job.on('complete', () => console.log('Notification job completed'));
job.on('failed', ()=> console.log('Notification job failed'));

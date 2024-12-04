import kue from 'kue';

import createPushNotificationsJobs from './8-job.js';

import { expect } from 'chai';
import { spy } from 'sinon';

const queue = kue.createQueue();

describe('Job Queue Tests', () => {
  const queue = kue.createQueue();

  before(() => {
    queue.testMode.enter();
  });
  afterEach(() => {
    queue.testMode.clear();
  });
  after(() => {
    queue.testMode.exit();
  });

  it('should add a job to the queue', () => {
    const consoleSpy = spy(console, 'log');
    const jobs = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account'
      }
    ];
    createPushNotificationsJobs(jobs, queue);
    expect(queue.testMode.jobs.length).to.equal(1);
    expect(consoleSpy.calledOnce).to.be.true;	
  });

  it('should add jobs with expected data', () => {
    const jobs = [
      {
        phoneNumber: '4153518780',                                  message: 'This is the code 1234 to verify your account'
      }
    ];
    createPushNotificationsJobs(jobs, queue);
    expect(queue.testMode.jobs[0].data).to.equal(jobs[0]);
  });

  it('should throw error for wrong data type', () => {
    const jobs = {phoneNumber: '4153518780', message: 'This is the code 1234 to verify your account'};
    expect(() => createPushNotificationsJobs(jobs, queue)).to.throw('Jobs is not an array');
  });
})

const kafka = require('kafka-node');
const Consumer = kafka.Consumer;
const client = new kafka.KafkaClient({ kafkaHost: 'localhost:9092' });
const consumer = new Consumer(
  client,
  [{ topic: 'registration-topic', partition: 0 }],
  { autoCommit: true }
);

consumer.on('message', (message) => {
  console.log('Received message:', message.value);
  const registrationData = JSON.parse(message.value);
  // Process registration data (e.g., save to database)
  console.log(registrationData);
});

consumer.on('error', (error) => {
  console.error('Consumer error:', error);
});

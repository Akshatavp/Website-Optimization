const kafka = require("kafka-node");
const Consumer = kafka.Consumer;
const client = new kafka.KafkaClient({ kafkaHost: "localhost:9092" });
const consumer = new Consumer(
  client,
  [{ topic: "registration-topic", partition: 0 }],
  { autoCommit: true }
);
const DataModel = require("../schema/dataSchema");

consumer.on("message", (message) => {
  console.log("Received message:", message.value);
  const registrationData = JSON.parse(message.value);
  const data = new DataModel(registrationData);
  data.save();
  // console.log(registrationData);
});

consumer.on("error", (error) => {
  console.error("Consumer error:", error);
});

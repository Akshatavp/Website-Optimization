const kafka = require("kafka-node");
const Producer = kafka.Producer;
const client = new kafka.KafkaClient({ kafkaHost: "localhost:9092" });
const producer = new Producer(client);
const Product = require("../schema/productSchema");

producer.on("ready", () => {
  console.log("Kafka Producer is connected and ready.");
});

producer.on("error", (error) => {
  console.error("Producer error:", error);
});

const sendMessage = (message) => {
  const payloads = [
    {
      topic: "registration-topic",
      messages: JSON.stringify(message),
      partition: 0,
    },
  ];
  producer.send(payloads, (error, data) => {
    if (error) {
      console.error("Failed to send message:", error);
    } else {
      console.log(data);
    }
  });
};

module.exports = sendMessage;

const kafka = require("kafka-node");
const DataModel = require("../schema/dataSchema");
const Producer = kafka.Producer;
const client = new kafka.KafkaClient({ kafkaHost: "localhost:9092" });
const producer = new Producer(client);

producer.on("ready", () => {
  console.log("Kafka Producer is connected and ready.");
});

producer.on("error", (error) => {
  console.error("Producer error:", error);
});

// Function to send messages
const sendMessage = async (message) => {
  // Construct payloads
  const payloads = [
    {
      topic: "registration-topic",
      messages: JSON.stringify(message),
      partition: 0,
    },
  ];

  const data = new DataModel(message);
  await data.save();

  // Check if the producer is ready
  if (producer.ready) {
    producer.send(payloads, (error, data) => {
      if (error) {
        console.error("Failed to send message:", error);
      } else {
        console.log("Message sent successfully:", data);
      }
    });
  } else {
    console.error("Producer is not ready.");
  }
};

module.exports = sendMessage;

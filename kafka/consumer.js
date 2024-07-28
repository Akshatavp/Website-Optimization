const kafka = require("kafka-node");
const DataModel = require("../schema/dataSchema");
const Product = require("../schema/productSchema");
const client = new kafka.KafkaClient({ kafkaHost: "localhost:9092" });
const Consumer = kafka.Consumer;
const consumer = new Consumer(
  client,
  [{ topic: "registration-topic", partition: 0 }],
  { autoCommit: true, groupId: "registration-group" }
);

// Configuration for batching
const BATCH_SIZE = 5; // Number of messages per batch
const FLUSH_INTERVAL = 5000; // Time in milliseconds to flush the batch

let batch = [];

// Function to flush batch to MongoDB
const flushBatch = async () => {
  if (batch.length === 0) return;

  try {
    console.log(`Flushing batch of ${batch.length} messages`);
    await DataModel.insertMany(batch);
    console.log("Batch saved successfully");
    batch = []; // Clear the batch after saving
  } catch (error) {
    console.error("Error saving batch:", error);
  }
};

// Set up interval for flushing
setInterval(flushBatch, FLUSH_INTERVAL);

consumer.on("message", async (message) => {
  console.log("Received message:", message.value);
  try {
    const registrationData = JSON.parse(message.value);
    console.log(registrationData.data);
    const data = new Product({
      data: registrationData.data,
    });
    // await data.save();

    // batch.push(registrationData);

    // // Flush the batch if it reaches the batch size
    // if (batch.length >= BATCH_SIZE) {
    //   flushBatch();
    // }
  } catch (error) {
    console.error("Error processing message:", error);
  }
});

consumer.on("ready", () => {
  console.log("Kafka Consumer is connected and ready.");
});

consumer.on("error", (error) => {
  console.error("Consumer error:", error);
});

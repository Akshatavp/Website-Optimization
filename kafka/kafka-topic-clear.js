const { Kafka } = require("kafkajs");

const kafka = new Kafka({
  clientId: "my-app",
  brokers: ["localhost:9092"],
});

const admin = kafka.admin();

async function clearTopicMessages(topicName) {
  try {
    // Connect to Kafka
    await admin.connect();
    console.log(`Connected to Kafka`);

    // Get current topic configuration
    const topicConfigs = await admin.fetchTopicMetadata({
      topics: [topicName],
    });
    const currentConfig = topicConfigs.topics[0].configEntries;

    console.log(`Current topic configuration:`, currentConfig);

    // Temporarily set retention to a short time (e.g., 1 minute)
    await admin.alterConfigs({
      resources: [
        {
          type: 0, // Topic type
          name: topicName,
          config: {
            "retention.ms": "60000", // Retention time in milliseconds
          },
        },
      ],
    });
    console.log(`Retention policy for '${topicName}' set to 1 minute`);

    // Wait for the retention period to elapse
    await new Promise((resolve) => setTimeout(resolve, 60000));

    // Revert retention time to its original value (e.g., 7 days)
    await admin.alterConfigs({
      resources: [
        {
          type: 0, // Topic type
          name: topicName,
          config: {
            "retention.ms": "604800000", // Retention time in milliseconds (7 days)
          },
        },
      ],
    });
    console.log(`Retention policy for '${topicName}' reverted to 7 days`);
  } catch (error) {
    console.error("Error clearing topic messages:", error);
  } finally {
    // Disconnect from Kafka
    await admin.disconnect();
  }
}

clearTopicMessages("registration-topic");

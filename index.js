const express = require("express");
const sendMessage = require("./kafka/producer");
const app = express();
const path = require("path");
const port = 3000;
var cors = require("cors");
const mongoose = require("mongoose");
const DBconnect = require("./utils/DBconnection");
const Product = require("./schema/productSchema");
const data = require("./data/data.json");

app.use(express.json());
app.use(cors());

// Request counter and timestamp tracking
let requestCount = 0;
let startTime = Date.now();

DBconnect();

app.post("/register", (req, res) => {
  requestCount++;
  const registrationData = req.body;
  sendMessage(registrationData);
  res.status(202).send("Registration request received.");
});

app.get("/", (req, res) => {
  requestCount++;
  res.sendFile(path.join(__dirname, "client", "index.html"));
});

app.get("/products", (req, res) => {
  requestCount++;
  res.json(data);
});

// Periodically log the request rate
setInterval(() => {
  const currentTime = Date.now();
  const elapsedSeconds = (currentTime - startTime) / 1000;
  console.log(`Requests per second: ${requestCount / elapsedSeconds}`);
  requestCount = 0; // Reset counter
  startTime = currentTime; // Reset start time
}, 1000); // Log every second

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}/`);
});

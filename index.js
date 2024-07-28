const express = require("express");
require("dotenv").config();
const sendMessage = require("./kafka/producer");
const app = express();
const path = require("path");
const port = 3000;
var cors = require("cors");
const DBconnect = require("./utils/DBconnection");
// const data = require("./data/data.json");
const Product = require("./schema/productSchema");

app.use(express.json());
app.use(cors());

app.use(
  express.static(path.join(__dirname, "public"), {
    extensions: ["html", "htm", "gif", "png", "jpg"],
  })
);

// Request counter and timestamp tracking
let requestCount = 0;
let startTime = Date.now();

DBconnect();

app.post("/register", (req, res) => {
  requestCount++;
  const registrationData = req.body;
  sendMessage(registrationData);
  res.status(200).send("Registration request received.");
});

app.get("/", (req, res) => {
  requestCount++;
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.get("/products", async (req, res) => {
  requestCount++;
  const data = await Product.find();
  res.json(data);
});

// Periodically log the request rate
setInterval(() => {
  const currentTime = Date.now();
  const elapsedSeconds = (currentTime - startTime) / 1000;
  console.log(`Requests per second: ${requestCount / elapsedSeconds}`);
  requestCount = 0;
  startTime = currentTime;
}, 1000);

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}/`);
});

const mongoose = require("mongoose");

const DBconnect = () => {
  const DB =
    "mongodb://localhost:27017/Webopti" || "mongodb://my-mongodb:27017/Webopti";

  mongoose.connect(DB, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
    serverSelectionTimeoutMS: 30000,
  });

  const db = mongoose.connection;
  db.on("error", console.error.bind(console, "connection error:"));
  db.once("open", () => {
    console.log("Connected to MongoDB");
  });
};
module.exports = DBconnect;

const mongoose = require("mongoose");

const dataSchema = new mongoose.Schema({
  data: String,
});

const DataModel = mongoose.model("data", dataSchema);

module.exports = DataModel;

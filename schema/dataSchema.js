const mongoose = require("mongoose");

const dataSchema = new mongoose.Schema({
  data: {
    type: String,
  },
});

const DataModel = mongoose.model("DataModel", dataSchema);

module.exports = DataModel;

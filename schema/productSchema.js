const mongoose = require("mongoose");

const productSchema = new mongoose.Schema({
  image: String,
  alt: String,
  title: String,
  description: String,
  price: String,
  button: {
    text: String,
    link: String,
  },
});

const Product = mongoose.model("products", productSchema);

module.exports = Product;

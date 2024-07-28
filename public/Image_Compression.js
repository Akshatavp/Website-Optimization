const tinify = require("tinify");
const fs = require("fs");
const path = require("path");

tinify.key = "67K2X2z0tsyRBQ0WqDbq7hwrVfgwccq4";

const optimizeImage = async (inputPath, outputPath) => {
  try {
    await tinify.fromFile(inputPath).toFile(outputPath);
    console.log(`Optimized: ${outputPath}`);
  } catch (err) {
    console.error(`Error optimizing ${inputPath}:`, err);
  }
};

const optimizeImagesInDir = async (dir) => {
  const files = fs.readdirSync(dir);
  for (const file of files) {
    const inputPath = path.join(dir, file);
    const outputPath = path.join(dir, file);
    if (fs.lstatSync(inputPath).isFile()) {
      await optimizeImage(inputPath, outputPath);
    }
  }
};

optimizeImagesInDir(path.join(__dirname, "images")).then(() => {
  console.log("Image optimization complete.");
});

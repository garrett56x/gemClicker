const robot = require("robot");
const Jimp = require("jimp");
const pixelmatch = require("pixelmatch");

const screenX = 0;
const screenY = 0;
const screenWidth = 700;
const screenHeight = 900;

// Load the button reference image
let buttonImage;

Jimp.read("./button.png")
  .then((img) => {
    buttonImage = img;
  })
  .catch((err) => console.error("Failed to load button image:", err));

// Function to capture the screen and look for the button
async function findAndClickButton() {
  if (!buttonImage) {
    console.log("Button image not loaded yet.");
    return;
  }

  // Take a screenshot of the game area
  const screen = robot.screen.capture(
    screenX,
    screenY,
    screenWidth,
    screenHeight
  );
  const screenImage = new Jimp(screen.width, screen.height);

  // Convert Robot screenshot to Jimp image
  let i = 0;
  for (let y = 0; y < screen.height; y++) {
    for (let x = 0; x < screen.width; x++) {
      const r = screen.image[i++];
      const g = screen.image[i++];
      const b = screen.image[i++];
      i++; // Skip alpha channel
      screenImage.setPixelColor(Jimp.rgbaToInt(r, g, b, 255), x, y);
    }
  }

  // Scan for the button using pixelmatch
  let minDiff = Infinity;
  let bestX = -1,
    bestY = -1;

  for (let x = 0; x <= screen.width - buttonImage.width; x++) {
    for (let y = 0; y <= screen.height - buttonImage.height; y++) {
      const cropped = screenImage
        .clone()
        .crop(x, y, buttonImage.width, buttonImage.height);
      const diffImage = new Jimp(buttonImage.width, buttonImage.height);

      let diff = pixelmatch(
        cropped.bitmap.data,
        buttonImage.bitmap.data,
        diffImage.bitmap.data,
        buttonImage.width,
        buttonImage.height,
        { threshold: 0.1 }
      );

      if (diff < minDiff) {
        minDiff = diff;
        bestX = x;
        bestY = y;
      }
    }
  }

  // If the match is good, click the button
  if (minDiff < 10) {
    // Adjust threshold if needed
    const clickX = screenX + bestX + buttonImage.width / 2;
    const clickY = screenY + bestY + buttonImage.height / 2;

    console.log(`Button found at (${clickX}, ${clickY}) - Clicking!`);
    robot.moveMouse(clickX, clickY);
    robot.mouseClick();
  } else {
    console.log("Button not found.");
  }
}

// Run every 15 seconds
setInterval(findAndClickButton, 15 * 1000);

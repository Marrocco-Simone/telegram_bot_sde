const fs = require('fs');
const path = require('path');

const baseUrlPath = path.join(__dirname,'weatherUrl.txt');
const tokenPath = path.join(__dirname,'weatherToken.txt');

const baseUrl = fs.readFileSync(baseUrlPath,'utf-8');
const token = fs.readFileSync(tokenPath,'utf-8');

const getWeatherUrl = (latitude = 46.07, longitude = 11.13) => {
    const url = `${baseUrl}?query=${latitude},${longitude}&access_key=${token}`;
    return url;
};

module.exports = getWeatherUrl;
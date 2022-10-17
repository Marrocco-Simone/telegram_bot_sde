const fs = require('fs');
const path = require('path');

const baseUrlPath = path.join(__dirname,'geocodingUrl.txt');
const tokenPath = path.join(__dirname,'geocodingToken.txt');

const baseUrl = fs.readFileSync(baseUrlPath,'utf-8');
const token = fs.readFileSync(tokenPath,'utf-8');

const getGeocodingUrl = (address = 'Trento') => {
    if(!address) address = 'Trento';
    //substitute spaces with %20
    address = encodeURIComponent(address.trim());
    const url = `${baseUrl}${address}.json?limit=1&access_token=${token}`;
    return url;
};

module.exports = getGeocodingUrl;
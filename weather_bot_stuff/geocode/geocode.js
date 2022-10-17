const getGeocodingUrl = require('./getGeocodingUrl');
const request = require('request');

const geocode = (address, callback) => {

    const geocodingUrl = getGeocodingUrl(address);
    //console.log(`link of geocoding: ${geocodingUrl}\n`);
    
    request({ url: geocodingUrl , json: true }, (err,res) => {
        if(err){
            callback(`Can't connect to the server`,undefined);
            return;
        }
        if(res.body.message === "Not Found" || res.body.features.length === 0){
            callback('Location not found',undefined);
            return;
        }
    
        const geocodingData = res.body;

        callback(undefined,{
            geocodingName: geocodingData.features[0].place_name,
            latitude: geocodingData.features[0].center[1],
            longitude: geocodingData.features[0].center[0]
        });
    })
}

module.exports = geocode;
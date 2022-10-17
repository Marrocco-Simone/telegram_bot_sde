const getWeatherUrl = require('./getWeatherUrl');
const request = require('request');

const weather = (latitude, longitude, callback) => {

    const weatherUrl = getWeatherUrl(latitude,longitude);
    //console.log(`link of weather: ${weatherUrl}\n`);

    request({ url: weatherUrl, json: true },(err,res) => {
        if(err){
            callback(`Can't connect to the server`,undefined);
            return;
        }
        if(res.body.success===false){
            callback(`error in fetching weather data, code ${weatherData.error.code}: ${weatherData.error.info}`,undefined);
            return;
        }

        const weatherData = res.body;
        
        callback(undefined,{
            weatherName: weatherData.location.name,
            temperature: weatherData.current.temperature,
            feelslike: weatherData.current.feelslike,
            precip: weatherData.current.precip
        });
    });
}

module.exports = weather;
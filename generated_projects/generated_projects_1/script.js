let latitude; // Latitude
let longitude; // Longitude

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition, showError);
  } else {
    console.log("Geolocation is not supported by this browser.");
    // Optionally, use a default location if geolocation is not supported
    getWeatherData(40.7128, -74.0060).then(weatherData => {
            if (weatherData) {
                displayCurrentWeather(weatherData);
                displayForecast(weatherData);
            }
        });
  }
}

function showPosition(position) {
  latitude = position.coords.latitude;
  longitude = position.coords.longitude;
  console.log("Latitude: " + latitude + "\nLongitude: " + longitude);
  getWeatherData(latitude, longitude).then(weatherData => {
        if (weatherData) {
            displayCurrentWeather(weatherData);
            displayForecast(weatherData);
        }
    });
}

function showError(error) {
  switch(error.code) {
    case error.PERMISSION_DENIED:
      console.log("User denied the request for Geolocation.");
      // Optionally, use a default location if permission is denied
      getWeatherData(40.7128, -74.0060).then(weatherData => {
            if (weatherData) {
                displayCurrentWeather(weatherData);
                displayForecast(weatherData);
            }
        });
      break;
    case error.POSITION_UNAVAILABLE:
      console.log("Location information is unavailable.");
      // Optionally, use a default location if location is unavailable
      getWeatherData(40.7128, -74.0060).then(weatherData => {
            if (weatherData) {
                displayCurrentWeather(weatherData);
                displayForecast(weatherData);
            }
        });
      break;
    case error.TIMEOUT:
      console.log("The request to get user location timed out.");
      // Optionally, use a default location if the request times out
      getWeatherData(40.7128, -74.0060).then(weatherData => {
            if (weatherData) {
                displayCurrentWeather(weatherData);
                displayForecast(weatherData);
            }
        });
      break;
    case error.UNKNOWN_ERROR:
      console.log("An unknown error occurred.");
      // Optionally, use a default location if an unknown error occurs
      getWeatherData(40.7128, -74.0060).then(weatherData => {
            if (weatherData) {
                displayCurrentWeather(weatherData);
                displayForecast(weatherData);
            }
        });
      break;
  }
}

async function getWeatherData(latitude, longitude) {
  const apiKey = "YOUR_API_KEY"; // Replace with your actual API key
  const apiUrl = `https://api.openweathermap.org/data/2.5/forecast?lat=${latitude}&lon=${longitude}&appid=${apiKey}`;

  try {
    const response = await fetch(apiUrl);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log("Weather Data:", data);
    return data; // Return the weather data
  } catch (error) {
    console.error("Error fetching weather data:", error);
    return null; // Or handle the error as needed
  }
}

function displayCurrentWeather(weatherData) {
    // Extract relevant information from the weather data
    const temperature = weatherData.list[0].main.temp;
    const humidity = weatherData.list[0].main.humidity;
    const windSpeed = weatherData.list[0].wind.speed;
    const description = weatherData.list[0].weather[0].description;
    const iconCode = weatherData.list[0].weather[0].icon;
    const iconUrl = `http://openweathermap.org/img/w/${iconCode}.png`;

    // Update the HTML elements
    document.getElementById('temperature').textContent = `Temperature: ${temperature}°C`;
    document.getElementById('humidity').textContent = `Humidity: ${humidity}%`;
    document.getElementById('wind-speed').textContent = `Wind Speed: ${windSpeed} m/s`;
    document.getElementById('description').textContent = `Description: ${description}`;
    document.getElementById('weather-icon').src = iconUrl;
    document.getElementById('weather-icon').alt = description;
}

function displayForecast(weatherData) {
    const forecastContainer = document.getElementById('forecast');
    forecastContainer.innerHTML = ''; // Clear previous forecast data

    // Loop through the forecast data (every 8 hours)
    for (let i = 0; i < weatherData.list.length; i += 8) {
        const forecast = weatherData.list[i];
        const temperature = forecast.main.temp;
        const description = forecast.weather[0].description;
        const iconCode = forecast.weather[0].icon;
        const iconUrl = `http://openweathermap.org/img/w/${iconCode}.png`;

        // Create forecast item elements
        const forecastItem = document.createElement('div');
        forecastItem.classList.add('forecast-item');

        const date = new Date(forecast.dt * 1000);
        const dayOfWeek = date.toLocaleDateString('en-US', { weekday: 'short' });
        const forecastDate = document.createElement('h3');
        forecastDate.textContent = dayOfWeek;
        forecastItem.appendChild(forecastDate);

        const icon = document.createElement('img');
        icon.src = iconUrl;
        icon.alt = description;
        forecastItem.appendChild(icon);

        const temp = document.createElement('p');
        temp.textContent = `Temperature: ${temperature}°C`;
        forecastItem.appendChild(temp);

        const desc = document.createElement('p');
        desc.textContent = `Description: ${description}`;
        forecastItem.appendChild(desc);

        forecastContainer.appendChild(forecastItem);
    }
}

// Call getLocation() on page load
window.onload = getLocation;

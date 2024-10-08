import {React, useState, useEffect} from 'react'
import weatherdata from '../weather_codes.json'
import {Link} from 'react-router-dom'

export default function Home() {
    const [currentZipCode, setZipCode] = useState(39406);
    const [currentdata, setdata] = useState({})
    const [error, setError] = useState('')
  
    // a webpack feature that allows to dynamically import modules or files based on certain context
    const images = require.context('../weather_img/', false);
    
    const weather_description = weatherdata?.[currentdata.weather_code]?.[currentdata.time_of_day]?.description
  
    function getImage(imageName){
      console.log(`searching for ${imageName}`);
      const output = images(`./${imageName}.png`); 
      console.log(`${output}`);
      return images(`./${imageName}.png`);
    }
  
    function backend_fetch(currentZipCode){
        fetch(`/home?zipcode=${currentZipCode}`)
        .then(res =>{
          if (!res.ok){
            return res.json().then(errorData=>{
              throw new Error(errorData.error) //Throwing error to be caught in the next catch action
            });
          }
          return res.json(); 
        })
        .then(data => {
          console.log("The data received is");
          console.log(data);
          setdata(data)
          setError('');
        })
        .catch(error=>{
          console.error("Error:", error.message);
          setError(error.message)
          // setdata({})
        })
    }
      
    // function image_location(image){
    //   const image_loc = `weather_img/${image}`;
    //   console.log(image_loc)
    //   return image_loc;
    // }
  
    // function convert_24hr(timestamp){
    //   console.log(`timestamp received is ${timestamp}`)
    //   const date = new Date(timestamp*1000);
    //   const hours = date.getHours();
    //   const minutes = date.getMinutes();
  
    //   const formattedHours = String(hours).padStart(2, '0');
    //   const formattedMinutes = String(minutes).padStart(2, '0');
  
    //   setTime(`${formattedHours}:${formattedMinutes}`)
    // }
  
    useEffect(()=>{
     backend_fetch(currentZipCode);
    }, [])  
  
    const handleInputChange = (event) => {
      console.log(event.target.value)
      setZipCode(event.target.value);
    };
   
    return (
        <div className="flex flex-col
        rounded-xl
        mx-auto mt-7 mb-7 w-96
        bg-orange-200 
        ring-4 ring-black ring-inset shadow-xl shadow-slate-400">
            <div className= "flex flex-row mt-6 mx-auto" id = "Input-container">
              <input type='text' placeholder='Zip Code'  onChange={handleInputChange}
              className = "bg-teal-50 p-1 rounded-md ring-1 ring-black" />
              <button type='submit' onClick={() => backend_fetch(currentZipCode)} 
              className = "inline items-center max-content bg-black text-white rounded-md p-1 ml-2 hover:text-black hover:bg-gray-600">
                            Search</button>
            </div>
            {error && <div className="flex rounded-md mx-3 my-3 px-2
                                    bg-red-50
                                    text-center text-red-600 text-xs">{error}</div>}
            {currentdata && (
              <>
                <div className="inline-flex items-center rounded-md top-9 mt-9
                                text-center text-green-50 font-semibold text-3xl
                                bg-orange-950 px-2 py-1 mx-auto
                                border-green-50 
                                ring-1 ring-inset ring-green-600/20">{currentdata.primary_city}</div>
                <p className = "mx-auto mt-3 text-2xl font-bold text-gray-700">{currentdata.state}</p>
                <p className="mx-auto py-2 px-2 rounded-md
                            text-gray-700 font-semibold text-7xl">{currentdata.current_temp}°</p>
                <p id="feels_like" className="mx-auto text-gray-950">feels like 
                  <span className="font-semibold text-2xl text-gray-600"> {currentdata.current_apparent_temp}</span> °F
                </p>
                <p className="mx-auto mt-3 text-2xl font-bold text-gray-700">{currentdata.time}</p>
                {currentdata.image && <img src = {getImage(currentdata.image)} className="mx-auto w-32 h-32"/>}
                <p className= "mx-auto mb-6 text-3xl text-gray-700 font-bold">{weather_description}</p>
            </>)
          }
          <div className='flex flex-row justify-between mx-4 mb-4'>
            <Link to = '/hourlyforecast' className='p-1 px-2
                                                  bg-orange-950 rounded-md text-white'>Hourly Forecast</Link>
            <Link to = '/dailyforecast' className='p-1 px-2
                                                  bg-orange-950 rounded-md text-white'>Weekly Forecast</Link>
          </div>
        </div>
      )
}


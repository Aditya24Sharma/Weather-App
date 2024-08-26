import { useEffect, useState } from "react";
import React from "react";
import {Link} from 'react-router-dom'
import weatherDetails from '../weather_codes.json'

function DailyForecast(){
    const [forecast, setForecast] = useState({})
    const [locationInfo, setLocationInfo] = useState({})
    // const [zipCode, setZipCode] = useState({39406})

    const images = require.context('../weather_img/', false)
    
    function getImage(image){
        return images(`./${image}.png`)
    }
    useEffect(()=>{
        backendFetch()
    },[])

    function backendFetch() {
        fetch('/dailyforecast')
        .then(res=>res.json())
        .then(data=>{setForecast(data['forecast']); setLocationInfo(data['location_info']); console.log(data['location_info'])})
        }

    return(
        <>
            <div className="text-center mt-16 -mb-4 text-6xl font-serif font-bold">{locationInfo['primary_city']}, <span className="font-sans font-semibold text-4xl">{locationInfo['state']}</span></div>
            <div className="flex flex-col">
                {/* <input type='text' placeholder="Zip Code" onChange={handleInputChange}/>  */}
                {/* <button type='submit' onClick={() => backendFetch()}>Search</button> */}
                <ul className="flex flex-row mx-auto mt-14">
                    {/* the forecast contains object so we need to convert them to array to be mapped */}
                    {/* Object.entries converts the objects to a 2-d array with [date,details] */}
                    {Object.entries(forecast).map(([date, details])=>
                    <li key={date} className="flex flex-col mx-2 items-center bg-orange-200 rounded-lg p-2 ring-2 ring-inset ring-black shadow-lg shadow-slate-400">
                        <p className="text-gray-700">{date}</p>
                        <p className="font-bold text-2xl text-gray-600">{details.day_of_week}</p>
                        {details.image && <img src = {getImage(details.image)} className="-mt-3"/>}
                        <p className="text-xs">{weatherDetails?.[details.weather_code]?.day?.description}</p>
                        <p className="text-m">{details.Max_Temp} --- {details.Min_Temp}</p>
                    </li>
                    )}
                </ul>
                <Link to = '/' className='block mx-auto mb-3 mt-12 p-2
                                                    bg-orange-950 rounded-md ring-2 ring-inset ring-black
                                                    text-white text-xl'>Weather Search</Link>
            </div>
        </>
    )
}

export default DailyForecast
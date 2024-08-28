import { useEffect, useState } from "react";
import React from "react";
import {Link} from 'react-router-dom'
// import weatherDetails from '../weather_codes.json'


function HourlyForecast() {

    const[currentforecast, setForecast] = useState({});
    const[locationInfo, setLocationInfo] = useState({});
    const[currentTimeHr, setcurrentTimeHr] = useState(0);

    const images = require.context('../weather_img', false)

    function getImage(image){
        console.log(image);
        return images(`./${image}.png`);
    }

    const backendfetch = () =>{
        fetch('/hourlyforecast')
        .then(rsp => rsp.json())
        .then(data => {setForecast(data['forecast']);
            setLocationInfo(data['location_info']);
            setcurrentTimeHr(data['locationTime_hr'])})
    }

    useEffect(()=>{
        backendfetch()
    }, [])

    return (
    <>
        <div className="flex justify-center">
            <ul className="flex flex-row flex-wrap space-x-2 mt-12">
                {Object.entries(currentforecast)
                // this sort function has a comparision function based on which the sorting is done.
                // In this case the elements are compared. Negative value means 'a' comes before 'b'
                // equal means same and +ve value means 'b' comes before 'a'. We can do similar to 
                // sort based on length of strings.     
                .sort((([a], [b])=> parseInt(a) - parseInt(b))) 
                .map(([time, details])=>{
                    const isPast = parseInt(time) < currentTimeHr;

                    return (
                        <li key = {time} className={`flex flex-col items-cente rounded-md w-12
                        ${isPast ? 'bg-gray-700': 'bg-orange-200'} `}>
                            <div className="my-2">
                                <p className="text-lg text-center text-gray-800">{details.time_in_12hour}<span className="text-xs ml-0.5 text-gray-700">{details.AM_PM}</span></p>
                                {/* console.log({'OUTPUT'})
                                console.log({details['weather_code']}) */}
                                <img src = {getImage(details.image)} alt={details.image} className="w-9 h-9"/>
                                <p className="text-center text-sm">{details.temperature}</p>
                            </div>
                        </li>)}
                )}
            </ul>
        </div>
    </>
  )
}

export default HourlyForecast

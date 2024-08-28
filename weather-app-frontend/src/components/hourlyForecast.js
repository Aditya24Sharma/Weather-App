import { useEffect, useState } from "react";
import React from "react";
import {Link} from 'react-router-dom'
// import weatherDetails from '../weather_codes.json'


function HourlyForecast() {

    const[currentforecast, setForecast] = useState({});
    const[locationInfo, setLocationInfo] = useState({});

    const images = require.context('../weather_img', false)

    function getImage(image){
        return images`./${image}.png`;
    }

    const backendfetch = () =>{
        fetch('/hourlyforecast')
        .then(rsp => rsp.json())
        .then(data => {setForecast(data['forecast']); setLocationInfo(data['location_info']); console.log(data)})
    }

    useEffect(()=>{
        backendfetch()
    }, [])

    return (
    <>
        <div>
            <ul className="flex flex-row flex-wrap space-x-4 m-4">
                {Object.entries(currentforecast)
                // this sort function has a comparision function based on which the sorting is done.
                // In this case the elements are compared. Negative value means 'a' comes before 'b'
                // equal means same and +ve value means 'b' comes before 'a'. We can do similar to 
                // sort based on length of strings.     
                .sort((([a], [b])=> parseInt(a) - parseInt(b))) 
                .map(([time, details])=>
                <li key = {time}>
                    <p className="text-xl">{time}</p>
                    {/* console.log({'OUTPUT'})
                    console.log({details['weather_code']}) */}
                    <img src = {getImage(details.image)} alt={details.image}/>
                    <p className="text-center">{details.temperature}</p>
                </li>
                )}
            </ul>
        </div>
    </>
  )
}

export default HourlyForecast

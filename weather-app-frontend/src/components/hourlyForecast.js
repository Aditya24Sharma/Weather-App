import { useEffect, useState } from "react";
import React from "react";
import {Link} from 'react-router-dom'
// import weatherDetails from '../weather_codes.json'


function HourlyForecast() {

    const[currentforecast, setForecast] = useState({});
    const[locationInfo, setLocationInfo] = useState({});
    const[currentTimeHr, setcurrentTimeHr] = useState(0);
    const[currentDate, setDate]=useState('');

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
            setcurrentTimeHr(data['locationTime_hr']);
            setDate(data['Date'])})
    }

    useEffect(()=>{
        backendfetch()
    }, [])

    return (
    <>
    
        <div className="text-center mt-16 text-6xl font-serif font-bold">{locationInfo['primary_city']}, <span className="font-sans font-semibold text-4xl">{locationInfo['state']}</span></div>
        <div className="text-center mt-4 -mb-4 text-4xl font-sans text-orange-600">{currentDate}</div>
        <div className="flex justify-center">
            <div className="flex flex-col"> 
                <ul className="flex flex-row flex-wrap space-x-2 mt-12">
                    {Object.entries(currentforecast)
                    // this sort function has a comparision function based on which the sorting is done.
                    // In this case the elements are compared. Negative value means 'a' comes before 'b'
                    // equal means same and +ve value means 'b' comes before 'a'. We can do similar to 
                    // sort based on length of strings.     
                    .sort((([a], [b])=> parseInt(a) - parseInt(b))) 
                    .map(([time, details])=>{
                        const isPast = parseInt(time) < currentTimeHr;
                        const isNow = parseInt (time) === currentTimeHr;

                        return (
                            <li key = {time} className={`flex flex-col items-cente rounded-md w-12 items-center shadow-md shadow-slate-600 ring-inset ring-1
                            ${isPast ? 'bg-gray-600 ring-white': 'bg-orange-200 ring-black' }`}>
                                <div className="my-2">
                                    <p className={`text-lg text-center ${isPast? 'text-white' : 'text-gray-800'}`}>
                                        {time == currentTimeHr ? ('Now'): (
                                            <>
                                                {details.time_in_12hour}
                                                <span className={`text-xs ml-0.5 ${isPast? 'text-gray-300' : 'text-gray-700'}`}>
                                                    {details.AM_PM}</span>
                                            </>
                                        )}
                                    </p>
                                    <img src = {getImage(details.image)} alt={details.image} className="w-9 h-9"/>
                                    <p className={`text-center text-sm ${isPast? 'text-white' : 'text-black'}`}>{details.temperature}°</p>
                                </div>
                            </li>)}
                    )}
                </ul>
            <Link to = '/' className='inline mx-auto mb-3 mt-12 p-2
                                                    bg-orange-950 rounded-md ring-2 ring-inset ring-black
                                                    text-white text-xl'>Weather Search</Link>
            </div>
        </div>
    </>
  )
}

export default HourlyForecast

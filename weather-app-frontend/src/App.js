import React, {useState, useEffect} from 'react'
import './index.css'

function App(){
  const [currentTemp, setTemp] = useState(0);
  const [currentTime, setTime] = useState('')
  const [currentZipCode, setZipCode] = useState(39406);
  const [currentdata, setdata] = useState({})

  const images = require.context('./weather_img/', false);

  function getImage(imageName){
    console.log(`searching for ${imageName}`);
    const output = images(`./${imageName}.png`); 
    console.log(`${output}`);
    return images(`./${imageName}.png`);
  }

  function backend_fetch(currentZipCode){
      fetch(`/home?zipcode=${currentZipCode}`)
      .then(res => res.json())
      // .then(data => {setTemp(data.current_temp); convert_24hr(data.time);});
      .then(data => {
        console.log("The data received is");
        console.log(data);
        setdata(data);
      })
  }
    
  function image_location(image){
    const image_loc = `weather_img/${image}`;
    console.log(image_loc)
    return image_loc;
  }

  function convert_24hr(timestamp){
    console.log(`timestamp received is ${timestamp}`)
    const date = new Date(timestamp*1000);
    const hours = date.getHours();
    const minutes = date.getMinutes();

    const formattedHours = String(hours).padStart(2, '0');
    const formattedMinutes = String(minutes).padStart(2, '0');

    setTime(`${formattedHours}:${formattedMinutes}`)
  }

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
    mx-auto mt-12 w-96
    ring-4 ring-gray-500 ring-inset shadow-xl">
      {/* <form onSubmit={() => backend_fetch(currentZipCode)}> */}
        <div className= "flex flex-row mt-6 mx-auto" id = "Input-container">
          <input type='text' placeholder='Zip Code'  onChange={handleInputChange}
          className = "bg-white p-1 rounded-md ring-1 ring-gray-400" />
          <button type='submit' onClick={() => backend_fetch(currentZipCode)} 
          className = "inline items-center max-content bg-blue-400 text-black rounded-md p-1 ml-2 hover:text-white hover:bg-blue-950">
                        Search</button>
        </div>
        {/* {currentZipCode} */}
        <div className="inline-flex items-center rounded-md top-9 mt-9
                        text-center text-green-900 font-semibold text-3xl
                        bg-green-50 px-2 py-1 mx-auto
                        border-green-900 
                        ring-1 ring-inset ring-green-600/20">{currentdata.primary_city}</div>
        <p className = "mx-auto mt-3 text-2xl font-bold text-gray-700">{currentdata.state}</p>
        <p className="mx-auto py-2 px-2 rounded-md
                    text-gray-700 font-semibold text-7xl">{currentdata.current_temp}</p>
        <p id="feels_like" className="mx-auto text-gray-400">feels like 
          <span className="font-semibold text-2xl text-gray-600"> {currentdata.current_apparent_temp}</span>
        </p>
        <p className="mx-auto mt-3 text-2xl font-bold text-gray-700">{currentdata.time}</p>
        {/* <img src = {image_location(currentdata.image)}/> */}
        {currentdata.image && <img src = {getImage(currentdata.image)} className="mx-auto w-32 h-32"/>}
      {/* </form> */}
    </div>
  )
}

export default App
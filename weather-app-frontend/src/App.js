import React, {useState, useEffect} from 'react'

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
    <div>
      {/* <form onSubmit={() => backend_fetch(currentZipCode)}> */}
        <input type='text' placeholder='Zip Code'  onChange={handleInputChange} />
        <button type='submit' onClick={() => backend_fetch(currentZipCode)}>Click me</button>
        {/* {currentZipCode} */}
        <p>Temperature in {currentdata.primary_city}</p>
        <p>State = {currentdata.state}</p>
        <p>The current Temp is {currentdata.current_temp}</p>
        <p>The current Time is {currentdata.time}</p>
        {/* <img src = {image_location(currentdata.image)}/> */}
        {currentdata.image && <img src = {getImage(currentdata.image)}/>}
      {/* </form> */}
    </div>
  )
}

export default App
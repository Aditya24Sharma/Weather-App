import React, {useState, useEffect} from 'react'

function App(){
  const [currentTemp, setTemp] = useState(0);
  const [currentTime, setTime] = useState('')
  const [currentZipCode, setZipCode] = useState(0);



  function backend_fetch(){
      fetch('/home')
      .then(res => res.json())
      .then(data => {setTemp(data.current_temp); convert_24hr(data.time);});
  }
    

  function convert_24hr(timestamp){
    const date = new Date(timestamp*1000);
    const hours = date.getHours();
    const minutes = date.getMinutes();

    const formattedHours = String(hours).padStart(2, '0');
    const formattedMinutes = String(minutes).padStart(2, '0');

    setTime(`${formattedHours}:${formattedMinutes}`)
  }

  useEffect(()=>{
   backend_fetch();
  }, [])

  const handleInputChange = (event) => {
    setZipCode(event.target.value);
  };


  return (
    <div>
      <input type='text' placeholder='hello'  onChange={handleInputChange} />
      <button type='submit' onClick={backend_fetch(currentZipCode)}>Click me</button>
      {currentZipCode}
      <p>The current Temp is {currentTemp}</p>
      <p>The current Time is {currentTime}</p>
    </div>
  )
}

export default App
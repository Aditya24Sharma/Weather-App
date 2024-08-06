import React, {useState, useEffect} from 'react'




function App() {

  const [currentTemp, setTemp] = useState(0);
  const [currentTime, setTime] = useState('')

  function convert_24hr(timestamp){
    const date = new Date(timestamp*1000);
    const hours = date.getHours();
    const minutes = date.getMinutes();

    const formattedHours = String(hours).padStart(2, '0');
    const formattedMinutes = String(minutes).padStart(2, '0');

    setTime(`${formattedHours}:${formattedMinutes}`)
  }

  useEffect(()=>{
    fetch('/home')
    .then(res => res.json())
    .then(data => {setTemp(data.current_temp); convert_24hr(data.time);});
  }, [])
  return (
    <div>
      <p>The current Temp is {currentTemp}</p>
      <p>The current Time is {currentTime}</p>
    </div>
  )
}

export default App
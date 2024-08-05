import React, {useState, useEffect} from 'react'




function App() {

  const [currentTemp, setTemp] = useState(0);

  useEffect(()=>{
    fetch('/home')
    .then(res => res.json())
    .then(data => {setTemp(data.current_temp);});
  }, [])
  return (
    <div>
      <p>The current Temp is {currentTemp}</p>
    </div>
  )
}

export default App
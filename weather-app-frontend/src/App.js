import React from 'react'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import './index.css'
import Home from './components/Home.js'
import DailyForecast from './components/dailyForecast.js';

function App(){
  return(
    <>
      <Router>
        <Routes>
          <Route path='/' element={<Home/>}/>
          <Route path='/dailyforecast' element={<DailyForecast/>}/>
        </Routes>
      </Router>
    </>
  )
}

export default App
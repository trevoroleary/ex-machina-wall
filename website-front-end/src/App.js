import './App.css';
import React, { useState, Fragment }  from 'react';
import Slider from '@mui/material/Slider'
import { TextField } from '@mui/material';
import { ThemeProvider } from '@mui/material/styles';

import darkTheme from './darkTheme';
import lightTheme from './lightTheme';
import Wheel from '@uiw/react-color-wheel';

import { send_post } from './endpoints';

function App() {
  const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const theme = prefersDarkMode ? darkTheme : lightTheme;

  const [primaryHSVA, setPrimaryHSVA] = useState({ h: 214, s: 43, v: 90, a: 1 });
  const [secondaryHSVA, setSecondaryHSVA] = useState({ h: 214, s: 43, v: 90, a: 1 });
  const [timeOfLastSend, setTimeOfLastSend] = useState(Date.now());

  const handlePrimaryColorChange = (color) => {
    setPrimaryHSVA({ ...primaryHSVA, ...color.hsva })
    setTimeOfLastSend(send_post(`SET_PRIMARY_COLOR-${color.rgb.r}-${color.rgb.g}-${color.rgb.b}`, timeOfLastSend))
  }

  const handlePrimaryBrightnessChange = (event) => {
    setTimeOfLastSend(send_post(`SET_PRIMARY_BRIGHTNESS-${event.target.value}`, timeOfLastSend))
  }
  
  const handleSecondaryColorChange = (color) => {
    setSecondaryHSVA({ ...secondaryHSVA, ...color.hsva })
    setTimeOfLastSend(send_post(`SET_SECONDARY_COLOR-${color.rgb.r}-${color.rgb.g}-${color.rgb.b}`, timeOfLastSend))
  }

  const handleSecondaryBrightnessChange = (event) => {
    setTimeOfLastSend(send_post(`SET_SECONDARY_BRIGHTNESS-${event.target.value}`, timeOfLastSend))
  }

  const handleImageBrightnessChange = (event) => {
    setTimeOfLastSend(send_post(`SET_IMAGE_BRIGHTNESS-${event.target.value}`, timeOfLastSend))
  }

  const handleArduinoPGainChanged = (event) => {
    setTimeOfLastSend(send_post(`SET_ARDUINO_PGAIN-${event.target.value}`, timeOfLastSend))
  }

  const handleFrameTimeChanged = (event) => {
    setTimeOfLastSend(send_post(`SET_FRAME_TIME-${event.target.value}`, timeOfLastSend))
  }

  const handleImageLinkChanged = (event) => {
    if (event.key === "Enter") {
      setTimeOfLastSend(send_post(`SET_IMAGE_URL-${event.target.value}`, timeOfLastSend))
    }
  }

  return (
    // 
    <ThemeProvider theme={theme}>
      <main className="flex min-h-screen flex-col items-center justify-between p-10 font-mono">
        <div className="z-10 max-w-5xl w-full">
          <p>
            Ex Controller
          </p>
        </div>
        
        <div>
        <p className='pb-3'>Primary Color</p>
          <div className="flex flex-row">
            <div className="flex-1">
            <Fragment>
              <Wheel color={primaryHSVA} onChange={handlePrimaryColorChange}/>
            </Fragment>
            </div>
            <div className="flex-1">
            <Slider
              defaultValue={100} step={1} min={0} max={100} valueLabelDisplay='auto' orientation="vertical"
              onChange={handlePrimaryBrightnessChange}
            ></Slider>
            </div>
          </div>
        </div>
        
        <div>
        <p className='pb-3'>Secondary Color</p>
          <div className="flex flex-row">
            <div className="flex-1">
              <Fragment>
                <Wheel color={secondaryHSVA} onChange={handleSecondaryColorChange}/>
              </Fragment>
            </div>
            <div className="flex-1">
            <Slider 
              defaultValue={100} step={1} min={0} max={100} valueLabelDisplay='auto' orientation="vertical"
              onChange={handleSecondaryBrightnessChange}
            ></Slider>
            </div>
          </div>
        </div>

        <div>
          <p className='pb-3'>Image/Animation</p>
          <div className="flex flex-row">
            <div className="flex-1">
              <TextField 
                id="outlined-basic" label="GIF/Image Link" variant="outlined" onKeyDown={handleImageLinkChanged}
              />
              <p className='pt-3'>GIF Frame Time</p>
              <Slider
                defaultValue={0.1} step={0.01} min={0.01} max={0.5} valueLabelDisplay='auto'
                onChange={handleFrameTimeChanged}
              ></Slider>
              <p>Arduino P Gain</p>
              <Slider
                defaultValue={20} step={1} min={1} max={100} valueLabelDisplay='auto'
                onChange={handleArduinoPGainChanged}
              ></Slider>
            </div>
            <div>
              <Slider 
                defaultValue={100} step={1} min={0} max={100} valueLabelDisplay='auto' orientation="vertical"
                onChange={handleImageBrightnessChange}
              ></Slider>
            </div>
          </div>
        </div>
        <div className='z-10 max-w-5xl w-full text-right'>
          <p>Trevor O'Leary</p>
        </div>
      </main>
    </ThemeProvider>
  );
}

export default App;

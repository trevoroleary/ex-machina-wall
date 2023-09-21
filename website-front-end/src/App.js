import './App.css';
import React, { useState, Fragment }  from 'react';
import Slider from '@mui/material/Slider'
import { TextField } from '@mui/material';
import { ThemeProvider } from '@mui/material/styles';
import { Button } from '@mui/material';


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
  
  const handleSecondaryColorChange = (color) => {
    setSecondaryHSVA({ ...secondaryHSVA, ...color.hsva })
    setTimeOfLastSend(send_post(`SET_SECONDARY_COLOR-${color.rgb.r}-${color.rgb.g}-${color.rgb.b}`, timeOfLastSend))
  }

  const handleButtonPressed = (event) => {
    setTimeOfLastSend(send_post(event.target.id, timeOfLastSend))
  }

  const handleSliderChange = (event) => {
    setTimeOfLastSend(send_post(`${event.target.name}-${event.target.value}`, timeOfLastSend))
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
        
        <div className='max-w-sm w-full'>
          <p className='pb-3 pt-4'>React Color</p>
          <div className="flex flex-row w-min mx-auto">
            <div className="flex-1">
              <Fragment>
                <Wheel color={secondaryHSVA} onChange={handleSecondaryColorChange}/>
              </Fragment>
            </div>
            <div>
            <Slider 
              defaultValue={100} step={1} min={0} max={100} valueLabelDisplay='auto' orientation="vertical"
              name="SET_SECONDARY_BRIGHTNESS"
              onChange={handleSliderChange}
            ></Slider>
            </div>
          </div>
        </div>

        <div className='max-w-sm w-full'>
          <p className='pb-3'>Backround Color</p>
          <div className="flex flex-row mx-auto w-min">
            <div className="flex-1">
            <Fragment>
              <Wheel color={primaryHSVA} onChange={handlePrimaryColorChange}/>
            </Fragment>
            </div>
            <div>
            <Slider
              defaultValue={100} step={1} min={0} max={100} valueLabelDisplay='auto' orientation="vertical"
              name="SET_PRIMARY_BRIGHTNESS"
              onChange={handleSliderChange}
            ></Slider>
            </div>
          </div>
        </div>

        <div className='max-w-sm w-full'>
          <p className='pb-1 pt-4'>Audio React Settings</p>
          <div className='flex flex-row w-full mx-auto'>
            <div className="flex flex-col">
              <div className='flex flex-row'>
                <Button onClick={handleButtonPressed} id="SET_HIGH_FREQUENCY_REACT_STATE-ON">High_Freq_On</Button>
                <Button onClick={handleButtonPressed} id="SET_HIGH_FREQUENCY_REACT_STATE-OFF">High_Freq_Off</Button>
              </div>
              
              <div className='flex flex-col'>
                <p className='pr-5'>Threshold</p>
                <Slider 
                defaultValue={170000} step={1000} min={10000} max={250000} valueLabelDisplay='auto'
                name="SET_HIGH_FREQUENCY_THRESHOLD"
                onChange={handleSliderChange}
                ></Slider>
              </div>

              <div className='flex flex-row flex-1'>
                <Button onClick={handleButtonPressed} id="SET_LOW_FREQUENCY_REACT_STATE-ON">LOW_Freq_On</Button>
                <Button onClick={handleButtonPressed} id="SET_LOW_FREQUENCY_REACT_STATE-OFF">LOW_Freq_Off</Button>
              </div>

              <div className='flex flex-col'>
                <p>Threshold</p>
                <Slider 
                defaultValue={300000} step={1000} min={30000} max={500000} valueLabelDisplay='auto'
                name="SET_LOW_FREQUENCY_THRESHOLD"
                onChange={handleSliderChange}
                ></Slider>
              </div>

            </div>
          </div>
          
        </div>

        <div className='max-w-sm w-full'>
          <p className='pb-3 pt-4'>Image/Animation</p>
          <div className="flex flex-row">
            <div className="flex-1">
              <TextField 
                id="outlined-basic" label="GIF/Image Link" variant="outlined" onKeyDown={handleImageLinkChanged}
                fullWidth
              />
              <p className='pt-3'>GIF Frame Time</p>
              <Slider
                defaultValue={0.1} step={0.01} min={0.01} max={0.5} valueLabelDisplay='auto'
                name="SET_FRAME_TIME"
                onChange={handleSliderChange}
              ></Slider>
              <p>Arduino P Gain</p>
              <Slider
                defaultValue={20} step={1} min={1} max={100} valueLabelDisplay='auto'
                name="SET_ARDUINO_PGAIN"
                onChange={handleSliderChange}
              ></Slider>
            </div>
            <div>
              <Slider 
                defaultValue={100} step={1} min={0} max={100} valueLabelDisplay='auto' orientation="vertical"
                name="SET_IMAGE_BRIGHTNESS"
                onChange={handleSliderChange}
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

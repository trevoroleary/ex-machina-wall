import React from 'react';
import Wheel from '@uiw/react-color-wheel';
import { useState, Fragment } from 'react';

function ColorPick() {
  const [hsva, setHsva] = useState({ h: 214, s: 43, v: 90, a: 1 });
  const [timeOfLastSend, setTimeOfLastSend] = useState(Date.now()); 

  const onChange = (color) => {
      setHsva({ ...hsva, ...color.hsva })
      if (Date.now() - timeOfLastSend > 100){
        console.log(Date.now() - timeOfLastSend)
        setTimeOfLastSend(Date.now())
        fetch('https://ntfy.trevoroleary.com/x',{
          method: "POST",
          body: `SET_PRIMARY-${color.rgb.r}-${color.rgb.g}-${color.rgb.b}`,
        //   contentType: 'application/json',
          headers: {
            "Authorization": "Bearer tk_632ejha524dlfcgx7dnqnxb5in4sx"
          }
        })
        // .then(response => response.json())
        // .then(data => {
        //   console.log(data); // Handle the response data here
        // })
        .catch(error => {
          console.error('Error:', error);
        });
      }
  }
  return (
      <Fragment>
        <Wheel color={hsva} onChange={onChange} />
        {/* <div style={{ width: '100%', height: 34, background: hsvaToHex(hsva) }}></div> */}
      </Fragment>
  )
}

export default ColorPick
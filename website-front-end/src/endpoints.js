// math.js
export function send_post(body, timeOfLastSend) {
    if (Date.now() - timeOfLastSend > 100){
        fetch('https://expost.trevoroleary.com',{
        method: "POST",
        body: body,
        });
        return Date.now()
    }
    return timeOfLastSend
  }
  
  export function subtract(a, b) {
    return a - b;
  }
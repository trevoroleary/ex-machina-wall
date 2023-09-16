// math.js
export function send_post(body, timeOfLastSend) {
    if (Date.now() - timeOfLastSend > 100){
        fetch('https://ex.trevoroleary.com/sendpost',{
          method: "POST",
          body: body,
        })
        .then(response => response.json())
        .then(data => {
          console.log(data); // Handle the response data here
        })
        .catch(error => {
            console.error('Error:', error);
        });
        return Date.now()
    }
    return timeOfLastSend
  }
  
  export function subtract(a, b) {
    return a - b;
  }
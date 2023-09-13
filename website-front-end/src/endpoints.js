// math.js
export function send_post(body, timeOfLastSend) {
    console.log(process.env.NTFY_TOKEN);
    if (Date.now() - timeOfLastSend > 100){
        fetch('https://ntfy.trevoroleary.com/x',{
        method: "POST",
        body: body,
        headers: {
          "Authorization": `Bearer ${process.env.NTFY_TOKEN}`
        }
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
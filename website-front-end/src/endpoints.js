// math.js
export function send_post(body, timeOfLastSend) {
    if (Date.now() - timeOfLastSend > 100){
        fetch('https://ntfy.trevoroleary.com/x',{
        method: "POST",
        body: body,
        headers: {
          "Authorization": `Bearer tk_632ejha524dlfcgx7dnqnxb5in4sx`
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
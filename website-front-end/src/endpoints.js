// math.js
export function send_post(body, timeOfLastSend) {
  if (Date.now() - timeOfLastSend > 100){
      // fetch('https://ex.trevoroleary.com/sendpost',{
      //   method: "POST",
      //   body: body,
      // })
      fetch('https://ntfy.trevoroleary.com/x',{
        method: "POST",
        body: body,
        headers: {
            "Authorization": `Bearer tk_632ejha524dlfcgx7dnqnxb5in4sx`
        }
      })
      return Date.now()
  }
  return timeOfLastSend
}

// math.js
export function send_post(body, timeOfLastSend) {
  if (Date.now() - timeOfLastSend > 100){
      fetch('https://ex.trevoroleary.com/sendpost',{
        method: "POST",
        body: body,
      })
      return Date.now()
  }
  return timeOfLastSend
}

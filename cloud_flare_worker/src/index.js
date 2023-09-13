/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run `npm run dev` in your terminal to start a development server
 * - Open a browser tab at http://localhost:8787/ to see your worker in action
 * - Run `npm run deploy` to publish your worker
 *
 * Learn more at https://developers.cloudflare.com/workers/
 */

export default {
	async fetch(request, env, ctx) {
		if (Date.now() - timeOfLastSend > 100){
			fetch('https://ntfy.trevoroleary.com/x',{
			method: "POST",
			body: body,
			headers: {
			"Authorization": `Bearer tk_632ejha524dlfcgx7dnqnxb5in4sx`
			}
			})
			// .then(response => response.json())
			// .then(data => {
			//   console.log(data); // Handle the response data here
			// })
			.catch(error => {
				console.error('Error:', error);
			});
			return Date.now()
		}
		return timeOfLastSend

		return new Response('Hello World!');
	},
};

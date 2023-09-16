/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run `npm run dev` in your terminal to start a development server
 * - Open a browser tab at http://localhost:8787/ to see your worker in action
 * - Run `npm run deploy` to publish your worker
 *
 * Learn more at https://developers.cloudflare.com/workers/
 */

export function onRequest(context) {
    fetch('https://ntfy.trevoroleary.com/x',{
        method: "POST",
        body: context.request.body,
        headers: {
            "Authorization": `Bearer ${context.env.NTFY_TOKEN}`
        }
    })
    var keys = Object.keys(context);
    console.log(keys) // ['alpha', 'beta'] 
    var keys = Object.keys(context.request);
    console.log(keys) // ['alpha', 'beta'] 
    var keys = Object.keys(context.functionPath);
    console.log(keys) // ['alpha', 'beta'] 
    var keys = Object.keys(context.next);
    console.log(keys) // ['alpha', 'beta'] 
    var keys = Object.keys(context.params);
    console.log(keys) // ['alpha', 'beta'] 
    var keys = Object.keys(context.data);
    console.log(keys) // ['alpha', 'beta'] 
    var keys = Object.keys(context.env);
    console.log(keys) // ['alpha', 'beta'] 
    var keys = Object.keys(context.waitUntil);
    console.log(keys) // ['alpha', 'beta'] 
    var keys = Object.keys(context.passThroughOnException);
    console.log(keys) // ['alpha', 'beta'] 

    return new Response("HELLO!")
};

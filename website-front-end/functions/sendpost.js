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
    if (context.request.headers.get("origin") === "https://ex.trevoroleary.com")
        fetch('https://ntfy.trevoroleary.com/x',{
            method: "POST",
            body: context.request.body,
            headers: {
                "Authorization": `Bearer ${context.env.NTFY_TOKEN}`
            }
        })
    else {
        throw new UnauthorizedException("Forbidden (403)");
    }
    return new Response();
};

// Follow this setup guide to integrate the Deno language server with your editor:
// https://deno.land/manual/getting_started/setup_your_environment
// This enables autocomplete, go to definition, etc.

import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const supabase = createClient('https://bttqjbjajfomldjfwcxq.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ0dHFqYmphamZvbWxkamZ3Y3hxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY3MjI5NjMxMiwiZXhwIjoxOTg3ODcyMzEyfQ._9OAY37rFqJb6S8jnveCR1-ZdTeYhd-quXeBpvs3AkY')

const sha256 = async (message: string): Promise<T> => {
        // encode as UTF-8
        const msgBuffer = new TextEncoder().encode(message);                    
    
        // hash the message
        const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
    
        // convert ArrayBuffer to Array
        const hashArray = Array.from(new Uint8Array(hashBuffer));
    
        // convert bytes to hex string                  
        const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
        return hashHex;
}

const JOB_BOARD_CHANNELS = [
    '929538334550806538'
]

serve(async (req) => {
    const data = await req.json()
    const observed_channel_id = data.record.channel_id
    let status = 400
    if (JOB_BOARD_CHANNELS.includes(observed_channel_id)) {
        
        const post_urls_id = data.record.id
        const post_id = data.record.post_id
        const author_sha256 = await sha256(data.record.author_id)
        const channel_sha256 = await sha256(data.record.channel_id)
        const guild_sha256 = await sha256(data.record.guild_id)
        const content_sha256 = await sha256(data.record.content)
        const created_at = data.record.created_at
        const url = data.record.url
        const title = data.record.title
        const description = data.record.description

        const { response, error } = await supabase
            .from('job_urls')
            .insert([
                { post_id,post_urls_id,author_sha256,channel_sha256,guild_sha256,content_sha256,created_at,url,title,description },
        ])
        if(!error) {
            status = 200
        }
    }
    else {
        status = 401
    }
   
    return new Response(
        JSON.stringify(status),
            { headers: { "Content-Type": "application/json" } },
        )
})
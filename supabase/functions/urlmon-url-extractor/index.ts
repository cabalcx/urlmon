// Follow this setup guide to integrate the Deno language server with your editor:
// https://deno.land/manual/getting_started/setup_your_environment
// This enables autocomplete, go to definition, etc.

import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const supabase = createClient('https://bttqjbjajfomldjfwcxq.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ0dHFqYmphamZvbWxkamZ3Y3hxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY3MjI5NjMxMiwiZXhwIjoxOTg3ODcyMzEyfQ._9OAY37rFqJb6S8jnveCR1-ZdTeYhd-quXeBpvs3AkY')


const get_preview = async (url: string): Promise<T> => {
    try {
        const response = await fetch('https://api.linkpreview.net',{
            method: 'POST',
            headers: {
                'content-type': 'application/x-www-form-urlencoded'
            },
            body: `key=b94a6802883768742457381f05d751e4&q=${url}`
        })
        return response.json()
    } catch {
        return {
            title: null,
            description: null
        }
    }
    
}

serve(async (req) => {
    const data = await req.json()
    const post_id = data.record.id
    const author_id = data.record.author_id
    const channel_id = data.record.channel_id
    const guild_id = data.record.guild_id
    const content = data.record.content
    const created_at = data.record.created_at

    const matches = content.match(/\bhttps?:\/\/\S+/gi);
    var status = 200
    await matches.forEach(async url => {        
        const preview = await get_preview(url)
        const title = preview.title
        const description = preview.description
        try {
            const { response, error } = await supabase
                .from('post_urls')
                .insert([
                    { post_id,author_id,channel_id,guild_id,content,created_at,url,title,description },
            ])
        } catch(e) {
            status = 500
        }
        
    });

   
    return new Response(
        JSON.stringify(status),
            { headers: { "Content-Type": "application/json" } },
        )
})
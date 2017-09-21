<template>
    <div id="pdf_canvas">        
    </div>
</template>

<script>
    import axios from 'axios'
    import {root_url} from '@/common/index.js'

    import PDFObject from 'pdfobject'


    export default {
        mounted(){
            PDFObject.embed(root_url + "media/pdf/song_" + this.$route.params.item_id + ".pdf", "#pdf_canvas")
        }
        
    }
</script>
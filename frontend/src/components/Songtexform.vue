<template>
    <div>
        <h1>{{ title }}</h1>
        <form id="songtexform" class="ui form">
            <fieldset>
                <legend>Tex form for song</legend>
                <p class="field">
                    <label for="content">Content:</label>
                    <textarea name="content" v-model="code"></textarea>
                </p>
                <p class="field"><button @click.prevent="save()" class="ui button">Save</button><button @click.prevent="cancel()" class="ui button">Cancel</button></p>
            </fieldset>
        </form>
    </div>
</template>

<script>
    import axios from 'axios'
    import {root_url} from '@/common/index.js'

    export default {
        data() {
            return {
                code: "",
                title: ""
            }
        },
        props:{
            force_conversion: false,
        },
        mounted() {
            if( this.$route.params.item_id ){
                let url = root_url + "song/edit/tex/" + this.$route.params.item_id + "/"
                if( this.force_conversion ) {
                    url = root_url + "song/convert/to/tex/" + this.$route.params.item_id + "/"
                }
                axios.get(url)
                    .then(response => {
                        this.$data.code = response.data.code
                        this.$data.title = response.data.title
                    },  (error) => { console.log(error) })
            }
        },
        methods: {
            save() {
                let data_code = {
                    code: this.$data.code
                }
                axios.put(root_url + "song/edit/tex/" + this.$route.params.item_id + "/", data_code)
                    .then(response => {
                        this.$data.code = response.data.code
                    },  (error) => { console.log(error) })
                this.$router.push({name:'song_detail', params:{item_id:this.$route.params.item_id}})
            },
            cancel() {
                this.$router.push({name:'song_detail', params:{item_id:this.$route.params.item_id}})
            }
        }
    }
</script>
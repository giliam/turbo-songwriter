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
            </fieldset>
        </form>
    </div>
</template>

<script>
    import axios from 'axios'

    export default {
        data() {
            return {
                code: "",
                title: ""
            }
        },
        props: {
            song: Number,
            force_conversion: Boolean
        },
        mounted() {
            if( this.song ){
                if( this.force_conversion ) {
                    axios.get("http://localhost:8000/song/convert/to/tex/" + this.song)
                        .then(response => {
                            this.$data.code = response.data.code;
                            this.$data.title = response.data.title;
                        },  (error) => { console.log(error) });
                } else {
                    axios.get("http://localhost:8000/song/edit/tex/" + this.song)
                        .then(response => {
                            this.$data.code = response.data.code;
                            this.$data.title = response.data.title;
                        },  (error) => { console.log(error) });
                }
            }
        }
    }
</script>
<template>
    <div>
        <h1>{{ title }}</h1>
        <form id="songtexform" class="ui form">
            <fieldset>
                <legend>Tex form for song</legend>
                <p class="field">
                    <label for="content">Content:</label>
                    <textarea name="content" v-model="tex"></textarea>
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
                tex: "",
                title: ""
            }
        },
        props: {
            song: Number
        },
        mounted() {
            if( this.song ){
                axios.get("http://localhost:8000/songs/convert/to/tex/" + this.song)
                    .then(response => {
                        this.$data.tex = response.data.tex;
                        this.$data.title = response.data.title;
                    },  (error) => { console.log(error) });
            }
        }
    }
</script>
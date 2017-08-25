<template>
    <div>
        <p>
            <div v-if="!is_editing">
                <span @click="launchEdition()">{{ verse.content }}</span>
                - <a @click.prevent="launchEdition()">Edit verse</a>
            </div>
            <div v-if="is_editing">
                <input type="text" v-model="verse.content" v-if="is_editing" @keyup.enter="saveEdition()"/>
                <button v-if="is_editing" @click.prevent="saveEdition()">Save</button>
            </div>
        </p>
    </div>
</template>

<script>
    import axios from 'axios'

    export default {
        data () {
            return {
                is_editing: false
            }
        },
        props: {
            verse: Object
        },
        methods: {
            launchEdition() {
                this.$data.is_editing = true
            },
            saveEdition() {
                axios.put("http://localhost:8000/verses/" + this.verse.id + "/", this.verse)
                    .then(response2 => { console.log(response2.data)
                    }, 	(error2) => { console.log(error2) });
                this.$data.is_editing = false
            }
        }
    }
</script>
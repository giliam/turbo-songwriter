<template>
    <div>
        <p>
            <div v-if="!is_editing">
                <span @click="launchEdition()">
                    <b v-if="is_refrain">
                        {{ verse.content }}
                    </b>
                    <span v-else>
                        {{ verse.content }}
                    </span>
                </span>
                - <a @click.prevent="launchEdition()">Edit verse</a>
            </div>
            <div v-if="is_editing">
                <form class="ui form">
                    <fieldset>
                        <p class="field">
                            <input type="text" name="verse" v-model="verse.content" @keyup.enter="saveEdition()"/>
                        </p>
                        <p>
                            <button @click.prevent="saveEdition()" class="ui button">Save</button>
                            <button @click.prevent="cancelEdition()" class="ui button">Cancel</button>
                        </p>
                    </fieldset>
                </form>
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
            verse: Object,
            is_refrain: Boolean
        },
        methods: {
            launchEdition() {
                this.$data.is_editing = true
            },
            cancelEdition() {
                this.$data.is_editing = false
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
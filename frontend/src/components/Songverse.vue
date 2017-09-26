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
                - <i class="icon edit" @click.prevent="launchEdition()"></i><slot></slot>
            </div>
            <div v-if="is_editing">
                <form class="ui form">
                    <fieldset>
                        <p class="field">
                            <input type="text" name="verse" v-model="verse.content" @keyup.enter="saveEdition()" v-focus/>
                        </p>
                        <p>
                            <button @click.prevent="saveEdition()" class="ui button primary">{{ t('Save') }}</button>
                            <button @click.prevent="cancelEdition()" class="ui button">{{ t('Cancel') }}</button>
                        </p>
                    </fieldset>
                </form>
            </div>
        </p>
    </div>
</template>

<script>
    import axios from 'axios'
    import {root_url} from '@/common/index.js'

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
                axios.put(root_url + "verses/" + this.verse.id + "/", this.verse)
                    .then(response2 => { console.log(response2.data)
                    }, 	(error2) => { console.log(error2) });
                this.$data.is_editing = false
            }
        }
    }
</script>
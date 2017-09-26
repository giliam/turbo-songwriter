<template>
    <div>
        <div id="listchords">
            <div v-if="!is_updating">
                <template v-if="is_editing">
                    <form class="ui form">
                        <fieldset>
                            <legend>{{ t('Edit an chord') }}</legend>
                            <p class="field">
                                <label for="note">{{ t('Note:') }} </label>
                                <input type="text" name="note" v-model="note" v-focus>
                            </p>
                            <p class="field">
                                <button class="ui button primary" @click.prevent="saveChord(true)">{{ t('Save') }}</button>
                                <button class="ui button" @click.prevent="hideChordForm()">{{ t('Cancel') }}</button>
                            </p>
                        </fieldset>
                    </form>
                </template>
                <template v-else>
                    <h2>{{ t('List of chords') }}</h2>
                    <button @click="synchronize()" class="ui button primary">{{ t('Update the list') }}</button>
                    <div class="ui list large">
                        <div v-for="item in chords" class="item" @click="editChord(item)">
                            <i class="icon music"></i>
                            {{ item.note }}
                        </div>
                    </div>
                </template>
                <div>
                    <p><a class="ui button green" @click.prevent="addChord()">{{ t('Add an chord') }}</a></p>
                    <form v-if="is_adding" class="ui form">
                        <fieldset>
                            <legend>{{ t('Add an chord') }}</legend>
                            <p class="field">
                                <label for="note">{{ t('Note:') }} </label>
                                <input type="text" name="note" v-model="note" v-focus>
                            </p>
                            <p class="field">
                                <button class="ui button primary" @click.prevent="saveChord(false)">{{ t('Save') }}</button>
                                <button class="ui button" @click.prevent="hideChordForm()">{{ t('Cancel') }}</button>
                            </p>
                        </fieldset>
                    </form>
                </div>
            </div>
            <div v-else>
                Updating...
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    import {root_url} from '@/common/index.js'

    export default {
        data() {
            return {
                chords: Array,
                chord_id: -1,
                is_adding: false,
                is_updating: false,
                is_editing: false,
                note: "",
            }
        },
        components: {
        },
        created() {
            axios.get(root_url + "chords/list/")
                .then(response => {
                    this.$data.chords = response.data;
                },  (error) => { console.log(error) });
        },
        methods:{
            // TODO: Use VueX to prevent passing this signal all the way up
            launch_show_chord(item_id) {
                this.$emit("show_chord", item_id)
            },
            launch_edit_chord(item_id) {
                this.$emit("edit_chord", item_id)
            },
            addChord() {
                this.$data.is_adding = !this.$data.is_adding
                this.$data.is_editing = false
                this.$data.note = ""
            },
            hideChordForm() {
                axios.get(root_url + "chords/list/")
                    .then(response => {
                        this.$data.chords = response.data;
                    },  (error) => { console.log(error) });
                this.$data.is_adding = false
                this.$data.is_editing = false
            },
            synchronize(){
                this.$data.is_updating = true
                axios.get(root_url + "chords/list/")
                    .then(response => {
                        this.$data.chords = response.data;
                        this.$data.is_updating = false
                    },  (error) => { console.log(error) });
            },
            saveChord(is_editing) {
                let chord = {
                    note: this.$data.note,
                };
                this.$data.is_updating = true
                if( is_editing ) {
                    axios.put(root_url + "chords/" + this.$data.chord_id + "/", chord)
                        .then(response => {
                            axios.get(root_url + "chords/list/")
                                .then(response => {
                                    this.$data.chords = response.data;
                                    this.$data.is_updating = false
                                },  (error) => { console.log(error) });
                        }, (error) => { console.log(error)});
                } else {
                    axios.post(root_url + "chords/list/", chord)
                        .then(response => {
                            axios.get(root_url + "chords/list/")
                                .then(response => {
                                    this.$data.chords = response.data;
                                    this.$data.is_updating = false
                                },  (error) => { console.log(error) });
                        }, (error) => { console.log(error)});
                }
                this.$data.is_adding = false
                this.$data.is_editing = false
                this.$data.chord_id = -1
            },
            editChord(chord){
                this.$data.note = chord.note
                this.$data.chord_id = chord.id
                this.$data.is_editing = true
                this.$data.is_adding = false
            }
        }
    }
</script>
<template>
    <div>
        <div id="listchords">
            <h2>List of chords</h2>
            <p @click="synchronize()">Update the list</p>
            <div v-if="!is_updating">
                <form v-if="is_editing" class="ui form">
                    <fieldset>
                        <legend>Edit an chord</legend>
                        <p class="field">
                            <label for="note">Name: </label>
                            <input type="text" name="note" v-model="note">
                        </p>
                        <p class="field">
                            <button class="ui button primary" @click.prevent="saveChord(true)">Save</button>
                            <button class="ui button" @click.prevent="hideChordForm()">Cancel</button>
                        </p>
                    </fieldset>
                </form>
                <ul v-if="!is_editing">
                    <li v-for="item in chords">
                        <p @click="editChord(item)">{{ item.note }}</p>
                    </li>
                </ul>
                <div>
                    <p><a @click.prevent="addChord()">Add an chord</a></p>
                    <form v-if="is_adding" class="ui form">
                        <fieldset>
                            <legend>Add an chord</legend>
                            <p class="field">
                                <label for="note">Name: </label>
                                <input type="text" name="note" v-model="note">
                            </p>
                            <p class="field">
                                <button class="ui button primary" @click.prevent="saveChord(false)">Save</button>
                                <button class="ui button" @click.prevent="hideChordForm()">Cancel</button>
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
            }
        }
    }
</script>
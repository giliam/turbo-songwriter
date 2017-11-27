<template>
        <div>
            <div id="listsongs">
                <h2>{{ t('List of elements') }}</h2>
                <div class="ui list aligned large">
                    <p><button class="ui button primary" @click="sync()">{{ t('Refresh') }}</button></p>
                    <p><button class="ui button primary" @click="save()">{{ t('Save changes') }}</button></p>
                    <table class="ui celled table">
                        <thead>
                            <tr>
                                <th>{{ t('Type') }}</th>
                                <th>{{ t('Name') }}</th>
                                <th>{{ t('Value') }}</th>
                                <th>{{ t('Caracteristics') }}</th>
                            </tr>
                        </thead>
                        <tbody>
                            <template v-for="(item, index) in results">
                            <tr>
                                <template v-if="item.is_song">
                                    <td>{{ t('Song') }}</td>
                                    <td>{{item.title}}</td>
                                </template>
                                <template v-else>
                                    <td>{{ t('Group') }}</td>
                                    <td>{{item.name}}</td>
                                </template>
                                <td>
                                    <input type="checkbox" v-model="item.selected"/>
                                </td>
                                <td>{{ t('Force value : ') }}<input type="text" v-model="item.order_value" /></td>
                                <td>
                                    <span v-if="item.order_value>0"> - </span>
                                    <i class="arrow up icon" @click.prevent="sendUp(item, index)" v-if="item.order_value>0"></i>
                                    <span v-if="item.order_value>0"> - </span>
                                    <i class="arrow down icon" @click.prevent="sendDown(item, index)" v-if="results.length-1>item.order_value"></i>
                                </td>
                            </tr>
                            </template>
                        </tbody>
                    </table>
                    <p><button class="ui button primary" @click="save()">{{ t('Save changes') }}</button></p>
                </div>
            </div>
        </div>
</template>

<script>
import axios from 'axios'
import {root_url, songs_by_page} from '@/common/index.js'

export default {
    data() {
        return {
            results: Array,
        }
    },
    created() {
        axios.get(root_url + "book/elements/list/")
            .then(response => {
                    this.results = response.data;
            },  (error) => { console.log(error) });
    },
    methods: {
        sync() {
            axios.get(root_url + "book/elements/list/")
            .then(response => {
                    this.results = response.data;
            },  (error) => { console.log(error) });
        },
        saveArray(arrayToSave) {
            axios.put(root_url + "book/elements/sort/", arrayToSave)
                .then(response => {},
                (error) => { console.log("Error", error) });
        }, 
        save() {
            this.saveArray(this.results)
        }, 
        sendUp(item, index){
            let other_index = -1
            for (var i = 0; i < this.results.length; i++) {
                if( this.results[i].order_value == item.order_value-1 ){
                    other_index = i
                    this.results[i].order_value = item.order_value
                    this.results[index].order_value--
                    break
                }
            }
            if( other_index >= 0 ){
                this.results[index] = this.results[other_index]
                this.results[other_index] = item
                // this.saveArray(
                //     [this.results[index], this.results[other_index]]
                // )
            }
        },
        sendDown(item, index){
            let other_index = -1
            for (var i = 0; i < this.results.length; i++) {
                if( this.results[i].order_value == item.order_value+1 ){
                    other_index = i
                    this.results[i].order_value = item.order_value
                    this.results[index].order_value++
                    break
                }
            }
            if( other_index >= 0 ){
                this.results[index] = this.results[other_index]
                this.results[other_index] = item
                // this.saveArray(
                //     [this.results[index], this.results[other_index]]
                // )
            }
        }
    }
}
</script>
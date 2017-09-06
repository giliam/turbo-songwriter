<template>
    <p>
        {{item.title}} - 
        <router-link :to="{name: 'song_detail', params:{item_id: item.id}}">Show</router-link> - 
        <router-link :to="{name: 'song_edit', params:{item_id: item.id}}">Edit</router-link>
    </p>
</template>

<script>
    export default {
        name: "Songtitle",
        props:{
            item: Object
        },
        methods:{
            launch_show_song: function(item) {
                this.$emit("show_song", item.id)
            },
            launch_edit_song: function(item) {
                this.$emit("edit_song", item.id)
            }
        }
    }
</script>
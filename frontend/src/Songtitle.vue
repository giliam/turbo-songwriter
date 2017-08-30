<template>
    <p>{{item.title}} - <a @click.prevent="launch_show_song(item)">Show</a> - <a @click.prevent="launch_edit_song(item)">Edit</a></p>
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
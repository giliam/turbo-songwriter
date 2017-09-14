<template>
    <div class="ui grid">
        <router-link :to="{name: 'song_detail', params:{item_id: item.id}}" tag="div" class="ten wide column">{{item.title}}</router-link>
        <div class="six wide column">
            <router-link :to="{name: 'song_detail', params:{item_id: item.id}}">{{ t('Show') }}</router-link> - 
            <router-link :to="{name: 'song_edit', params:{item_id: item.id}}">{{ t('Edit') }}</router-link>
        </div>
    </div>
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
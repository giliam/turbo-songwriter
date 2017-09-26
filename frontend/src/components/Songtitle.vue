<template>
    <div class="item">
        <div class="right floated content">
            <router-link :to="{name: 'song_detail', params:{item_id: item.id}}">{{ t('Show') }}</router-link> - 
            <router-link :to="{name: 'song_edit', params:{item_id: item.id}}">{{ t('Edit') }}</router-link>
        </div>
        <i class="music icon"></i>
        <div class="content">
            <router-link :to="{name: 'song_detail', params:{item_id: item.id}}" tag="a" class="header">{{item.title}}</router-link>
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
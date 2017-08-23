<template>
    <div id="song">
        <h2>{{ result.title }}</h2>
    </div>
</template>

<script>
    import axios from 'axios'

    export default {
        props: {
            item_id: Number
        },
        data() {
            return {
                result: Object
            }
        },
        created(){
            axios.get("http://localhost:8000/songs/" + this.$props.item_id + ".json")
                .then(response => {
                    this.result = response.data;
                })
        }
    }
</script>
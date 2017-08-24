<template>
    <div id="song">
        <slot></slot>
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
        watch : {
            item_id : function (value) {
                console.log("Receives", value)
                this.item_id = value
                if( this.item_id ){
                    axios.get("http://localhost:8000/songs/" + this.item_id + ".json")
                        .then(response => {
                            console.log(response.data)
                            this.result = response.data;
                        })
                }
            }
        }
    }
</script>
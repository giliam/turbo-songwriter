<template>
    <div>
        <p>{{ content }}</p>
        <button @click.prevent="edit">Edit</button>
    </div>
</template>

<script>
    export default {
        props: {
            content: String,
            id: Number
        },
        methods: {
            edit () {
                console.log("Edit", this.$props.id)
            },
        }
    }
</script>
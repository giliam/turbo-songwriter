<template>
    <div>
        <p>{{ verse.content }} - <a @click.prevent="editVerse()">Edit verse</a></p>
    </div>
</template>

<script>
    export default {
        props: {
            verse: Object
        },
        methods: {
            editVerse() {
                console.log("Edit verse")
            }
        }
    }
</script>
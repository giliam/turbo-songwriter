<template>
    <div>
        <form class="ui form">
            <fieldset>
                <p class="field">
                    <label for="username">{{ t('Username') }}:</label>
                    <input type="text" name="username" v-model="username">
                </p>
                <p class="field">
                    <label for="password">{{ t('Password') }}:</label>
                    <input type="password" name="password" v-model="password">
                </p>
                <p class="field"><button @click.prevent="log_in()" class="ui primary button">{{ t('Save') }}</button></p>
            </fieldset>
        </form>
    </div>
</template>

<script>
    import { mapActions } from 'vuex'

    export default {
        data() {
            return {
                username: "",
                password: ""
            }
        },
        methods: {
            ...mapActions({
                launch_login: "log_in"
            }),
            log_in(){
                if( this.launch_login({
                    username: this.$data.username, 
                    password: this.$data.password
                }) ){
                }else{
                }
            }
        }
    }
</script>
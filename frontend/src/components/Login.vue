<template>
    <div>
        <div class="ui negative message" v-if="error_message">
            <i class="close icon" @click="error_message = false"></i>
            <div class="header">
                {{ t("Sorry, we couldn't log you in") }}
            </div>
            <p>{{ t('The credentials are wrong!') }}</p>
        </div>
        <form class="ui form">
            <fieldset>
                <p class="field">
                    <label for="username">{{ t('Username') }}:</label>
                    <input type="text" name="username" v-model="username" v-focus>
                </p>
                <p class="field">
                    <label for="password">{{ t('Password') }}:</label>
                    <input type="password" name="password" v-model="password">
                </p>
                <p class="field"><button @click.prevent="log_in()" class="ui primary button">{{ t('Login') }}</button></p>
            </fieldset>
        </form>
    </div>
</template>

<script>
    import { mapActions, mapGetters } from 'vuex'

    import store from '@/store'

    export default {
        data() {
            return {
                username: "",
                password: "",
                error_message: false
            }
        },
        methods: {
            ...mapActions({
                launch_login: "log_in",
                log_out: "log_out",
            }),
            ...mapGetters([
                'has_jwt_token',
            ]),
            async log_in(){
                this.$data.error_message = false
                var b = await this.launch_login({
                    username: this.$data.username, 
                    password: this.$data.password
                })
                if( b ){
                    this.$router.push(store.getters.get_original_target)
                }else{
                    this.$data.error_message = true
                }
            }
        },
        created(){
            if( this.has_jwt_token() && this.$route.name == "logout" ) {
                this.log_out()
            } else if( this.has_jwt_token() ){
                this.$router.push("/")
            }
        }
    }
</script>
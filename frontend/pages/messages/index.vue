<template>
    <div class="d-flex flex-column font-theme">
        <TopBar />
        <div class="container-fluid row mx-auto">
            <div class="col-md-3 p-0 d-flex flex-column">
                <div class="chat-top-bar top-bar-theme">
                    <h5 class="lead">Direct messages</h5>
                </div>
                <div class="messaged-users-contrainer">
                    <div v-for="user in messagedUsers" :key="user.id" :id="user.id" class="bg-color text-theme-secondary p-2 messaged-user">
                        <h5 @click="openChat(user)" class="font-theme lead">
                            <b-avatar class="usericon"></b-avatar>
                            <strong> {{user.username}} </strong>
                        </h5>
                    </div>  
                </div>
               
            </div>
            <div class="px-0 col-md-9">
                <Chat v-if="this.activeChatUser" :key="this.activeChatUser.id" :user="this.activeChatUser" />
            </div>
        </div>

    </div>
</template>

<script>
import vueCustomScrollbar from 'vue-custom-scrollbar'
import "vue-custom-scrollbar/dist/vueScrollbar.css"

import TopBar from "@/components/TopBar"
import Chat from "@/components/Chat"

export default {
    name: "Messages",
    components: {TopBar, Chat, vueCustomScrollbar},
    middleware: ["auth-notLoggedIn"],
    head: function() {
        return {
            title: "Home",
            meta: [
                {
                name: "viewport",
                content: "width=device-width, initial-scale=1, shrink-to-fit=no",
                },
            ],
            bodyAttrs: {
                class: "body-theme",
            },
        };
    },

    data: function() {
        return {
            activeChatUser: undefined,
            messagedUsers: []
        }
    },

    created: async function() {
        let response = await this.$axios.get(`account/get_messaged_users/`)

        this.messagedUsers = response.data.reverse()

        if(this.$route.query.user != undefined)
            this.messagedUsers.unshift(this.$route.query.user)

        this.activeChatUser = !this.messagedUsers ? null : this.messagedUsers[0]

        if(this.$route.query.user != undefined)
            this.$router.replace('/messages')
    },

    mounted: function() {
        //mounted executes before created has ended so timeout is needed
        setTimeout(() => this.toggleSelectedUser(), 500);
    },  

    methods: {
        openChat(user) {
            document.getElementById(`${this.activeChatUser.id}`).classList.toggle("messaged-user-selected")
            this.activeChatUser = user
            document.getElementById(`${user.id}`).classList.toggle("messaged-user-selected")
        },

        toggleSelectedUser() {
            if(this.activeChatUser != null)
                document.getElementById(`${this.activeChatUser.id}`).classList.toggle("messaged-user-selected")
        }
    }
}
</script>

<style scoped>
/* Move these styles into static folder */
.chat-top-bar {
    height: 50px;
}

.chat-top-bar > h5 {
    margin-top: calc((50px - 24px) / 2);
    margin-bottom: calc((50px - 24px) / 2);
    margin-left: 5px;
}

.messaged-user {
    margin-top: 10px;
    border-radius: 5px;
}

.messaged-user:hover {
    border: 3px solid rgb(71, 26, 71);
}

.messaged-users-contrainer {
    overflow-y: scroll;
    overflow-x: hidden;
    padding-right: 2px;
    height: calc(100vh - 8vh - 50px);
    background-image: url("../../static/patterns/5-dots.png");
    background-size: contain;
}

.messaged-user-selected {
    border: 3px solid rgb(71, 26, 71);
}

</style>
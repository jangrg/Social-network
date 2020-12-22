<template>
    <div class="d-flex flex-column font-theme">
        <TopBar />
        <div class="container-fluid row mx-auto">
            <div class="col-md-3 p-0 d-flex flex-column">
                <div class="chat-top-bar top-bar-theme d-flex justify-content-between">
                    <h5 class="lead">Direct messages</h5>
                    <button @click.prevent="openNewChat = true" class="btn btn-purple btn-new-chat text-align m-2" title="open new chat">
                        ➕
                    </button>
                </div>
                <div class="messaged-users-contrainer">
                    <div v-for="user in messagedUsers" :key="user.id" :id="user.id" class="bg-color text-theme-secondary p-2 messaged-user">
                        <h5 @click.prevent="openChat(user)" class="font-theme lead">
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
        <div v-if="openNewChat">
            <OpenNewChat @user="newChat" />
        </div>
    </div>
</template>

<script>
import TopBar from "@/components/TopBar"
import Chat from "@/components/Chat"
import OpenNewChat from "@/components/OpenNewChat"

export default {
    name: "Messages",
    components: {TopBar, Chat, OpenNewChat},
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
            messagedUsers: [],
            openNewChat: false
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
        //activating periodic function
        setInterval(() => this.checkNewMessagedUsers(), 1000)
    },  

    methods: {
        openChat(user) {

            document.getElementById(`${this.activeChatUser.id}`).classList.toggle("messaged-user-selected")
            this.activeChatUser = user
            document.getElementById(`${user.id}`).classList.toggle("messaged-user-selected")
        },

        newChat(user) {
            this.openNewChat = false

            if(user.searched != undefined) {
                user.searched = undefined
                if(!this.messagedUsers.map((e) => e.id).includes(user.id))
                    this.messagedUsers.unshift(user);

                
                document.getElementById(`${this.activeChatUser.id}`).classList.toggle("messaged-user-selected")
                this.activeChatUser = user
                setTimeout(() => this.toggleSelectedUser(), 100)
            }
        },

        toggleSelectedUser() {
            if(this.activeChatUser != undefined)
                document.getElementById(`${this.activeChatUser.id}`).classList.toggle("messaged-user-selected")
        },

        async checkNewMessagedUsers() {
              let response = await this.$axios.get(`account/get_messaged_users/`)
              if(response.data.length > this.messagedUsers.length) {
                    this.messagedUsers = response.data.reverse()
                    setTimeout(() => this.toggleSelectedUser(), 100)
              }
             
        }

    }
}
</script>
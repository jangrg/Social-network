<template>
    <div class="w-100 h-100 d-flex flex-column font-theme-top-bar">
        <div class="chat-window">
            <div v-for="message in messages" :key="message.id" class="d-flex flex-column">
                <h5 v-if="$auth.user.id == message.sender" class="align-self-end message-bubble sender"> {{message.text_content}} </h5>
                <h5 v-else class="align-self-start message-bubble reciever"> {{message.text_content}} </h5>
            </div>
        </div> 

        <b-form class="align-self-center top-bar-theme message-form">
            <b-form-input
                class="message-input input-grey"
                type="text"
                v-model="newMessage.text_content"
                placeholder="Type a message"
            >
            </b-form-input> 
            <button
                @click.prevent="sendMessage"
                type="submit"
                class="btn"
            > 
            </button>
        </b-form>
    </div>

</template>

<script>
export default {
    name: "Chat",
    props: {
        user: Object
    },

    data: function() {
        return {
            messages: [],
            newMessage: {
                photo: null,
                text_content: "",
                sender: this.$auth.user.id,
                receiver: this.user.id
            },
            checkPendingMessages: undefined
        }
    },

    created: async function() {
        let response = await this.$axios.post(`account/${this.user.id}/get_messages/`)

        this.messages = response.data.reverse()
    },

    mounted: function() {
        this.checkPendingMessages = setInterval(() => this.checkNewMessages(), 1000)
    },

    beforeDestroy: function() {
        clearInterval(this.checkPendingMessages)
    },

    methods: {
        async sendMessage() {
            if(this.newMessage.text_content == "")
                return

            console.log(this.newMessage)
            let response = await this.$axios.post(`account/${this.user.id}/send_message/`, this.newMessage)
            //this.messages.push(response.data)

            //tmp solution
            this.messages.unshift({ 
                text_content: this.newMessage.text_content,
                photo: this.newMessage.photo,
                sender: this.newMessage.sender,
                receiver: this.newMessage.receiver
            });

            this.newMessage.text_content = ""
        },

        async checkNewMessages() {
            let response = await this.$axios.post(`account/${this.user.id}/get_messages/`)
            if(response.data.length > this.messages.length)
                   this.messages = response.data.reverse()
        }
    }
}
</script>
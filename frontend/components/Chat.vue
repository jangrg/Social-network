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
                :disabled="!allowSubmit"
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
            }
        }
    },

    created: async function() {
        let response = await this.$axios.post(`account/${this.user.id}/get_messages/`)
        // console.log(response)

        this.messages = response.data.reverse()
    },

    methods: {
        async sendMessage() {
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
        }
    },

    computed: {
        allowSubmit() {
            return this.newMessage.text_content != ""
        }
    }
}
</script>

<style scoped>
/* Move these styles into static folder */

.chat-window {
    display: flex;
    flex-direction: column-reverse;
    overflow-y: scroll;
    height: 86vh;
    padding-right: 2vw;
    padding-left: 2vw;
}

.message-form {
    position: relative;
    bottom: 0px;
    display: flex;
    justify-content: center;
    width: 100%;
    height: 6vh;
    min-height: 40px;
}

.message-form > button {
    margin: auto 10px auto 5px;
    height: 30px;
    width: 50px;
    background-image: url("../static/send_message.png");
    background-position: center;
    background-repeat: no-repeat;
    background-size: contain;
}

.message-input {
    max-height: 30px;
    width: 80%;
    margin: auto 5px auto 10px !important;
}

.message-bubble.sender {
    background-color: rgb(86, 19, 142);;
}

.message-bubble.reciever {
    background-color: #2b2828;
}

.message-bubble {
    word-wrap: break-word;
    max-width: 60%;
    color: white;
    border-radius: 40px;
    padding: 15px;
    margin: 12px;
}


</style>
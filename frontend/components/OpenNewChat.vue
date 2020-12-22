<template>
  <transition name="preview">
        <div class="overlay">
            <div class="media font-theme text-left">
                <div class="media-body post-theme p-5 d-flex flex-column">
                    <b-form-input
                    type="search"
                    class="form-control search-bar input-grey"
                    v-model="searchQuery"
                    placeholder="Send messeage to..."
                    @input="search"
                    ></b-form-input>

                    <div v-if="this.searchQuery != ''" class="send-message-to-container text-theme-secondary text-center">
                        <h6 v-if="this.searchResult.length == 0" class="mt-3"> 
                            <i>No users found</i>
                        </h6>
                        <div v-for="user in searchResult" :key="user.id" :id="user.id" class="bg-color text-theme-secondary p-2 messaged-user text-left">
                            <h5 @click.prevent="closeWindow(user)" class="font-theme lead">
                                <b-avatar class="usericon"></b-avatar>
                                <strong> {{user.username}} </strong>
                            </h5>
                        </div>
                    </div>   
                    <button
                    @focus="closeWindow(undefined)" 
                    class="btn btn-purple mt-2 text-align align-self-end"
                    >
                        Close
                    </button>
                </div>
            </div>
        </div>
  </transition>
</template>


<script>

export default {
    name: "OpenNewChat",
    data: function() {
        return  {
            searchResult: [],
            searchQuery: ""
        }
    },
    methods: {
        closeWindow(user) {
            if(user != undefined)
                user.searched = true
            this.$emit("user", user)
        },

        async search() {
            if(this.searchQuery == "")
                return
            
            let result = await this.$axios.get(`/account/`, {params:  { query: this.searchQuery}});
            this.searchResult = result.data

        }
    }
}

</script>
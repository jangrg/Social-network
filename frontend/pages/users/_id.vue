<template>
  <div class="d-flex flex-column bg-pattern">
    <div class="container-fluid sticky-top">
      <b-navbar variant="warning">
        <b-button class="btn btn-primary btn-lg text-align mx-1" to="/home">Home</b-button>
        <b-button class="btn btn-primary btn-lg text-align mx-1" @click.prevent="logOut">Logout</b-button>
      </b-navbar>
    </div>
    <div v-if="this.loaded" class="container-fluid row  mx-auto">
      <div class="col-md-2 my-4">
        <b-avatar size="16rem" src=""></b-avatar>
        <h1 class="profile-username">{{user.username}}</h1>
        <h2 class="profile-email">{{user.email}}</h2>
      </div>
      <div class="col-md-8 white-container rounded my-4">
        <h3>{{user.username}}'s posts:</h3>
        <!-- Just as an example -->
        <!-- <Post post=""/>
        <Post post=""/> Morao zakomentirati da radi. -->
      </div>
      
      <div class="col-md-2 my-4">
        <b-button v-if="anotherUser" class="btn btn-primary btn-lg text-align mx-1">Follow</b-button>
        <b-button v-if="anotherUser" class="btn btn-secondary btn-lg text-align mx-1">Message</b-button>
        <div class="my-4">
          <h1 class="subtitle">See also:</h1>

          <div class="media border p-1">
            <div class="media-body post-color p-1">
              <div class="d-flex align-items">
                <b-avatar class="mx-1"></b-avatar>
                <h5 class="lead mt-0">
                <strong> Other user/shop username</strong>
                </h5>
              </div>
              <p class="lead">
                Other user/shop profile information.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div>
      <!-- Empty div needed for alignment -->
    </div>
  </div>
</template>

<script>
import Post from "../../components/Post";

export default {
    name: "User",
    components: { Post },
    middleware: ['auth-notLoggedIn'],
    head() {
        return {
        title: "User",
        meta: [
            {
            name: "viewport",
            content: "width=device-width, initial-scale=1, shrink-to-fit=no",
            },
        ],
        };
    },

    data() {
      return {
        loaded: false,
        id: this.$route.params.id,
        currentUser: "",
        posts: []
      } 
    },

    async created() {
      try{
        let response = await this.$axios.get(`/account/${this.id}/`)
        this.currentUser = response.data
        this.loaded = true
      }catch(e) {
        this.$toast.error(`${e.response.status} ${e.response.statusText}`, {
        duration: 8000});
        this.$router.push("/home");
      }
    },
    computed: {
      user() {
        if(this.anotherUser)
          return this.currentUser
        else
          return this.$auth.user
      },

      anotherUser() {
        return this.id !== this.$auth.user.id
      }
    },
    methods: {
        logOut() {
            this.$store.commit('User/RESET_USER')
            this.$router.push('/')
        }
    },

}
</script>

<style scoped>

</style>

<template>
  <div class="container-fluid sticky-top font-theme-top-bar">
    <b-navbar class="top-bar top-bar-theme">
      <div class="row container-fluid center inline-block">
        <b-navbar class="col-2 topbar-logo"
          ><nuxt-link class="logo" to="/home"> WeShare </nuxt-link></b-navbar
        >
        <div class="col-4">
          <b-form class="navbar-form fix form-theme">
            <input
              type="search"
              class="form-control search-bar input-grey"
              v-model="searchQuery"
              placeholder="Search"
            />
            <b-button
              variant="btn search-btn"
              :disabled="search"
              :to="{
                name: 'search-keyword',
                params: { keyword: this.searchQuery }
              }"
              type="submit"
            ></b-button>
          </b-form>
        </div>
        <div class="links" v-if="!this.$auth.user">
          <b-button variant="btn btn-purple text-align btn-lg" to="/register"
            >Register</b-button
          >
          <b-button variant="btn btn-purple text-align btn-lg" to="/login"
            >Login</b-button
          >
        </div>
        <!-- <div class="col-2" v-if="this.$auth.user">
          <button class="btn btn-lg ml-auto" v-b-toggle.sidebar-right>
            <i class="fa fa-bars"></i>
          </button>
        </div-->
        <div
          class="topbar-buttons col-2 avatar d-flex justify-content-end"
          v-if="this.$auth.user"
        >
          <b-button
            id="button-home"
            class="button-home"
            variant="btn text-align btn-lg"
            to="/following"
            v-if="this.user"
          ></b-button>
          <b-button
            id="button-explore"
            class="button-explore"
            variant="btn text-align btn-lg"
            to="/home"
            v-if="this.user"
          ></b-button>
          <b-button
            id="button-message"
            class="button-message"
            variant="btn text-align btn-lg"
            v-if="this.user"
          ></b-button>
          <b-avatar
            class="mb-2 usericon"
            variant="dark"
            :to="{ name: 'users-id', params: { id: this.user.id } }"
            v-if="this.user"
          ></b-avatar>
          <b-button
            variant="btn btn-purple text-align btn-lg btn-logout"
            @click.prevent="logOut"
            v-if="this.user"
            >Logout</b-button
          >
        </div>
      </div>
    </b-navbar>
  </div>
</template>

<script>
export default {
  name: "TopBar",
  data() {
    return {
      // posts: [],
      searchQuery: ""
    };
  },
  computed: {
    user() {
      return this.$auth.user;
    },
    search() {
      return this.searchQuery == "";
    }
  },
  head: {
    link: [
      {
        rel: "stylesheet",
        href:
          "https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"
      }
    ]
  },
  methods: {
    // emitPost(parameters) {
    //   this.$emit("post", parameters);
    // },
    logOut() {
      this.$auth.logout();
      this.$router.push("/");
    }
  }
};
</script>

<style></style>

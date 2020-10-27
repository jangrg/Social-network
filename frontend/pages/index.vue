<template>
  <div class="d-flex flex-column bg justify-content-between">
    <div>
      <div class="container-fluid" v-if="loggedIn">
        <b-navbar variant="warning">
          <b-navbar-brand class="lead"><strong>Wellcome!</strong></b-navbar-brand>
          <b-button class="btn btn-primary btn-lg text-align mx-1" to="/users">Profile</b-button>
          <b-button class="btn btn-primary btn-lg text-align mx-1" @click.prevent="logOut">Logout</b-button>
        </b-navbar>
      </div>
    </div>
    <div class="mx-auto">
      <div class="lead border rounded mx-auto p-4 white-container justify-content-center">
        <div class="d-flex flex-column container">
          <h1 class="title">
            Welcome to our Social Network
          </h1>
          <h2 class="subtitle">
            Feel free to register now!
          </h2>
          <div class="links">
            <b-button v-if="!loggedIn" class="btn btn-primary btn-lg text-align" to="/register">Register</b-button>
            <b-button v-if="!loggedIn" variant="btn btn-outline-primary btn-lg text-align" to="/login">Login</b-button>
          </div>
        </div>
      </div>
    </div>
    <div></div>
  </div>
</template>

<script>
import { ButtonPlugin } from 'bootstrap-vue'

export default {
  name: "Homepage",

  head() {
    return {
      title: "Homepage",
      meta: [
        {
          name: "viewport",
          content: "width=device-width, initial-scale=1, shrink-to-fit=no",
        },
      ],
    };
  },
  computed: {
      loggedIn() {
        return this.$store.state.User.user == undefined ? false : true;
      }
  },
  methods: {
      logOut() {
        this.$store.commit('User/RESET_USER')
        this.$router.push('/')
      }
  }
}
</script>

<style>
.container {
  align-items: center;
  text-align: center;
}

.title {
  font-family: 'Quicksand', 'Source Sans Pro', -apple-system, BlinkMacSystemFont,
    'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  display: block;
  font-weight: 300;
  font-size: 75px;
  color: #24303d;
  letter-spacing: 1px;
}

.subtitle {
  font-weight: 300;
  font-size: 42px;
  color: #5b6885;
  word-spacing: 5px;
  padding-bottom: 15px;
}

.links {
  padding-top: 15px;
}

.btn {
  width: 100px;
}

.btn-primary {
  background-color: #182839;
}

</style>

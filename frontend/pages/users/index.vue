<template>
  <div class="d-flex flex-column justify-content-between">
    <div>
      <div class="container-fluid">
        <b-navbar variant="warning">
          <b-button class="btn btn-primary btn-lg text-align mx-1" to="/">Home</b-button>
          <b-button class="btn btn-primary btn-lg text-align mx-1" @click.prevent="logOut">Logout</b-button>
        </b-navbar>
      </div>
    </div>
    <div class="d-flex flex-column justify-content-top mx-auto user-data">
        <div class="my-2">
            <h1>Your profile</h1>
        </div>
        <div class="my-2">
            <h1>Name: {{$store.state.User.user.username}} </h1>
        </div>
        <div class="my-2">
            <h1>E-mail: {{$store.state.User.user.email}} </h1>
        </div>
    </div>
    <div></div>
  </div>
</template>

<script>

export default {
    // this page needs id in URL
    name: "User",

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
    methods: {
        logOut() {
            this.$store.commit('User/RESET_USER')
            this.$router.push('/')
        }
    }
}
</script>

<style>
    .user-data {
        text-align: center;

        font-family: 'Quicksand', 'Source Sans Pro', -apple-system, BlinkMacSystemFont,
    'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        font-weight: 300;
        font-size: 75px;
        color: #24303d;
        letter-spacing: 1px;
    }

</style>

<template>
  <b-sidebar id="sidebar" title="Menu" shadow>
    <div class="card">
      <div class="card-body">
        <h4 class="card-title lead">Hello {{ user.username }}!</h4>
        <h5 class="card-subtitle lead">What will we do today?</h5>
        <div class="card-link p-1 mx-auto">
          <a
            v-b-toggle.postForm
            variant="primary"
            class="mx-auto btn-inline"
            type="button"
            >Make a new post!</a
          >
        </div>
      </div>
    </div>
    <div class="container-fluid bg-muted">
      <b-collapse id="postForm" class="mt-1 mb-1 col-md-11">
        <b-form>
          <label>New post:</label>
          <b-form-input
            type="text"
            placeholder="Name of post?"
            v-model="newPost.name"
          >
          </b-form-input>

          <div class="form-group">
            <label for=""></label>
            <textarea
              class="form-control"
              rows="4"
              v-model="newPost.content"
            ></textarea>
          </div>

          <button
            @click.prevent="postForm"
            type="submit"
            class="btn btn-primary mt-2 text-align"
          >
            Submit
          </button>
        </b-form>
        <hr />
      </b-collapse>
    </div>
    <div class="container">
      <form
        v-if="this.user"
        class="form-inline navbar-form mt-xs-2 ml-auto"
      >
        <input type="search" class="form-control" v-model="searchQuery"/>
        <b-button
          class="btn btn-primary btn-lg text-align mt-1"
          :to="{name:'search-keyword', params: {keyword: this.searchQuery}}"
          v-if="this.user"
          >Search</b-button
        >
      </form>
    </div>
    <div class="container mt-3">
      <nuxt-link
        class="btn btn-primary btn-lg"
        :to="{name:'users-id', params: {id: this.user.id}}"
        v-if="this.user"
      >
        Profile
      </nuxt-link>
      <button
        class="btn btn-primary btn-lg"
        @click.prevent="logOut"
        v-if="this.user"
      >
        Logout
      </button>
    </div>
  </b-sidebar>
</template>

<script>
export default {
  name: "SideBar",
  data() {
    return {
      newPost: {
        name: "",
        content: "",
        owner: this.$store.state.User.user
      },
      searchQuery: ""
    };
  },
  computed: {
    user() {
      return this.$store.state.User.user;
    },
  },
  methods: {
    postForm() {
        console.log(this.newPost.name + " " + this.newPost.content + " " + this.newPost.owner.username);
        //let response = await this.$axios.post(`account/create/post`, this.newPost);
        this.$toast.show("Zahtjev uspješno poslan!", { duration: 8000 });
    },
    logOut() {
      // send request to backend to logout!
      this.$store.commit("User/RESET_USER");
      this.$router.push("/");
    },
    allowSubmit() {
      
    }
  },
};
</script>

<style scoped>
</style>
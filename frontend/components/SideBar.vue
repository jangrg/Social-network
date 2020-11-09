<template>
  <b-sidebar id="sidebar-right" title="WeShare" right shadow>
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
          class="btn btn-primary mt-2"
          :to="{name:'search-keyword', params: {keyword: this.searchQuery}}"
          v-if="this.user"
          >Search</b-button
        >
      </form>

    <hr>

    </div>
    <div class="d-flex mt-4 p-1 justify-content-around">
      <nuxt-link
        class="btn btn-primary"
        to="/home"
        v-if="this.user && $nuxt.$route.path != '/home'"
      >
      Home
      </nuxt-link>
      <nuxt-link
        class="btn btn-primary"
        :to="{name:'users-id', params: {id: this.user.id}}"
        v-if="this.user"
      >
        Profile
      </nuxt-link>
      <button
        class="btn btn-primary"
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
        content: "",
        photo: null,
        type_attr: null,
        likes_num: 0,
        posted_by: this.$auth.user.id,
      },
      posts : [],
      searchQuery: ""
    };
  },
  created: async function () {
    let response = await this.$axios.get(`post/`);
    //debugger

    console.log($nuxt.$route.path);

    this.posts = response.data.reverse();

    this.$emit("posts", this.posts);
  },
  computed: {
    user() {
      return this.$auth.user;
    },
  },
  methods: {
    async postForm() {
      console.log(
        this.newPost.posted_by +
          " " +
          this.newPost.content +
          " " +
          this.newPost.likes_num
      );
      try {
        let res = await this.$axios.post(`post/`, this.newPost);

        //debugger

        console.log(res);
        if (res.status == 201) {
          this.$toast.show("Post uspješno objavljen!", { duration: 8000 });
          this.newPost.posted_by = {username: this.$auth.user.username, id: this.$auth.user.id};
          this.posts.unshift(this.newPost);
          this.$emit("posts", this.posts);
        }
      } catch (e) {
        this.$toast.error(`${e.response.status} ${e.response.statusText}`, {
          duration: 8000,
        });
      }
    },
    logOut() {
      this.$auth.logout()
      this.$router.push("/");
    },
    allowSubmit() {
      
    }
  },
};
</script>

<style scoped>
</style>
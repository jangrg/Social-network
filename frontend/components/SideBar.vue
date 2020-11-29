<template>
  <b-sidebar
    id="sidebar-right"
    title="WeShare"
    class="bg-color"
    right
    shadow
    header-class="sidebar-theme"
    body-class="bg-color"
    close-label="close-sidebar-theme"
  >
    <template #header-close>
      <i class="fa fa-window-close close-sidebar-theme"></i>
    </template>
    <div class="container bg-color sidebar-theme p-2">
      <div class="">
        <h4>Hello {{ user.username }}!</h4>
        <h5>What will we do today?</h5>
        <div class="link p-1 mx-auto">
          <a
            v-b-toggle.postForm
            variant="warning"
            class="mx-auto btn-inline text-theme"
            type="button"
            >Make a new post!</a
          >
        </div>
      </div>
    </div>
    <div class="container-fluid">
      <b-collapse id="postForm" class="mt-1 mb-1 col-md-11 collapsible-fill">
        <b-form id="form">
          <label class="text-theme-secondary mb-0 p-0">New post:</label>

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
            class="btn btn-outline-warning btn-fill mt-2 text-align"
          >
            Submit
          </button>
        </b-form>
        <hr class="post-separator-theme"/>
      </b-collapse>
    </div>
    <div class="container">
      <form v-if="this.user" class="form-inline navbar-form mt-xs-2 ml-auto">
        <input type="search" class="form-control w-100" v-model="searchQuery" placeholder="Search"/>
        <b-button
          variant="btn btn-outline-warning btn-fill mt-2"
          :to="{
            name: 'search-keyword',
            params: { keyword: this.searchQuery },
          }"
          v-if=" this.$auth.user && this.searchQuery"
          >Search</b-button
        >
      </form>

      <hr />
    </div>
    <div class="row mt-4 container mx-0">
      <nuxt-link
        class=" sidebar-link-theme text-theme-secondary  col-12"
        to="/home"
        v-if=" this.$auth.user && $nuxt.$route.path != '/home'"
      >
        Home
      </nuxt-link>
      <nuxt-link
        class=" sidebar-link-theme text-theme-secondary  col-12"
        :to="{ name: 'users-id', params: { id: this.user.id } }"
        v-if="this.user"
      >
        Profile
      </nuxt-link>
      <a type="button" class="sidebar-link-theme no-border text-theme-secondary col-12" @click.prevent="logOut" v-if="this.user">
        Logout
      </a>
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
      posts: [],
      searchQuery: "",
    };
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

        console.log(res);
        if (res.status == 201) {
          this.$toast.show("Post uspješno objavljen!", { duration: 8000 });
          let createdPost = res.data;
          document.getElementById("form").reset();
          this.$emit("post", createdPost);
        }
      } catch (e) {
        this.$toast.error(`${e.response.status} ${e.response.statusText}`, {
          duration: 8000,
        });
      }
    },
    logOut() {
      this.$auth.logout();
      this.$router.push("/");
    },
    allowSubmit() {},
  },
};
</script>

<style scoped>
</style>
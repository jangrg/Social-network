<template>
  <div class="d-flex flex-column bg-pattern font-theme">
    <TopBar @post="addPost" />
    <div class="container-fluid row text-theme mx-auto">
      <div class="container-fluid col-md-2 my-4 text-center">
        <div class="post-theme p-3">
          <b-avatar class="profile-icon" src=""></b-avatar>
          <h1 class="profile-username">{{ user.username }}</h1>
          <h2 class="profile-email">{{ user.email }}</h2>
          <button
            v-if="anotherUser"
            class="btn btn-purple btn-lg text-align p-1 m-1 my-1"
          >
            Follow
          </button>
          <button
            v-if="anotherUser"
            class="btn btn-purple btn-lg text-align p-1 m-1 my-1"
          >
            Message
          </button>
        </div>
      </div>
      <div class="col-md-8 no-border my-3">
        <div class="text-center">
          <div v-if="!anotherUser" class="container-fluid new-post">
            <PostForm @post="setPost" />
          </div>
        </div>
        <div v-for="post in posts" :key="post.id">
          <Post :post="post" />
        </div>
      </div>

      <div class="container-fluid col-md-2 my-4">
          <div class="post-theme p-3">
            <div class="bg-color text-theme-secondary p-2">
               <h5 class="font-theme lead">
                <b-avatar class="usericon"></b-avatar>
                <strong> Other user</strong>
              </h5>
            </div>
            <hr />
            <h5 class="font-theme mx-2">Other user profile information.</h5>
          </div>
      </div>
    </div>
  </div>
</template>

<script>
import Post from "@/components/Post";
import TopBar from "@/components/TopBar";
import PostForm from "@/components/PostForm";

export default {
  name: "User",
  components: { Post, TopBar, PostForm },
  middleware: ["auth-notLoggedIn"],
  head() {
    return {
      title: "User",
      bodyAttrs: {
        class: "body-theme",
      },
      meta: [
        {
          name: "viewport",
          content: "width=device-width, initial-scale=1, shrink-to-fit=no",
        },
      ],
    };
  },

  data: function () {
    return {
      id: this.$route.params.id,
      currentUser: "",
      posts: [],
    };
  },

  created: async function () {
    try {
      let response = await this.$axios.get(`/account/${this.id}/`);
      this.currentUser = response.data;

      
      response = await this.$axios.get(`post/?by_user=${this.id}`);
      this.posts = response.data;

    } catch (e) {
      // this.$toast.error(`${e.response.status} ${e.response.statusText}`, {
      //   duration: 8000,
      // });
      // this.$router.push("/home");
      consol.log(e);
    }

  },

  computed: {
    user() {
      if (this.anotherUser) return this.currentUser;
      else return this.$auth.user;
    },

    anotherUser() {
      return this.id !== this.$auth.user.id;
    },
  },

  methods: {
    setPost(parameters) {
      this.posts.unshift(parameters);
    },
  },
};
</script>
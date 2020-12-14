<template>
  <div class="d-flex flex-column bg-pattern font-theme">
    <TopBar />
    <div class="container-fluid row text-theme mx-auto">
      <div class="container-fluid col-md-2 my-4 text-center">
        <div class="post-theme p-3">
          <b-avatar class="profile-icon" src=""></b-avatar>
          <h1 class="profile-username">{{ this.store.name }}</h1>
          <h2 class="profile-email">{{ this.owner.username }}</h2>
          <button
            v-if="anotherUser"
            class="btn btn-purple btn-lg text-align p-1 m-1 my-1"
            @click="follow"
          >
            Follow
          </button>
          <button
            v-if="anotherUser"
            class="btn btn-purple btn-lg text-align p-1 m-1 my-1"
            @click.prevent="sendMessage"
          >
            Message
          </button>
          <button
            v-if="!anotherUser"
            class="btn btn-purple btn-outline btn-lg text-align p-1 m-1 my-1"
            @click="changeTheme"
          >
            Change theme!
          </button>
        </div>
      </div>

      <PostFeed :filter="`?by_user=${this.$auth.user.id}`" />

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
import TopBar from "@/components/TopBar";
import PostFeed from "@/components/PostFeed";

export default {
  name: "Store",
  components: { TopBar, PostFeed },
  middleware: ["auth-notLoggedIn"],
  head() {
    return {
      title: "User",
      bodyAttrs: {
        class: "body-theme"
      },
      meta: [
        {
          name: "viewport",
          content: "width=device-width, initial-scale=1, shrink-to-fit=no"
        }
      ]
    };
  },

  data: function() {
    return {
      id: this.$route.params.id,
      store: "",
      currentUser: "",
      owner: ""
    };
  },
  created: async function() {
    try {
      let response = await this.$axios.get(`page/`);
      response.data.forEach(element => {
        if (element.id === this.id) {
          this.store = element;
          this.owner = this.store.owner;
        }
      });
    } catch (e) {
      consol.log(e);
    }
  },

  computed: {
    user() {
      if (this.anotherUser) return this.currentUser;
      else return this.$auth.user;
    },
    anotherUser() {
      return this.owner.id !== this.$auth.user.id;
    }
  },

  methods: {
    setPost(parameters) {
      this.posts.unshift(parameters);
    },

    changeTheme() {
      debugger;
      var theme = this.$auth.$storage.getCookie("theme");
      if (theme == "light") {
        this.$auth.$storage.setCookie("theme", "dark");
      } else {
        this.$auth.$storage.setCookie("theme", "light");
      }
      location.reload();
    },

    async follow() {
      let response = await this.$axios.post(`account/${this.id}/follow/`);
      console.log(response.data);
    },
    sendMessage() {
      this.$router.replace({
        path: "/messages",
        query: Object.assign({}, { user: this.currentUser })
      });
    }
  }
};
</script>

<template>
  <div class="d-flex flex-column bg-pattern font-theme">
    <TopBar />
    <div class="container-fluid row text-theme mx-auto">
      <div class="container-fluid col-md-2 my-4 text-center">
        <div class="post-theme p-3">
          <b-avatar class="profile-icon" src=""></b-avatar>
          <h1 class="profile-username">{{ user.username }}</h1>
          <h2 class="profile-email">{{ user.email }}</h2>
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
        <button
          v-if="!hasPage && !anotherUser"
          class="btn btn-purple btn-lg text-align p-2 m-2 my-1"
          @click="openCreatePage"
        >
          Create store
        </button>
        <b-button
          v-if="hasPage"
          class="btn btn-purple btn-lg text-align p-2 m-2 my-1"
          :to="{ name: 'store-id', params: { id: this.store } }"
        >
          Store page
        </b-button>
      </div>

      <PostFeed
        :filter="`?by_user=${this.id}`"
        v-bind:data-following="followed"
      />

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
      <div v-if="openPreview">
        <CreatePage v-on:delete="removeCreatePage()" />
      </div>
    </div>
  </div>
</template>

<script>
import TopBar from "@/components/TopBar";
import PostFeed from "@/components/PostFeed";
import CreatePage from "@/components/CreatePage";

export default {
  name: "User",
  components: { TopBar, PostFeed, CreatePage },
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
      currentUser: "",
      openPreview: false,
      store: false,
      followed: true
    };
  },

  async beforeCreate() {
    try {
      let response = await this.$axios.get(`page/`);
      response.data.forEach(element => {
        if (element.owner.id === this.id) this.store = element.id;
      });
    } catch (e) {
      console.log(e);
    }
  },

  created: async function() {
    try {
      let response = await this.$axios.get(`/account/${this.id}/`);
      console.log(this.id);
      this.currentUser = response.data;
    } catch (e) {
      console.log(e);
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
    hasPage() {
      if (this.store === false) return false;
      else return true;
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
      if (response.status == 200) {
        this.$toast.show("User followed!", {
          duration: 8000
        });
        this.followed = true;
      }
      console.log(response.data);
    },

    openCreatePage() {
      this.openPreview = true;
    },
    sendMessage() {
      this.$router.replace({
        path: "/messages",
        query: Object.assign({}, { user: this.currentUser })
      });
    },
    removeCreatePage() {
      this.openPreview = false;
    }
  }
};
</script>

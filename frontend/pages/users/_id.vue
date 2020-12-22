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
            id="follow-button"
            v-if="anotherUser && !followed"
            class="btn btn-purple btn-lg text-align p-1 m-1 my-1"
            @click="follow"
          >
            Follow
          </button>
          <button
            v-if="anotherUser && followed"
            class="btn btn-purple btn-lg text-align p-1 m-1 my-1"
          >
            Unfollow
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
            Change theme
          </button>
        </div>
      </div>

      <PostFeed
        :filter="`?by_user=${this.id}`"
        v-bind:data-following="followed"
      />

      <div class="container-fluid col-md-2 my-4">
        <button
          v-if="!hasPage && !anotherUser"
          class="btn btn-purple btn-create text-align p-2 m-2 my-1"
          @click="openCreatePage"
        >
          ➕ create your store
        </button>
        <b-button
          v-if="hasPage"
          class="btn btn-purple btn-create text-align p-2 m-2 my-1"
          :to="{ name: 'store-id', params: { id: this.store.id } }"
        >
          {{ this.store.name }}
        </b-button>
        <!-- <div class="post-theme p-3">
          <div class="bg-color text-theme-secondary p-2">
            <h5 class="font-theme lead">
              <b-avatar class="usericon"></b-avatar>
              <strong> Other user</strong>
            </h5>
          </div>
          <hr />
          <h5 class="font-theme mx-2">Other user profile information.</h5>
        </div> -->
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
      followed: false
    };
  },

  async beforeCreate() {
    try {
      let response = await this.$axios.get(`page/`);
      response.data.forEach(element => {
        if (element.owner.id === this.id) this.store = element;
      });
    } catch (e) {
      console.log(e);
    }
  },

  created: async function() {
      //this endpoint must return following array
      let response = await this.$axios.get(`/account/${this.id}/`);
      this.currentUser = response.data;
  },

  mounted: async function() {
      // if(this.anotherUser) {
      //   console.log(this.$auth.user)
      //   if(this.$auth.user.following.includes(this.id))
      //     this.followed = true
      // }
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
      if(this.followed)
        return

      let response = await this.$axios.post(`account/${this.id}/follow/`);
      this.followed = true
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

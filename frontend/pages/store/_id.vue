<template>
  <div class="d-flex flex-column bg-pattern font-theme">
    <TopBar />
    <div class="container-fluid row text-theme mx-auto">
      <div class="photo">
        <span class="cover-text"
          ><bold>{{ this.store.name }} </bold>
        </span>
      </div>
    </div>
    <div class="container-fluid row text-theme mx-auto">
      <div class="container-fluid col-md-2 my-4 text-center">
        <div class="panel-theme p-2">
          <h1 class="store-text profile-username">
            📍 {{ this.store.location }}
          </h1>
          <h1 class="store-text store-time">
            🕐
            {{
              this.store.work_time == unknown
                ? "not specified"
                : this.store.work_time
            }}
          </h1>
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
        </div>
        <b-button
          id="posts"
          class="btn btn-choice btn-choice-selected btn-fill mt-2 text-align btn-post"
          @click="switchSelect"
        >
          POSTS
        </b-button>
        <b-button
          id="articles"
          class="btn btn-choice btn-fill mt-2 text-align btn-post"
          @click="switchSelect"
        >
          ARTICLES
        </b-button>
      </div>

      <PostFeed
        v-if="this.postsSelected"
        :filter="`?on_page=${this.$route.params.id}`"
      />
      <div v-if="!this.postsSelected" class="container-fluid col-md-8 my-4">
        <h4 class="store-text">
          articles coming...
        </h4>
      </div>

      <div class="container-fluid col-md-2 my-4 text-center">
        <h4 class="text-theme-secondary">STORE OWNER</h4>
        <div class="panel-theme p-1">
          <nuxt-link
            v-if="!isPage"
            :to="{ name: 'users-id', params: { id: this.owner.id } }"
          >
            <b-avatar class="mb-3 smaller-profile-icon" src=""></b-avatar>
            <h1 class="store-text profile-username">
              {{ this.owner.username }}
            </h1>
            <h2 class="store-text profile-email">{{ this.owner.email }}</h2>
          </nuxt-link>
          <button
            v-if="anotherUser"
            class="btn btn-purple btn-lg text-align p-1 m-1 my-1"
            @click="followUser"
          >
            Follow
          </button>
          <button
            v-if="anotherUser"
            class="btn btn-purple btn-lg text-align p-1 m-1 my-1"
            @click.prevent="sendMessageToOwner"
          >
            Message
          </button>
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
      owner: "",
      postsSelected: true
    };
  },
  created: async function() {
    this.currentUser = this.$auth.user;
    try {
      let response = await this.$axios.get(`page/`);
      response.data.forEach(element => {
        if (element.id === this.id) {
          this.store = element;
        }
      });
      response = await this.$axios.get(`account/${this.store.owner.id}`);
      this.owner = response.data;
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

    async followUser() {
      let response = await this.$axios.post(`account/${this.owner.id}/follow/`);
      console.log(response.data);
    },
    async follow() {},
    sendMessageToOwner() {
      this.$router.replace({
        path: "/messages",
        query: Object.assign({}, { user: this.owner })
      });
    },
    switchSelect() {
      this.postsSelected = !this.postsSelected;
      document.getElementById("posts").classList.toggle("btn-choice-selected");
      document
        .getElementById("articles")
        .classList.toggle("btn-choice-selected");
    }
  }
};
</script>

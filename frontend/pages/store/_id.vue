<template>
  <div class="d-flex flex-column bg-pattern font-theme">
    <TopBar />
    <div class="container-fluid row text-theme mx-auto">
      <div class="photo">
        <span class="cover-text"
          ><bold>{{ this.nameEdit ? "" : this.store.name }} </bold>
          <b-form-input
            v-if="this.nameEdit"
            required
            class="input-edit-name"
            v-model="store.name"
            type="text"
            v-on:blur="switchNameEdit"
          >
          </b-form-input>
        </span>
        <b-button
          v-if="!anotherUser"
          class="btn btn-edit-name text-center"
          @click="switchNameEdit"
          >🖊</b-button
        >
        <br />
      </div>
    </div>
    <div class="container-fluid row text-theme mx-auto">
      <div class="container-fluid col-md-2 my-4 text-center">
        <div class="panel-theme p-2">
          <span class="store-text profile-username">
            📍
            {{ this.locationEdit ? "" : this.store.location }}
          </span>
          <b-form-input
            v-if="this.locationEdit"
            required
            class="input-edit"
            v-model="store.location"
            type="text"
            v-on:blur="switchLocationEdit"
          >
          </b-form-input>
          <b-button
            v-if="!anotherUser"
            class="btn btn-edit text-center"
            @click="switchLocationEdit"
            >🖊</b-button
          >
          <br />
          <span class="store-text store-time">
            🕐
            {{
              this.timeEdit
                ? ""
                : this.store.work_time == unknown
                ? "not specified"
                : this.store.work_time
            }}
          </span>
          <b-form-input
            v-if="this.timeEdit"
            required
            class="input-edit"
            v-model="store.work_time"
            type="text"
            v-on:blur="switchTimeEdit"
          >
          </b-form-input>
          <b-button
            v-if="!anotherUser"
            class="btn btn-edit text-center"
            @click="switchTimeEdit"
            >🖊</b-button
          >
          <!-- waiting for backend -->
          <!-- <button
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
          </button> -->
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
        :filter="`${this.$route.params.id}/get_posts_from_page`"
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
        <button
          v-if="!anotherUser"
          class="btn btn-purple btn-create text-align p-2 m-2 my-1"
          @click="deletePage"
        >
          Delete store
        </button>
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
      postsSelected: true,
      nameEdit: false,
      locationEdit: false,
      timeEdit: false
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
    },
    async edit() {
      let formData = new FormData();
      formData.append("name", this.store.name);
      formData.append("location", this.store.location);
      formData.append("work_time", this.store.work_time);
      let response = await this.$axios.patch(
        `page/${this.store.id}/`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        }
      );
    },
    async deletePage() {
      if (confirm("Really want to delete this actualPost?")) {
        let res = await this.$axios.delete(`page/${this.store.id}/`);
        this.$router.go(`user/${this.owner.id}`);
      }
    },
    switchLocationEdit() {
      if (this.locationEdit) this.edit();
      this.locationEdit = !this.locationEdit;
    },
    switchNameEdit() {
      if (this.nameEdit) this.edit();
      this.nameEdit = !this.nameEdit;
    },
    switchTimeEdit() {
      if (this.timeEdit) this.edit();
      this.timeEdit = !this.timeEdit;
    }
  }
};
</script>

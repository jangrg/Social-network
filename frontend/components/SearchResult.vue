<template>
  <div class="post-theme p-3 my-3">
    <div class="bg-color text-theme-secondary p-2">
      <div class="d-flex justify-content-between mt-2 mb-4 mx-2">
        <div class="font-theme lead text-left">
          <b-avatar class="usericon"></b-avatar>
          <strong
            ><nuxt-link
              :to="{ name: 'users-id', params: { id: this.user.id } }"
              >{{ user.username }}</nuxt-link
            ></strong
          >
        </div>
        <div class="text-right">
          <button
            class="btn btn-purple btn-lg text-align p-1 m-1 my-1"
            v-if="this.$auth.user.id != this.user.id && !following"
            @click="follow"
          >
            Follow
          </button>
          <button
            class="btn btn-purple btn-lg text-align p-1 m-1 my-1"
            v-else-if="this.$auth.user.id != this.user.id && following"
            @click="unfollow"
          >
            Unfollow
          </button>
        </div>
      </div>

      <hr class="mt-2 post-separator-theme" />
      <h5 class="font-theme mx-2">
        {{ user.email }}
      </h5>
    </div>
  </div>
</template>

<script>
export default {
  name: "SearchResult",
  props: {
    user: Object,
  },
  data() {
    return {
      following: null,
    };
  },
  computed: {
    followed() {
      return this.$auth.user.following.includes(this.user.id);
    },
  },
  methods: {
    async follow() {
      let response = await this.$axios.post(`account/${this.user.id}/follow/`);
      this.following = true;
      this.$store.commit("ADD_FOLLOWING", this.user.id);
      debugger
    },

    async unfollow() {
      let response = await this.$axios.post(`account/${this.user.id}/unfollow/`);
      this.following = false;
      debugger
      this.$store.commit("REMOVE_FOLLOWING", this.user.id);
    },
  },
  mounted() {
    if (this.followed) this.following = true;
    else this.following = false;
  },
};
</script>

<style>
</style>
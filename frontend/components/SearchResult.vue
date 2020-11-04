<template>
  <div class="media border p-1">
    <div class="media-body post-color p-1">
      <h5 class="lead mt-0">
        <!-- <strong><nuxt-link :to="{name:'users-id', params: {id: this.currentUser.id}}">{{currentUser.username}}</nuxt-link></strong> -->
        <strong>User number {{userId}}</strong>
      </h5>
    </div>
  </div>
</template>

<script>
export default {
  name: "Search",
  props: {
    userId: "",
  },

  data() {
    return {
      currentUser: ""
    }
  },

  // async mounted() {
  //     try{
  //       let response = await this.$axios.get(`/account/${this.id}/`)
  //       this.currentUser = response.data

  //     }catch(e) {
  //       this.$toast.error(`${e.response.status} ${e.response.statusText}`, {
  //       duration: 8000});
  //       this.$router.push("/home");
  //     }
  //   }
};
</script>

<style>
</style>
<template>
  <div>
    Form....
    <input type="text" v-model="username">
    <button @click="register">register</button>
  </div>
</template>

<script>
export default {
  data() {
    return{
      username: null,
      password: '12341234' //example
    }
  },

  methods: {
    async register() {
      let formData = new FormData();
      formData.append("username", this.username);
      formData.append("password", this.password);
      console.log('here')
      try {
        await this.$axios.post(`/account/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        });
        console.log('here')
        window.location.reload();
        this.$toast.show("Zahtjev uspješno poslan!");
      } catch (e) {
        this.$toast.error(e, { duration: 8000 }); //.response.data.detail
      }
    },
  }
}
</script>
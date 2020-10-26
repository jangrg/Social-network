<template>
  <div class="d-flex flex-column bg justify-content-between">
    <BrandName form="Feel free to register" />
    <div class="mx-auto">
      <div class="lead border rounded mx-auto p-5 white-container justify-content-center">
        <div class="center">
          <div>
            <strong>Register:</strong>
          </div>
          <b-form class="mx-auto mt-2 text-center" @submit.prevent="register">
            <b-form-input
              v-model="email"
              type="email"
              placeholder="Enter your email"
            >
            </b-form-input>
            <b-form-input
              v-model="name"
              type="text"
              placeholder="Enter your name"
            >
            </b-form-input>
            <b-form-input
              v-model="username"
              type="text"
              placeholder="Enter your username"
            >
            </b-form-input>
            <b-form-input
              v-model="password1"
              type="password"
              placeholder="Enter a password"
            >
            </b-form-input>
             <b-form-input
              v-model="password2"
              type="password"
              placeholder="Repeat the password"
              :class="{'notEqual': checkPasswords}"
            >
            </b-form-input>
            <span v-if="checkPasswords">Passwords are not equal!</span>
            <b-form-checkbox v-model="store" class="mt-2"
              >Are you a store?</b-form-checkbox
            >
            <button type="submit" class="btn btn-primary mt-2 text-align">
              Submit
            </button>
          </b-form>
        </div>
      </div>
    </div>
    <div></div>
  </div>

</template>

<script>

import BrandName from '../../components/BrandName'

export default {
  name:"RegisterForm",
  components: {BrandName},
  data() {
    return{
      username: null,
      email: null,
      name: null,
      password1: null, //example
      password2: null,
      store: null
    }
  },
  computed: {
        checkPasswords() {
        return this.password1 !== this.password2;
      }
  },
  methods: {
    async register() {
      let formData = new FormData();
      formData.append("email", this.email);
      formData.append("name", this.name);
      formData.append("password", this.password1);
      formData.append("store", this.store);
      console.log(JSON.stringify(formData));
      try {
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

<style>
.bg {
  /* The image used */
  background-image: url("/marrakech-4500910_1920.jpg");

  height: 100vh;

  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
}

.white-container {
  background-color: whitesmoke;
}

.container-fluid {
  padding: 0;
}

input {
  margin-top: 10px !important;
}

.notEqual {
  color: red;
  border-color: red;
}
</style>
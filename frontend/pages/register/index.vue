<template>
  <div class="d-flex flex-column bg justify-content-between">
    <BrandName form="Feel free to register" />
    <div class="mx-auto">
      <div class="lead border rounded mx-auto p-5 white-container justify-content-center">
        <div class="center">
          <div>
            <strong>Register:</strong>
          </div>
          <b-form class="mx-auto mt-2 text-center">
            <b-form-input
              v-model="form.email"
              type="email"
              placeholder="Enter your email"
            >
            </b-form-input>
            <b-form-input
              v-model="form.name"
              type="text"
              placeholder="Enter your name"
            >
            </b-form-input>
            <b-form-input
              v-model="form.username"
              type="text"
              placeholder="Enter your username"
            >
            </b-form-input>
            <b-form-input
              v-model="form.password"
              type="password"
              placeholder="Enter a password"
            >
            </b-form-input>
             <b-form-input
              v-model="repeatedPassword"
              type="password"
              placeholder="Repeat the password"
              :class="{'notEqual': passwordsDontMatch}"
            >
            </b-form-input>
            <span v-if="passwordsDontMatch">Passwords are not equal!</span>
            <b-form-checkbox v-model="form.store" class="mt-2"
              >Are you a store?</b-form-checkbox
            >
            <button @click.prevent="register" :disabled="passwordsDontMatch" type="submit" class="btn btn-primary mt-2 text-align">
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
      form: {
        username: '',
        email: '',
        name: '',
        password: '',
        store: false
      },
      repeatedPassword: '',
    }
  },
  computed: {
        passwordsDontMatch() {
        return this.form.password !== this.repeatedPassword;
      }
  },
  methods: {
    async register() {
      try {
        console.log('here')
        await this.$axios.post(`/account/`, this.form);
        this.$toast.show("Zahtjev uspješno poslan!");
        // TODO: redirect na homepage
      } catch (e) {
        this.$toast.error(e, { duration: 8000 }); //.response.data.detail
        // TODO: check error json, and show it
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
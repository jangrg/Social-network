<template>
  <div class="d-flex flex-column bg justify-content-between">
    <BrandName form="Please log in" />
    <div class="mx-auto">
      <div class="lead border rounded mx-auto p-5 white-container justify-content-center">
        <div class="center">
          <div>
            <strong>Login:</strong>
          </div>
          <b-form class="mx-auto mt-2 text-center" @submit.prevent="loginUser">
            <b-form-input
              v-model="email"
              type="email"
              placeholder="Enter your email"
            >
            </b-form-input>
            <b-form-input
              class="mt-2"
              v-model="password"
              type="password"
              placeholder="Enter your password"
            >
            </b-form-input>
            <b-form-checkbox v-model="remember" class="mt-2"
              >Remember me</b-form-checkbox
            >
            <button type="submit" class="btn btn-primary mt-2 text-align">
              Submit
            </button>
          </b-form>
          <p class="lead mt-3">
            Not a user?<nuxt-link to="/register" class="ml-5"
              ><b-button variant="primary">Register!</b-button>
            </nuxt-link>
          </p>
          <div class="mt-2">
            <p class="lead text-center">
              Forgot your
              <nuxt-link to="/passwordForgot" class="ml-auto"
                >password?</nuxt-link
              >
            </p>
          </div>
        </div>
      </div>
    </div>
    <div></div>
  </div>
</template>

<script>
import BrandName from "../../components/BrandName";

export default {
  name: "Index",
  components: { BrandName },
  head() {
    return {
      title: "Login",
      meta: [
        {
          name: "viewport",
          content: "width=device-width, initial-scale=1, shrink-to-fit=no",
        },
      ],
    };
  },
  data() {
    return {
      email: null,
      password: null,
      remember: null,
    };
  },
  methods: {
    //Not finished
    async loginUser() {
      let formData = new formData();
      formData.append("email", this.email);
      formData.append("name", this.name);
      formData.append("password", this.password1);

      //axios stuff, ne znam kako sam napraviti. Vjv cemo podatke koje vrati axios spremiti u store i onda preusmjeriti na glavni
      //page

    }
  }
};
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
</style>
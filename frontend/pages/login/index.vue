<template>
  <div class="d-flex flex-column bg justify-content-between">
    <BrandName form="Please log in" />
    <div class="mx-auto">
      <div class="lead border rounded mx-auto p-5 white-container justify-content-center">
        <div class="center">
          <div>
            <strong>Login:</strong>
          </div>
          <b-form class="mx-auto mt-2 text-center">
            <b-form-input
              v-model="form.email"
              type="email"
              placeholder="Enter your email">
            </b-form-input>

            <b-form-input
              class="mt-2"
              v-model="form.password"
              type="password"
              placeholder="Enter your password">
            </b-form-input>

            <b-form-checkbox v-model="form.remember" class="mt-2">
              Remember me
            </b-form-checkbox>

            <button @click.prevent="loginUser" type="submit" class="btn btn-primary mt-2 text-align">
              Login
            </button>
          </b-form>

          <p class="lead mt-4">
            Not a user?  <b-button class="btn btn-primary text-align" variant="primary" to="/register">Register!</b-button>
          </p>

          <div class="mt-2">
            <p class="lead text-center">
              Forgot your
              <nuxt-link to="/passwordForgot" class="ml-auto">password?</nuxt-link>
            </p>
          </div>
        </div>
      </div>
    </div>
    <div></div>
  </div>
</template>

<script>
import BrandName from "../../components/BrandName"

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
      form: {
        email: '',
        password: '',
        remember: false 
      }
    };
  },
  methods: {
    //Not finished
   async loginUser() {
      try {
        
        let user = await this.$axios.post(`/account/`, this.form);
        
        this.$store.commit('User/SET_LOGGED_USER', {
          name: user.name,
          email: user.email
        });

        //redirect na homepage
        this.$router.push('/')

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

</style>
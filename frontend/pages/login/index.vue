<template>
  <div class="d-flex flex-column bg justify-content-between">
    <BrandName form="Please log in" />
    <div class="mx-auto">
      <div class="lead border rounded mx-auto p-5 white-container justify-content-center">
        <div class="center ">
          <div>
            <strong>Login:</strong>
          </div>
          <b-form class="mx-auto mt-2 text-center" @submit.prevent="loginUser">
            <b-form-input
              v-model="form.email"
              type="email"
              placeholder="Enter your email"
            >
            </b-form-input>
            <b-form-input
              v-model="form.username"
              type="text"
              placeholder="Enter your username"
            >
            </b-form-input>
            <b-form-input
              class="mt-2"
              v-model="form.password"
              type="password"
              placeholder="Enter your password"
            >
            </b-form-input>
            <b-form-checkbox v-model="form.remember" class="mt-2"
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
      form:{
        email: '',
        username: '',
        password: '',
        remember: false,
      }
    };
  },
  methods: {
    async loginUser() {
      try{
        let data = await this.$axios.post(`/account/login/`, this.form);
        if (data.data.error != undefined) throw data.data.error;

        this.$store.commit('User/SET_LOGGED_USER', {
          name: this.form.username, email: this.form.email});

        this.$router.push('/');
      }catch(e){
        this.$toast.error(e, { duration: 8000 });
        console.log(e);
        this.$router.push('/login');
      }
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

p.lead{
  align-content: center;
  justify-content: center;
}
</style>
<template>
  <div class="d-flex flex-column bg justify-content-between">
    <!-- <BrandName form="Please log in" /> -->
    <div class="mx-auto center-vertical">
      <div
        class="border-theme font-theme mx-auto p-5 bg-color justify-content-center text-white"
      >
        <div class="center">
          <div class="text-center">
            <strong class="text-theme text-title">WeShare</strong>
          </div>
          <!-- <div>
            <strong class="text-theme">Login:</strong>
          </div> -->
          <b-form class="mx-auto mt-2 text-center">
            <b-form-input
              class="input-style"
              v-model="form.username"
              placeholder="Enter your username"
            >
            </b-form-input>

            <b-form-input
              class="mt-2 input-style"
              v-model="form.password"
              type="password"
              placeholder="Enter your password"
            >
            </b-form-input>

            <!-- <b-form-checkbox v-model="form.remember" class="mt-2">
              Remember me
            </b-form-checkbox> -->

            <button
              @click.prevent="loginUser"
              type="submit"
              class="btn btn-purple mt-2 text-align"
            >
              Login
            </button>
          </b-form>

          <p class="lead mt-4">
            <span class="p-2">Not a user?</span>
            <b-button variant="btn btn-purple text-align" to="/register"
              >Register!</b-button
            >
          </p>

          <div class="mt-2 text-center mx-auto">
            <b-form-checkbox v-model="passwordForgot" class="mt-2">
              Forgot your password?
            </b-form-checkbox>

            <div class="forgottenPass" v-if="passwordForgot">
              <b-form-input
                class="input-style"
                v-model="emailForPassword"
                type="email"
                placeholder="Enter your email"
              >
              </b-form-input>
            </div>

            <button
              v-if="passwordForgot"
              @click.prevent="forgottenPassword"
              type="submit"
              class="btn btn-wider btn-purple mt-2 text-align"
            >
              Send email
            </button>
          </div>
        </div>
      </div>
    </div>
    <div></div>
  </div>
</template>

<script>

export default {
  name: "Index",
  middleware: ["auth-loggedIn"],
  head() {
    return {
      title: "WeShare",
      meta: [
        {
          name: "viewport",
          content: "width=device-width, initial-scale=1, shrink-to-fit=no"
        }
      ]
    };
  },
  data() {
    return {
      form: {
        username: "",
        password: ""
      },
      passwordForgot: false,
      emailForPassword: " "
    };
  },
  methods: {
    async loginUser() {
      try {
        await this.$auth.loginWith("local", {
          data: this.form
        });

        // redirect to user profile
        this.$router.push("/home");
      } catch (e) {
        if (e.response.status == 401)
          this.$toast.error(`Not a registered user!`, { duration: 8000 });
        else
          this.$toast.error(`${e.response.status} ${e.response.statusText}`, {
            duration: 8000
          });
        this.$router.push("/login");
      }
    },
    async forgottenPassword() {
      try {
        if (this.passwordForgot == true) {
          let data = await this.$axios.post(`/password_reset/`, {
            email: this.emailForPassword
          });
          this.$toast.show("Email sent!", { duration: 8000 });
        }
      } catch (e) {
        if (e.response.status == 400)
          this.$toast.error(`Not a registered user!`, { duration: 8000 });
        else
          this.$toast.error(`${e.response.status} ${e.response.statusText}`, {
            duration: 8000
          });
        this.$router.push("/login");
      }
    }
  }
};
</script>

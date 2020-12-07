<template>
  <div class="d-flex flex-column bg">
    <div class="mx-auto font-theme mt-2">
      <div
        class="border-theme mx-auto p-5 bg-color justify-content-center text-white"
      >
        <div class="center">
          <div class="text-center">
            <strong class="text-theme text-title">WeShare</strong>
          </div>
          <b-form class="mx-auto mt-2 text-center">
            <b-form-input
              class="input-style"
              v-model="form.email"
              type="email"
              placeholder="Enter your email"
            >
            </b-form-input>

            <b-form-input
              class="input-style"
              v-model="form.first_name"
              type="text"
              placeholder="Enter your first name"
            >
            </b-form-input>

            <b-form-input
              class="input-style"
              v-model="form.last_name"
              type="text"
              placeholder="Enter your lastname"
            >
            </b-form-input>

            <b-form-input
              class="input-style"
              v-model="form.username"
              type="text"
              placeholder="Enter your username"
            >
            </b-form-input>

            <b-form-input
              class="input-style"
              v-model="form.password"
              type="password"
              placeholder="Enter a password"
              :class="{ notEqual: passCheck }"
            >
            </b-form-input>

            <span class="passCheck" v-if="passCheck"
              >Password should have 8 characters both letters and numbers.</span
            >

            <b-form-input
              class="input-style"
              :disabled="passCheck"
              v-model="repeatedPassword"
              type="password"
              placeholder="Repeat the password"
              :class="{ notEqual: passwordsDontMatch }"
            >
            </b-form-input>

            <span v-if="passwordsDontMatch">Passwords are not equal!</span>

            <b-form-input
              class="input-style"
              v-model="form.birth_date"
              type="date"
              placeholder="Enter your date of birth"
            >
            </b-form-input>

            <b-form-checkbox v-model="form.store" class="mt-3 mb-2">
              Are you a store?</b-form-checkbox
            >

            <button
              @click.prevent="register"
              :disabled="allowSubmit"
              type="submit"
              class="btn btn-purple mt-2 text-align"
            >
              Submit
            </button>

            <p class="lead mt-4">
              Already a user?
              <b-button variant="btn btn-purple text-align" to="/login"
                >Login</b-button
              >
            </p>
          </b-form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: "RegisterForm",
  middleware: ["auth-loggedIn"],
  head() {
    return {
      title: "Register",
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
        email: "",
        first_name: "",
        last_name: "",
        password: "",
        birth_date: ""
      },
      repeatedPassword: "",
      store: false
    };
  },
  computed: {
    passwordsDontMatch() {
      return (
        this.form.password !== this.repeatedPassword &&
        this.repeatedPassword.length > 0
      );
    },

    passCheck() {
      if (
        this.form.password.length >= 8 &&
        /[a-zA-Z]/g.test(this.form.password) &&
        /\d/.test(this.form.password)
      )
        return false;

      if (this.form.password.length > 0) return true;
    },

    allowSubmit() {
      return this.form.password !== this.repeatedPassword;
    }
  },
  methods: {
    async register() {
      try {
        let response = await this.$axios.post(`account/`, this.form);
        this.$toast.show(response.data.message, { duration: 8000 });

        // this.$store.commit('User/SET_LOGGED_USER', response.data);

        // redirect to user profile
        this.$router.push("/");
      } catch (e) {
        this.$toast.error(e, { duration: 8000 });
      }
    }
  }
};
</script>

<style></style>

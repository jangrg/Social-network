<template>
  <div class="d-flex flex-column bg justify-content-between">
    <div class="mx-auto center-vertical">
      <div
        class="font-theme border-theme rounded mx-auto p-5 bg-color justify-content-center"
      >
        <div class="center">
          <div>
            <strong class="text-theme">{{ this.header }}</strong>
          </div>
          <div v-if="showReset" class="center">
            <b-form class="mx-auto mt-2 text-center">
              <b-form-input
                v-model="form.password"
                type="password"
                placeholder="Enter a password"
                :class="{ notEqual: passCheck }"
              >
              </b-form-input>

              <span class="passCheck" v-if="passCheck"
                >Password should have 8 characters both letters and
                numbers.</span
              >

              <b-form-input
                :disabled="passCheck"
                v-model="repeatedPassword"
                type="password"
                placeholder="Repeat the password"
                :class="{ notEqual: passwordsDontMatch }"
              >
              </b-form-input>

              <span v-if="passwordsDontMatch">Passwords are not equal!</span>
              <div>
                <button
                  @click.prevent="changePassword"
                  :disabled="allowSubmit"
                  type="submit"
                  class="btn btn-purple btn-wider mt-2 text-align"
                >
                  Change password
                </button>
              </div>
            </b-form>
          </div>
          <div class="mt-2 text-center mx-auto">
            <div class="forgottenPass" v-if="resetAgain">
              <b-form-input
                v-model="emailForPassword"
                type="email"
                placeholder="Enter your email"
              >
              </b-form-input>
            </div>

            <button
              v-if="resetAgain"
              @click.prevent="forgottenPassword"
              type="submit"
              class="btn btn-primary btn-wider mt-2 text-align"
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
import TopBar from "@/components/TopBar";
import styles from "@/static/style.css";

export default {
  name: "RegisterForm",
  components: { TopBar },
  middleware: ["auth-loggedIn"],
  //theme
  head() {
    var theme = this.$auth.$storage.getCookie("theme") == "dark" ? "/theme.css" : "/light-theme.css"
    return {
      title: "Register",
      meta: [
        {
          name: "viewport",
          content: "width=device-width, initial-scale=1, shrink-to-fit=no",
        },
      ],
      link: [
        {
          rel: "stylesheet",
          href: theme,
          //this.user.theme == "dark" ? "/theme.css" : "/light-theme.css"
        },
      ],
    };
  },

  data() {
    return {
      header: "Verifying token ...",
      form: {
        password: "",
        token: this.$route.params.token,
      },
      repeatedPassword: "",
      showReset: false,
      resetAgain: false,
      emailForPassword: "",
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
    },
  },
  async mounted() {
    try {
      console.log(this.form.token);
      var token = this.form.token;
      await this.$axios.post(`/password_reset/validate_token/`, { token });
      this.header = "Reset password:";
      this.showReset = true;
    } catch (e) {
      this.header = "Your token has expired!";
      this.resetAgain = true;
    }
  },
  methods: {
    async changePassword() {
      try {
        let response = await this.$axios.post(
          `/password_reset/confirm/`,
          this.form
        );
        console.log(response);
        this.$toast.show(response.data.message, { duration: 8000 });
        this.$router.push("/login");
      } catch (error) {
        this.$toast.error(`${error.response.data.password}`, {
          duration: 8000,
        });
        this.form.password = "";
        this.repeatedPassword = "";
      }
    },
    async forgottenPassword() {
      try {
        let data = await this.$axios.post(`/password_reset/`, {
          email: this.emailForPassword,
        });
        this.$toast.show("Email sent!", { duration: 8000 });
      } catch (e) {
        if (e.response.status == 400)
          this.$toast.error(`Not a registered user!`, { duration: 8000 });
        else
          this.$toast.error(`${e.response.status} ${e.response.statusText}`, {
            duration: 8000,
          });
        this.$router.push("/register");
      }
    },
  },
};
</script>

<style></style>

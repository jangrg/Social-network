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
              placeholder="Enter your email">
            </b-form-input>

            <b-form-input
              v-model="form.firstname"
              type="text"
              placeholder="Enter your first name">
            </b-form-input>

            <b-form-input
              v-model="form.lastname"
              type="text"
              placeholder="Enter your surname">
            </b-form-input>

            <b-form-input
              v-model="form.username"
              type="text"
              placeholder="Enter your username">
            </b-form-input>

            <b-form-input
              v-model="form.password"
              type="password"
              placeholder="Enter a password"
              :class="{'notEqual': passCheck}">
            </b-form-input>

            <span class="passCheck" v-if="passCheck">Password should have 8 characters both letters and numbers.</span>

             <b-form-input :disabled="passCheck"
              v-model="repeatedPassword"
              type="password"
              placeholder="Repeat the password"
              :class="{'notEqual': passwordsDontMatch}">
            </b-form-input>
            
            <span v-if="passwordsDontMatch">Passwords are not equal!</span>

            <b-form-checkbox v-model="form.store" class="mt-3 mb-2">
              Are you a store?</b-form-checkbox>

            <button @click.prevent="register" :disabled="allowSubmit" type="submit" class="btn btn-primary mt-2 text-align">
              Submit
            </button>

            <p class="lead mt-4">
            Already a user?  <b-button class="btn btn-primary text-align" variant="primary" to="/login">Login</b-button>
          </p>

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

  head() {
    return {
      title: "Register",
      meta: [
        {
          name: "viewport",
          content: "width=device-width, initial-scale=1, shrink-to-fit=no",
        },
      ],
    };
  },

  data() {
    return{
      form: {
        username: '',
        email: '',
        firstname: '',
        surname:'',
        password: '',
        store: false
      },
      repeatedPassword: '',
    }
  },
  computed: {
        passwordsDontMatch() {
        return this.form.password !== this.repeatedPassword && this.repeatedPassword.length > 0 ;
      },

      passCheck(){
        if (this.form.password.length >= 8  && /[a-zA-Z]/g.test(this.form.password) && /\d/.test(this.form.password))
          return false;

        if (this.form.password.length > 0 )
          return true;
      },

      allowSubmit(){
        return this.form.password !== this.repeatedPassword
      }
  },
  methods: {
    async register() {
      try {
        
        let response = await this.$axios.post(`/account/create/`, this.form);
        this.$toast.show("Zahtjev uspješno poslan!", { duration: 8000 });

        this.$store.commit('User/SET_LOGGED_USER', response.data.user);

        // redirect to user profile
        this.$router.push('/');

      } catch (e) {
        this.$toast.error(e, { duration: 8000 });
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

.passCheck{
  font-size: 0.8rem;
}
</style>
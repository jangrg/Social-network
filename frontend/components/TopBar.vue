<template>
  <div class="container-fluid sticky-top font-theme-top-bar">
    <b-navbar class="top-bar top-bar-theme">
      <div class="row container-fluid center inline-block">
        <b-navbar class="col-2 topbar-logo"
          ><nuxt-link class="logo" to="/home"> WeShare </nuxt-link></b-navbar
        >
        <div class="col-4">
          <b-form class="navbar-form fix form-theme">
            <b-form-input
              type="search"
              class="form-control search-bar input-grey"
              v-model="searchQuery"
              placeholder="Search"
            ></b-form-input>
            <button
              @click.prevent="search"
              class="btn search-btn"
              :disabled="!allowSearch"
              type="submit"
            ></button>
          </b-form>
        </div>
        <div class="links" v-if="!this.$auth.user">
          <b-button variant="btn btn-purple text-align btn-lg" to="/register"
            >Register</b-button
          >
          <b-button variant="btn btn-purple text-align btn-lg" to="/login"
            >Login</b-button
          >
        </div>
        <!-- <div class="col-2" v-if="this.$auth.user">
          <button class="btn btn-lg ml-auto" v-b-toggle.sidebar-right>
            <i class="fa fa-bars"></i>
          </button>
        </div-->
        <div
          class="topbar-buttons col-2 avatar d-flex justify-content-end"
          v-if="this.$auth.user"
        >
          <b-button
            id="button-home"
            class="button button-home"
            variant="btn text-align btn-lg"
            v-bind:class="selectedHome"
            to="/home"
            v-if="this.user"
          ></b-button>
          <b-button
            id="button-explore"
            class="button button-explore"
            variant="btn text-align btn-lg"
            v-bind:class="selectedExplore"
            to="/explore"
            v-if="this.user"
          ></b-button>
          <b-button
            id="button-message"
            class="button button-message"
            variant="btn text-align btn-lg"
            v-bind:class="selectedMessage"
            v-if="this.user"
            to="/messages"
          ></b-button>
          <b-button
            id="button-store"
            class="button button-store"
            variant="btn text-align btn-lg"
            v-bind:class="selectedStore"
            v-if="hasStore"
            :to="{ name: 'store-id', params: { id: this.store.id } }"
          ></b-button>
          <b-dropdown
            size="sm"
            variant="outline-dark"
            class="float-right remove-style"
            no-caret
            v-if="user"
          >
            <template #button-content>
              <b-avatar class="mb-2 usericon" variant="dark"> </b-avatar>
              <span class="topbar-username">{{ user.username }}</span>
            </template>
            <b-dropdown-item
              :to="{ name: 'users-id', params: { id: this.user.id } }"
              >Account</b-dropdown-item
            >
            <b-dropdown-item @click.prevent="logOut">Logout</b-dropdown-item>
          </b-dropdown>
          <!-- <b-button
            variant="btn btn-purple text-align btn-lg btn-logout"
            @click.prevent="logOut"
            v-if="this.user"
            >Logout</b-button
          > -->
        </div>
      </div>
    </b-navbar>
  </div>
</template>

<script>
export default {
  name: "TopBar",
  data() {
    return {
      // posts: [],
      searchQuery: "",
      route: this.$nuxt.$route.name,
      store: false
    };
  },
  async beforeCreate() {
    try {
      let token = this.$auth.getToken("local");
      let response = await this.$axios.get("page/my_page/", {
        headers: { Authorization: `${token}` }
      });
      this.store = response.data;
    } catch (e) {}
  },
  computed: {
    user() {
      return this.$auth.user;
    },
    allowSearch() {
      return this.searchQuery != "";
    },
    selectedHome() {
      if (this.route == "home") {
        return "home-clicked";
      }
    },
    selectedExplore() {
      if (this.route == "explore") {
        return "explore-clicked";
      }
    },
    selectedMessage() {
      if (this.route == "messages") {
        return "message-clicked";
      }
    },
    selectedStore() {
      console.log(this.route);
      if (this.route == "store-id") {
        return "store-clicked";
      }
    },
    hasStore() {
      if (this.store == false) return false;
      return true;
    }
  },
  head: function() {
    var theme =
      this.$auth.$storage.getCookie("theme") == "dark"
        ? "/theme.css"
        : "/light-theme.css";
    return {
      link: [
        {
          rel: "stylesheet",
          href:
            "https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"
        },
        {
          rel: "stylesheet",
          href: theme
        }
      ]
    };
  },
  methods: {
    search() {
      this.$router.push({
        name: "search-keyword",
        params: { keyword: this.searchQuery }
      });
    },

    logOut() {
      this.$auth.logout();
      this.$router.push("/");
    }
  }
};
</script>

<style></style>

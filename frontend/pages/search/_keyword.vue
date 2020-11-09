<template>
  <div class="d-flex flex-column bg-pattern">
    <TopBar />
    <SideBar />

    <div class="container-fluid row  mx-auto">
      <div class="col-md-2"></div>  
      <div v-if="loaded" class="col-md-8 white-container rounded">
        <h3>Search result({{searchResult.length}}):</h3>
        <SearchResult v-for="result in searchResult" :key="result.id" :user="result"/>
      </div>
      
      <div class="col-md-2"></div>
    </div>
  </div>
</template>

<script>
import TopBar from "../../components/TopBar";

import SideBar from "../../components/SideBar";

import SearchResult from "../../components/SearchResult";

export default {
    name: "Home",
    components: { TopBar, SideBar, SearchResult },
    middleware: ['auth-notLoggedIn'],
    head() {
      return {
        title: "Login",
        meta: [
          {
            name: "viewport",
            content: "width=device-width, initial-scale=1, shrink-to-fit=no"
          }
        ]
      }
    },

    data() {
      return {
        loaded: false,
        keyword: this.$route.params.keyword,
        searchResult: []
      }
    },

    async created() {
      try{
        let result = await this.$axios.get(`/account/`, {params: {search: this.keyword}})
        this.searchResult = result.data
        this.loaded = true
      }catch(e) {
        this.$toast.error(`${e.response.status} ${e.response.statusText}`, {
        duration: 8000});
        this.$router.push("/home");
      }
      
    }
  }
</script>

<style scoped>

</style>
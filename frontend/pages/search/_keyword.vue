<template>
  <div class="d-flex flex-column bg-pattern">
    <TopBar />
    <SideBar />

    <div class="container-fluid row  mx-auto">
      <div class="col-md-2"></div>
      <div class="col-md-8 white-container rounded">
        <h3>Search result({{searchResult.length}}):</h3>
        <SearchResult userId="1"/>
        <SearchResult userId="2"/>
        <SearchResult userId="3"/>
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
        keyword: this.$route.params.keyword,
        searchResult: []
      }
    },

    async mounted() {
       try{
        let result = await this.$axios.get(`/account/`, {params: {search: this.keyword}})
        this.searchResult = result.data
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
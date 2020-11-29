<template>
<div class="container-fluid">
    <b-navbar class="top-bar-theme">
        <b-navbar-brand class="lead-text font-theme-top-bar"><strong>WeShare - {{ form }}</strong></b-navbar-brand>
    </b-navbar>
</div>
  
</template>

<script>
export default {
    name: 'BrandName',
    props: {
        form: String
    }
    
}
</script>

<style>

</style>